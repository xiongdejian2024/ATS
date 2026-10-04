#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import pytest
import copy
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.constants.gb32960_data import *
from xat_ecu.api.constants.config_data import *


@allure.feature("互联服务/远程控制/远程解闭锁")
@allure.story("远程解闭锁")
class TestGB32960(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "GB32960Service_server",
                         "HighVoltageService_server", "VehicleTimeService_server",
                         "CarConfigService_server","ConfigMasterService_server"])
        self.mix.start_get_request_and_send_response_to_tcam_thread(["VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "GB32960Service_server",
                         "HighVoltageService_server", "VehicleTimeService_server",
                         "CarConfigService_server"], {'GetVIN':{'vin':self.tb_config['vin']}})
        self.gb_config = gb_config_data
        self.gb_config[5]["value"] = 1
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5)
        # self.soa.stop_soa()
        self.ssh.tcam_ssh.exec("reboot -f")
        time.sleep(300)

        sleep(2)
        self.vin = self.tb_config["vin"]
        # self.soa.check_GetVIN_req_and_feedback_resp(vin=self.vin,timeout=30)
    

    def before_each_func(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.NORMAL)
        self.soa.s2s_set_car_mode(car_mode=CarMode.NORMAL)
        self.soa.s2s_set_mntnmode(mntnmode=False)
        self.soa.notify_OutputState(on=False)
        self.soa.notify_HVThermalOutOfControl()
        self.soa.notify_NotifyHvBatteryCode()
        self.soa.notify_NotifyVIN(vin=self.tb_config["vin"])
        self.soa.notify_VehicleTimeInfo(sync_sts=TimeSyncSts.NTP)

        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))

    def after_each_func(self, ecu):
        self.soa.notify_OutputState(on=False)
        self.soa.s2s_set_car_mode(car_mode=CarMode.NORMAL)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))

    def after_class(self, ecu):
        self.mix.stop_get_request_and_send_response_to_tcam_thread()
        pass

    def login_or_logout(self,login_flage:bool=True, buffer:int=1):
        if login_flage:
            self.soa.notify_OutputState()
        else:
            self.soa.notify_OutputState(on=False)
        login_time = time.time()
        logger.info("Start GB32960 report")
        t_login = int(login_time-buffer)
        t_login_buffer = int(login_time+buffer)
        return login_time,t_login,t_login_buffer
    
    
    def Warninglevel(self, warning_name:str='HvPackUUnderFltPrm', warning_level:int=1,time_stamp:int=30):
        self.soa.notify_GB32960Data(gb32960_data) 
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"][warning_name] = warning_level
        self.soa.notify_GB32960Data(gb_data) 
        str_a_time = int(time.time())#一级报警触发时间
        time.sleep(time_stamp)
        return str_a_time

    def check_gb_reissuegbdata_cycle(self, gb_data_list:list,cycle_time):
        s_time = self.tsp.datetime_to_timestamp(gb_data_list[0]['updateTime'])
        for data in gb_data_list[1:]:
            updateTime = self.tsp.datetime_to_timestamp(data['updateTime'])
            logger.info("报文时间戳： {0}".format(updateTime))
            assert  updateTime - s_time <= cycle_time
            s_time = updateTime
            

    @pytest.mark.full
    def test_gb32960_loginlogout_successfully_when_carmode_normal_usagemode_inactive_caseid_101485(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        # gb_data["VehStatus"]["VehSts"] = 0
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
        

    @pytest.mark.sanity
    def test_gb32960_loginlogout_successfully_when_carmode_normal_usagemode_convenience_caseid_1903368(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
        

    @pytest.mark.full
    def test_gb32960_loginlogout_successfully_when_carmode_normal_usagemode_active_caseid_101487(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_loginlogout_successfully_when_carmode_normal_usagemode_driving_caseid_101488(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)     
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_loginlogout_successfully_when_carmode_crash_usagemode_inactive_caseid_1903598(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_loginlogout_successfully_when_carmode_crash_usagemode_convenience_caseid_101478(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH) 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0

    @pytest.mark.smoke
    def test_gb32960_loginlogout_successfully_when_carmode_crash_usagemode_active_caseid_1903195(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH) 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_loginlogout_successfully_when_carmode_crash_usagemode_driving_caseid_101480(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH)  
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING) 
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_loginlogout_successfully_when_carmode_dyno_usagemode_inactive_caseid_101481(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_loginlogout_successfully_when_carmode_dyno_usagemode_convenience_caseid_101482(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO) 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)  
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_loginlogout_successfully_when_carmode_dyno_usagemode_active_caseid_1903491(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO) 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_loginlogout_successfully_when_carmode_dyno_usagemode_driving_caseid_101484(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO) 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)  
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
    

    @pytest.mark.full
    def test_gb32960_loginlogout_precondition_mismatch_usagemode_abandoned_caseid_101474(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(60)
        self.login_or_logout(False)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        logger.info(f'gb_data: {gb_data}')

    @pytest.mark.full
    def test_gb32960_loginlogout_precondition_mismatch_carmode_transport_caseid_101475(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.TRANSPORT)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(60)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        logger.info(f'gb_data: {gb_data}')

    @pytest.mark.sanity
    def test_gb32960_loginlogout_precondition_mismatch_carmode_factory_caseid_1903323(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.FACTORY)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(60)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        logger.info(f'gb_data: {gb_data}')


    @pytest.mark.full
    def test_gb32960_loginlogin_fail_when_notifymaintenancemode_ture_caseid_1980651(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(60)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        logger.info(f'gb_data: {gb_data}')



    @pytest.mark.sanity
    def test_gb32960_general_warning_undervoltagealarmofenergystoragedevice_caseid_101454(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvPackUUnderFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvPackUUnderFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvPackUUnderFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        # str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["车载储能装置类型欠压报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["车载储能装置类型欠压报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["车载储能装置类型欠压报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["车载储能装置类型欠压报警"])

     
     
    @pytest.mark.full
    def test_gb32960_general_warning_undervoltagealarmofbatterycell_caseid_100076(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvCellUUnderFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellUUnderFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvCellUUnderFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["单体电池欠压报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["单体电池欠压报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["单体电池欠压报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["单体电池欠压报警"])
     

    @pytest.mark.full
    def test_gb32960_general_warning_temperaturedifferencealarm_caseid_100065(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvCellTDifFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellTDifFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvCellTDifFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["温度差异报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["温度差异报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["温度差异报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["温度差异报警"])
     
     
    @pytest.mark.full
    def test_gb32960_general_warning_socjumpalarm_caseid_100080(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvSocHopFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvSocHopFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvSocHopFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["SOC跳变报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["SOC跳变报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["SOC跳变报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["SOC跳变报警"])
     
     
     
    @pytest.mark.full
    def test_gb32960_general_RechargeableEnergyStorageSystemSismatchAlarm_caseid_101452(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发2级报警
        str_a_time = self.Warninglevel(warning_name="HvBattMismatchFltPrm", warning_level=1) #二级报警触发时间
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["可充电储能系统不匹配报警"])
        
     
    @pytest.mark.full
    def test_gb32960_general_warning_PoorBatteryCellConsistencyAlarm_caseid_100075(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvCellUDifFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellUDifFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvCellUDifFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["电池单体一致性差报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["电池单体一致性差报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["电池单体一致性差报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["电池单体一致性差报警"])
     
     
    @pytest.mark.sanity
    def test_gb32960_general_warning_OverVoltageAlarmofEnergyStorageDevice_caseid_101455(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvPackUOverFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvPackUOverFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvPackUOverFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["车载储能装置类型过压报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["车载储能装置类型过压报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["车载储能装置类型过压报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["车载储能装置类型过压报警"])
     
     
     
     
    @pytest.mark.full
    def test_gb32960_general_warning_OverVoltageAlarmofBatteryCell_caseid_100090(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvCellUOverFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellUOverFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvCellUOverFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["单体电池过压报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["单体电池过压报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["单体电池过压报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["单体电池过压报警"])
     
     
     
    @pytest.mark.full
    def test_gb32960_general_warning_OverHighSOCAlarm_caseid_100078(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvSocHiFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvSocHiFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvSocHiFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["SOC过高报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["SOC过高报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["SOC过高报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["SOC过高报警"])
     
     
    @pytest.mark.full
    def test_gb32960_general_warning_OverchargeAlarmofEnergyStorageDevice_caseid_100066(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvPackOverChrgFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvPackOverChrgFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvPackOverChrgFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["车载储能装置类型过充"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["车载储能装置类型过充"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["车载储能装置类型过充"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["车载储能装置类型过充"])
        
        
        
    @pytest.mark.sanity
    def test_gb32960_general_warning_LowSOCAlarm_caseid_101453(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvSocLoFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvSocLoFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvSocLoFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["SOC低报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["SOC低报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["SOC低报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["SOC低报警"])
     
     
     
    @pytest.mark.sanity
    def test_gb32960_general_warning_InsulationAlarm_caseid_1903803(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvlsoFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["绝缘报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["绝缘报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["绝缘报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["绝缘报警"])
     
     
    @pytest.mark.full
    def test_gb32960_general_warning_DriveMotorTemperatureAlarm_caseid_100087(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvCellTOverFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellTOverFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvCellTOverFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["电池高温报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["电池高温报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["电池高温报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["电池高温报警"])
     

    @pytest.mark.full
    def test_gb32960_general_DriveMotorTemperatureAlarm_caseid_100077(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发2级报警
        str_a_time = self.Warninglevel(warning_name="IemGenericMotTAlrmStPrm", warning_level=1) #二级报警触发时间
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["驱动电机温度报警"])


    @pytest.mark.full
    def test_gb32960_general_DriveMotorControllerTemperatureAlarm_caseid_100088(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发2级报警
        str_a_time = self.Warninglevel(warning_name="IemGenericInvrtTAlrmStPrm", warning_level=1) #二级报警触发时间
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["驱动电机控制器温度报警"])


    @pytest.mark.full
    def test_gb32960_general_DCDCTemperatureAlarm_caseid_100079(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="FltTDcDcPrm", warning_level=1) #一级报警触发时间
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报")
        logger.info(f'一级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,1,["DC-DC温度报警"])
        
        
    @pytest.mark.full
    def test_gb32960_general_DCDCStatusAlarm_caseid_101449(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发2级报警
        str_a_time = self.Warninglevel(warning_name="FltElecDcDcPrm", warning_level=1) #2级报警触发时间
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        time.sleep(60)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["DC-DC状态报警"])



    @pytest.mark.full
    def test_gb32960_TCAM_Control_thermal_runaway_caseid_100782(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(35)     
        # 触发1级报警
        str_a_time = self.Warninglevel(warning_name="EscWarnIndcnReqPrm", warning_level=0) #一级报警触发时间
        # #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        gb_data["WarningData"]["AbsWarnIndcnReqPrm"] = 0
        gb_data["WarningData"]["BrkSysWarnIndcnReqPrm"] = 0
        gb_data["WarningData"]["BrkSysWarnIndcnReqSecPrm"] = 0    
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(30)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        # #触发3级报警
        str_c_time = self.Warninglevel(warning_name="BrkWarnIndcnReqPrm", warning_level=0)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,0,[])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,0,[])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(c_gb_data,0,[])
        
        
    @pytest.mark.smoke
    def test_gb32960_JIDU_LoginLogout_successfully_when_CarMode_Normal_UsageMode_Abandon_caseid_1939951(self, ecu):
        #TCAM休眠
        self.mix.tcam_network_sleep(360)
        #唤醒TCAM
        self.tsp.rvc_taskCmd()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.io.tcam_kl15_up()
        self.soa.notify_VehicleTimeInfo(sync_sts=TimeSyncSts.NTP)
        time.sleep(2)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout(buffer=5)
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
        
        
    @pytest.mark.full
    def test_gb32960_loginlogout_successfully_when_HVThermalOutOfControl_ture_caseid_1987629(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        self.soa.notify_HVThermalOutOfControl(True)
        login_time = time.time()
        t_login = int(login_time-1)
        t_login_buffer = int(login_time+1)
        logger.info("Start GB32960 report")
        time.sleep(61)
        self.soa.notify_HVThermalOutOfControl(False)
        logout_time = time.time()
        t_logout = int(logout_time-1)
        t_login_buffer = int(logout_time+1)

        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(login_time, logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_login_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
        
    @pytest.mark.full
    def test_gb32960_loginlogout_NotifyMaintenanceMode_ture_caseid_1980650(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(60)
        self.login_or_logout(False)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        logger.info(f'gb_data: {gb_data}')
        
        

    @pytest.mark.smoke
    def test_gb32960_general_warning_BrakeSystemWarning_caseid_1903177(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        # 触发1级报警
        str_a_time = self.Warninglevel(warning_name="EscWarnIndcnReqPrm", warning_level=0) #一级报警触发时间
        time.sleep(1)
        # #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        gb_data["WarningData"]["AbsWarnIndcnReqPrm"] = 0
        gb_data["WarningData"]["BrkSysWarnIndcnReqPrm"] = 0
        gb_data["WarningData"]["BrkSysWarnIndcnReqSecPrm"] = 0    
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        # #触发3级报警
        str_c_time = self.Warninglevel(warning_name="BrkWarnIndcnReqPrm", warning_level=0)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["制动系统报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["制动系统报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["制动系统报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["制动系统报警"])
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_RealtimePeriod_is_30s_caseid_101544(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][1]['value'] = 30
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报",cycle_time=30)
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_RealtimePeriod_is_10s_caseid_101545(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][1]['value'] = 10
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报",cycle_time=10)
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_RealtimePeriod_is_1s_caseid_101546(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][1]['value'] = 1
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报",cycle_time=10)
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][1]['value'] = 10
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_RmsActivate_is_Deactivated_caseid_101547(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][0]['value'] = 0
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(60)
        self.login_or_logout(False)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(60)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        logger.info(f'gb_data: {gb_data}')
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_RmsActivate_is_activated_caseid_101548(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][0]['value'] = 1
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报",cycle_time=10)
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
       
       
    @pytest.mark.full
    def test_gb32960_ParamCfg_RmsLoginDelayTime_is_0s_caseid_101539(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][3]['value'] = 0
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        self.soa.notify_OutputState()
        login_time = time.time()
        t_login = int(login_time-1)
        t_login_buffer = int(login_time+1)
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(login_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报",cycle_time=10)
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0 
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_RmsLoginDelayTime_is_30s_caseid_101538(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][3]['value'] = 30
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        self.soa.notify_OutputState()
        login_time = time.time()+30
        t_login = int(login_time-1)
        t_login_buffer = int(login_time+1)
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(login_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报",cycle_time=10)
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
        
         
    @pytest.mark.full
    def test_gb32960_ParamCfg_RmsLoginDelayTime_is_60s_caseid_101537(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][3]['value'] = 60
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        self.soa.notify_OutputState()
        login_time = time.time()+60
        t_login = int(login_time-1)
        t_login_buffer = int(login_time+1)
        logger.info("Start GB32960 report")
        time.sleep(121)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(login_time, str_logout_time))
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][3]['value'] = 0
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报",cycle_time=10)
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
        

    @pytest.mark.full
    def test_gb32960_LoginLogout_Precondition_Mismatch_RMSActive_deactivated_caseid_101473(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][0]['value'] = 0
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(60)
        self.login_or_logout(False)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        logger.info(f'gb_data: {gb_data}')
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][0]['value'] = 1#打开RMS激活
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))

        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_TemperatureDifferenceAlarm_caseid_101527(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][0]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="HvCellTDifFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][0]['value'] = 2 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellTDifFltPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][0]['value'] = 3 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        # time.sleep(2)
        str_c_time = self.Warninglevel(warning_name="HvCellTDifFltPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][0]['value'] = 0 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["温度差异报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["温度差异报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["温度差异报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["温度差异报警"])
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_BatteryHighTemperatureAlarm_caseid_101526(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][1]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="HvCellTOverFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][1]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellTOverFltPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][1]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="HvCellTOverFltPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][1]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["电池高温报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["电池高温报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["电池高温报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["电池高温报警"])
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_OverVoltageAlarmofEnergyStorageDevice_caseid_101525(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][2]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="HvPackUOverFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][2]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvPackUOverFltPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][2]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="HvPackUOverFltPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["车载储能装置类型过压报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["车载储能装置类型过压报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["车载储能装置类型过压报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["车载储能装置类型过压报警"])
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_UnderVoltageAlarmofEnergyStorageDevice_caseid_101524(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][3]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="HvPackUUnderFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][3]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvPackUUnderFltPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][3]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="HvPackUUnderFltPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][3]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["车载储能装置类型欠压报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["车载储能装置类型欠压报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["车载储能装置类型欠压报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["车载储能装置类型欠压报警"])
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_LowSOCAlarm_caseid_101523(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][4]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="HvSocLoFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][4]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvSocLoFltPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][4]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="HvSocLoFltPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][4]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["SOC低报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["SOC低报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["SOC低报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["SOC低报警"])
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_OverVoltageAlarmofBatteryCell_caseid_101522(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][5]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="HvCellUOverFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][5]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellUOverFltPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][5]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="HvCellUOverFltPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][5]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["单体电池过压报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["单体电池过压报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["单体电池过压报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["单体电池过压报警"])
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_UnderVoltageAlarmofBatteryCell_caseid_101521(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][6]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="HvCellUUnderFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][6]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellUUnderFltPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][6]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="HvCellUUnderFltPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][6]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["单体电池欠压报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["单体电池欠压报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["单体电池欠压报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["单体电池欠压报警"])
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_OverHighSOCAlarm_caseid_100071(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][7]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="HvSocHiFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][7]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvSocHiFltPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][7]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="HvSocHiFltPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][7]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["SOC过高报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["SOC过高报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["SOC过高报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["SOC过高报警"])
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_SOCJumpAlarm_caseid_101520(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][8]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="HvSocHopFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][8]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvSocHopFltPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][8]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="HvSocHopFltPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][8]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["SOC跳变报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["SOC跳变报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["SOC跳变报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["SOC跳变报警"])
        
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_RechargeableEnergyStorageSystemSismatchAlarm_caseid_101519(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][9]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="HvBattMismatchFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][9]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvBattMismatchFltPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][9]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="HvBattMismatchFltPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][9]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["可充电储能系统不匹配报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["可充电储能系统不匹配报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["可充电储能系统不匹配报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["可充电储能系统不匹配报警"])
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_PoorBatteryCellConsistencyAlarm_caseid_101518(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][10]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="HvCellUDifFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][10]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellUDifFltPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][10]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="HvCellUDifFltPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][10]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["电池单体一致性差报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["电池单体一致性差报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["电池单体一致性差报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["电池单体一致性差报警"])
        
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_InsulationAlarm_caseid_101517(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][11]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][11]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvlsoFltPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][11]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][11]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["绝缘报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["绝缘报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["绝缘报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["绝缘报警"])
         
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_DCDCTemperatureAlarm_caseid_101516(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][12]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="FltTDcDcPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][12]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["FltTDcDcPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][12]['value'] = 3 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="FltTDcDcPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][12]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["DC-DC温度报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["DC-DC温度报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["DC-DC温度报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["DC-DC温度报警"])
        
             
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_BrakeSystemWarning_caseid_101515(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        # 触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][13]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="EscWarnIndcnReqPrm", warning_level=0) #一级报警触发时间
        time.sleep(1)
        # #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][13]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        gb_data["WarningData"]["AbsWarnIndcnReqPrm"] = 0
        gb_data["WarningData"]["BrkSysWarnIndcnReqPrm"] = 0
        gb_data["WarningData"]["BrkSysWarnIndcnReqSecPrm"] = 0    
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        # #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][13]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="BrkWarnIndcnReqPrm", warning_level=0)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][13]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["制动系统报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["制动系统报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["制动系统报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["制动系统报警"])
        
        
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_DCDCStatusAlarm_caseid_101514(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][14]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="FltElecDcDcPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][14]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["FltElecDcDcPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][14]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="FltElecDcDcPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][14]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["DC-DC状态报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["DC-DC状态报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["DC-DC状态报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["DC-DC状态报警"])
        
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_DriveMotorControllerTemperatureAlarm_caseid_101513(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][15]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="IemGenericInvrtTAlrmStPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][15]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["IemGenericInvrtTAlrmStPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][15]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="IemGenericInvrtTAlrmStPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][15]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["驱动电机控制器温度报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["驱动电机控制器温度报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["驱动电机控制器温度报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["驱动电机控制器温度报警"])
        
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_HighVoltageInterlock_caseid_101512(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][16]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="HvilFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][16]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvilFltPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][16]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="HvilFltPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][16]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["高压互锁状态报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["高压互锁状态报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["高压互锁状态报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["高压互锁状态报警"])
        
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_DriveMotorTemperatureAlarm_caseid_101511(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][17]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="IemGenericMotTAlrmStPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][17]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["IemGenericMotTAlrmStPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][17]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="IemGenericMotTAlrmStPrm", warning_level=1)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][17]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["驱动电机温度报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["驱动电机温度报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["驱动电机温度报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["驱动电机温度报警"])
        
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningLevel_OverchargeAlarmofEnergyStorageDevice_caseid_101510(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][18]['value'] = 1 #设置报警配置等级1级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_a_time = self.Warninglevel(warning_name="HvPackOverChrgFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][18]['value'] = 2 #设置报警配置等级2级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvPackOverChrgFltPrm"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][18]['value'] = 3 #设置报警配置等级3级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        str_c_time = self.Warninglevel(warning_name="HvPackOverChrgFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[7]["value"][18]['value'] = 0 #设置报警配置等级0级
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["车载储能装置类型过充"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["车载储能装置类型过充"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["车载储能装置类型过充"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["车载储能装置类型过充"])
        
           

    @pytest.mark.full
    def test_gb32960_DataCollect_trigger_CarMode_Normal_UsageMode_Inactive_caseid_101506(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_DataCollect_trigger_CarMode_Normal_UsageMode_Convenience_caseid_101507(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_DataCollect_trigger_CarMode_Normal_UsageMode_Active_caseid_101508(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_DataCollect_trigger_CarMode_Normal_UsageMode_Driving_caseid_101509(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING) 
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_DataCollect_trigger_CarMode_Crash_UsageMode_Inactive_caseid_101498(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_DataCollect_trigger_CarMode_Crash_UsageMode_Convenience_caseid_101499(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH) 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_DataCollect_trigger_CarMode_Crash_UsageMode_Active_caseid_101500(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH) 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_DataCollect_trigger_CarMode_Crash_UsageMode_Driving_caseid_101501(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH) 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING) 
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_DataCollect_trigger_CarMode_Dyno_UsageMode_Inactive_caseid_1903492(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_DataCollect_trigger_CarMode_Dyno_UsageMode_Convenience_caseid_1903495(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO) 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_DataCollect_trigger_CarMode_Dyno_UsageMode_Active_caseid_101504(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO) 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_DataCollect_trigger_CarMode_Dyno_UsageMode_Driving_caseid_101505(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO) 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING) 
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0



    @pytest.mark.full
    def test_gb32960_DataCollect_Precondition_Mismatch_UsageMode_Abandoned_caseid_101492(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(60)
        self.login_or_logout(False)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        logger.info(f'gb_data: {gb_data}')


    @pytest.mark.full
    def test_gb32960_DataCollect_Precondition_Mismatch_CarMode_Transport_caseid_101493(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.TRANSPORT) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(60)
        self.login_or_logout(False)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        logger.info(f'gb_data: {gb_data}')

    @pytest.mark.full
    def test_gb32960_DataCollect_Precondition_Mismatch_CarMode_Factory_caseid_101494(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.FACTORY) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(60)
        self.login_or_logout(False)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        logger.info(f'gb_data: {gb_data}')



    @pytest.mark.full
    def test_gb32960_DataCollect_Precondition_Mismatch_RMSActive_deactivated_caseid_101491(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][0]['value'] = 0
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(60)
        self.login_or_logout(False)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][0]['value'] = 1#打开RMS激活
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入")
        logger.info(f'gb_data: {gb_data}')



    @pytest.mark.full
    def test_gb32960_brake_system_warning_when_usagemode_convenience_driving_caseid_1985669(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()#登入
        logger.info("Start GB32960 report")
        time.sleep(31)     
        # 触发1级报警
        str_a_time = self.Warninglevel(warning_name="EscWarnIndcnReqPrm", warning_level=0) #convenience模式一级报警触发时间
        time.sleep(1)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        time.sleep(5)
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)
        str_b_time = self.Warninglevel(warning_name="EscWarnIndcnReqPrm", warning_level=0) #driving模式一级报警触发时间
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)#登出
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询convenience模式是否产生报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'无报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,0,[])
        #查询driving模式是否产生报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_logout_time, data_type="实时信息上报")
        logger.info(f'一级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,1,["制动系统报警"])
        



    @pytest.mark.full
    def test_gb32960_General_Warning_BrakeSystemWarning_convenience_to_active_4s_caseid_1980659(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()#登入
        logger.info("Start GB32960 report")
        time.sleep(31)     
        # 触发1级报警
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        time.sleep(4)
        str_a_time = self.Warninglevel(warning_name="EscWarnIndcnReqPrm", warning_level=0,time_stamp=30) #active模式一级报警触发时间
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)#登出
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询active模式是否产生报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报")
        logger.info(f'无报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,0,[])
        #查询登出数据      
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_logout_time,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {logout_data}')
        logger.info(f'登入时间: {str_logout_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=t_logout,end_time=t_logout_buffer, data_type="车辆登入")


    @pytest.mark.full
    def test_gb32960_General_Warning_BrakeSystemWarning_convenience_to_driving_4s_caseid_1980657(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()#登入
        logger.info("Start GB32960 report")
        time.sleep(31)     
        # 触发1级报警
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        time.sleep(4)
        str_a_time = self.Warninglevel(warning_name="EscWarnIndcnReqPrm", warning_level=0,time_stamp=30) #active模式一级报警触发时间
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)#登出
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询active模式是否产生报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报")
        logger.info(f'无报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,0,[])
        #查询登出数据      
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_logout_time,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {logout_data}')
        logger.info(f'登入时间: {str_logout_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=t_logout,end_time=t_logout_buffer, data_type="车辆登入")



    @pytest.mark.full
    def test_gb32960_General_Warning_BrakeSystemWarning_convenience_to_active_6s_caseid_1980658(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()#登入
        logger.info("Start GB32960 report")
        time.sleep(31)     
        # 触发1级报警
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        time.sleep(6)
        str_a_time = self.Warninglevel(warning_name="EscWarnIndcnReqPrm", warning_level=0,time_stamp=30) #active模式一级报警触发时间
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)#登出
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询active模式是否产生报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报")
        logger.info(f'无报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["制动系统报警"])
        #查询登出数据      
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_logout_time,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {logout_data}')
        logger.info(f'登入时间: {str_logout_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=t_logout,end_time=t_logout_buffer, data_type="车辆登入")


    @pytest.mark.full
    def test_gb32960_General_Warning_BrakeSystemWarning_convenience_to_driving_6s_caseid_1980656(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()#登入
        logger.info("Start GB32960 report")
        time.sleep(31)     
        # 触发1级报警
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        time.sleep(6)
        str_a_time = self.Warninglevel(warning_name="EscWarnIndcnReqPrm", warning_level=0,time_stamp=30) #active模式一级报警触发时间
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)#登出
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询active模式是否产生报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报")
        logger.info(f'无报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["制动系统报警"])
        #查询登出数据      
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_logout_time,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {logout_data}')
        logger.info(f'登入时间: {str_logout_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=t_logout,end_time=t_logout_buffer, data_type="车辆登入")




    @pytest.mark.full
    def test_gb32960_ParamCfg_RmsLogoutDelayTime_is_0s_caseid_101536(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][4]['value'] = 0
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()#登入
        logger.info("Start GB32960 report")
        time.sleep(61)
        self.soa.notify_OutputState(False)
        logout_time = time.time()
        t_logout = int(logout_time-1)
        t_logout_buffer = int(logout_time+1)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=logout_time,data_type="实时信息上报",cycle_time=10)
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0 

    @pytest.mark.full
    def test_gb32960_ParamCfg_RmsLogoutDelayTime_is_30s_caseid_101535(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][4]['value'] = 30 #设置RmsLogoutDelayTime=30s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()#登入
        logger.info("Start GB32960 report")
        time.sleep(61)
        self.soa.notify_OutputState(False) #登出
        logout_time = time.time() + 30
        t_logout = int(logout_time-1)
        t_logout_buffer = int(logout_time+1)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, logout_time))
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][4]['value'] = 0 #设置RmsLogoutDelayTime=0s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=logout_time,data_type="实时信息上报",cycle_time=10)
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0 

    @pytest.mark.full
    def test_gb32960_ParamCfg_RmsLogoutDelayTime_is_60s_caseid_101534(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][4]['value'] = 60 #设置RmsLogoutDelayTime=60s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5) 
        str_start_time,t_login,t_login_buffer = self.login_or_logout()#登入
        logger.info("Start GB32960 report")
        time.sleep(61)
        self.soa.notify_OutputState(False) #登出
        logout_time = time.time() + 60
        t_logout = int(logout_time-1)
        t_logout_buffer = int(logout_time+1)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, logout_time))
        time.sleep(65)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][4]['value'] = 0 #设置RmsLogoutDelayTime=0s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=logout_time,data_type="实时信息上报",cycle_time=10)
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0 


    @pytest.mark.sanity
    def test_gb32960_Login_logou_serial_number_caseid_1903364(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(10)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(10)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        login_flownum = int(login_data[0]["flowNum"])
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
        logout_flownum = int(logout_data[0]["logoutFlownum"])
        assert login_flownum == logout_flownum #校验登入登出流水号是否一致
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(10)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(10)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        assert login_flownum == int(login_data[0]["flowNum"])-1
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
        assert logout_flownum == int(logout_data[0]["logoutFlownum"])-1
   
    @pytest.mark.sanity
    def test_gb32960_Login_message_data_format_caseid_1903422(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)     
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(10)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(10)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info("车辆登入数据: {0}".format(login_data))
        assert len(login_data) != 0
        assert "dataCollectTime" in login_data[0]
        assert "flowNum" in login_data[0]
        assert "iccid" in login_data[0]
        assert "systemNum" in login_data[0]
        assert "codeLength" in login_data[0]
        assert "systemCode" in login_data[0]
        
        
    @pytest.mark.sanity
    def test_gb32960_Logout_message_data_format_caseid_1903458(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)     
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(10)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(10)
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        logger.info("车辆登出数据: {0}".format(logout_data))
        assert len(logout_data) != 0
        assert "logoutTime" in logout_data[0]
        assert "logoutFlownum" in logout_data[0]
     
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningPeriod_is_0s_caseid_1903573(self, ecu):
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][6]['value'] = 0 #设置WarningPeriod=0s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvlsoFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["绝缘报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["绝缘报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["绝缘报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["绝缘报警"])

        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningPeriod_is_30s_interval_30s_caseid_100098(self, ecu):
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][6]['value'] = 30 #设置WarningPeriod=30s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        str_a_time = time.time()   #一级报警触发时间
        for i in range(29):
            self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=1,time_stamp=1)   
        for i in range(30):
            self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=0,time_stamp=1) #无报警  
        for i in range(29):
            self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=2,time_stamp=1) #二级报警触发时间 
        for i in range(30):
            self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=0,time_stamp=1) #无报警 
        for i in range(29):
            self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=3,time_stamp=1) #三级报警触发时间 
        for i in range(30):
            self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=0,time_stamp=1) #无报警
        str_g_time = time.time()   
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][6]['value'] = 0 #设置WarningPeriod=0s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询是否存在报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_g_time, data_type="实时信息上报")
        logger.info(f'无报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_g_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,0,[])

    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningPeriod_is_60s_interval_60s_caseid_101529(self, ecu):
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][6]['value'] = 60 #设置WarningPeriod=60s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发1级报警
        str_a_time = time.time()   #一级报警触发时间
        for i in range(59):
            self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=1,time_stamp=1)  
        for i in range(60):
            self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=0,time_stamp=1) #无报警 
        for i in range(59):
            self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=2,time_stamp=1) #二级报警触发时间
        for i in range(60):
            self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=0,time_stamp=1) #无报警
        for i in range(59):
            self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=3,time_stamp=1) #三级报警触发时间 
        for i in range(60):
            self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=0,time_stamp=1) #无报警
        str_g_time = time.time()   
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][6]['value'] = 0 #设置WarningPeriod=0s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询是否存在报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_g_time, data_type="实时信息上报")
        logger.info(f'无报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_g_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,0,[])
       
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_RmsUploadUrl_is_GB_server_caseid_101540(self, ecu):
        self.gb_config = gb_config_data
        self.gb_config[5]["value"] = 1
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)     
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
        
        
    @pytest.mark.full
    def test_gb32960_LoginLogout_successfully_with_RMSLoginDelayTime_1s_caseid_101470(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][3]['value'] = 1
        self.gb_config[6]["value"][4]['value'] = 1
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time())) #修改配置登入登出延迟为1s
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        self.soa.notify_OutputState() #登入
        login_time = time.time() + 1
        t_login = int(login_time-1)
        t_login_buffer = int(login_time+1)
        logger.info("Start GB32960 report")
        time.sleep(10)
        self.soa.notify_OutputState(False) #登出
        logout_time = time.time() + 1
        t_logout = int(logout_time-1)
        t_logout_buffer = int(logout_time+1)
        logger.info("Stop GB32960 report")
        time.sleep(10)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][3]['value'] = 0
        self.gb_config[6]["value"][4]['value'] = 0
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time())) #修改配置登入登出延迟为1s
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        assert len(login_data) != 0
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        logger.info(f'登出数据: {logout_data}')
        assert len(logout_data) != 0
        
        
    @pytest.mark.full
    def test_gb32960_LoginLogout_successfully_with_RMSLoginDelayTime_10s_caseid_101469(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][3]['value'] = 10
        self.gb_config[6]["value"][4]['value'] = 10 
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time())) #修改配置登入登出延迟为10s
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        self.soa.notify_OutputState() #登入
        login_time = time.time() + 10
        t_login = int(login_time-1)
        t_login_buffer = int(login_time+1)
        logger.info("Start GB32960 report")
        time.sleep(20)
        self.soa.notify_OutputState(False) #登出
        logout_time = time.time() + 10
        t_logout = int(logout_time-1)
        t_logout_buffer = int(logout_time+1)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][3]['value'] = 0
        self.gb_config[6]["value"][4]['value'] = 0
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time())) #修改配置登入登出延迟为0s
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        assert len(login_data) != 0
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        logger.info(f'登出数据: {logout_data}')
        assert len(logout_data) != 0  
        
        
    @pytest.mark.full
    def test_gb32960_LoginLogout_successfully_with_RMSLoginDelayTime_30s_caseid_101468(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][3]['value'] = 30
        self.gb_config[6]["value"][4]['value'] = 30
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time())) #修改配置登入登出延迟为30s
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        self.soa.notify_OutputState() #登入
        login_time = time.time() + 30
        t_login = int(login_time-1)
        t_login_buffer = int(login_time+1)
        logger.info("Start GB32960 report")
        time.sleep(60)
        self.soa.notify_OutputState(False) #登出
        logout_time = time.time() + 30
        t_logout = int(logout_time-1)
        t_logout_buffer = int(logout_time+1)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][3]['value'] = 0
        self.gb_config[6]["value"][4]['value'] = 0
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time())) #修改配置登入登出延迟为0s
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        assert len(login_data) != 0
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        logger.info(f'登出数据: {logout_data}')
        assert len(logout_data) != 0  
        
    @pytest.mark.full
    def test_gb32960_LoginLogout_successfully_with_RMSLoginDelayTime_60s_caseid_101467(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][3]['value'] = 60
        self.gb_config[6]["value"][4]['value'] = 60
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time())) #修改配置登入登出延迟为60s
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        self.soa.notify_OutputState() #登入
        login_time = time.time() + 60
        t_login = int(login_time-1)
        t_login_buffer = int(login_time+1)
        logger.info("Start GB32960 report")
        time.sleep(90)
        self.soa.notify_OutputState(False) #登出
        logout_time = time.time() + 60
        t_logout = int(logout_time-1)
        t_logout_buffer = int(logout_time+1)
        logger.info("Stop GB32960 report")
        time.sleep(90)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][3]['value'] = 0
        self.gb_config[6]["value"][4]['value'] = 0
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time())) #修改配置登入登出延迟为0s
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        assert len(login_data) != 0
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        logger.info(f'登出数据: {logout_data}')
        assert len(logout_data) != 0  
        
        
    @pytest.mark.full
    def test_gb32960_General_Warning_HighVoltageInterlock_caseid_100081(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(1)     
        # 触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvilFltPrm", warning_level=1) #一级报警触发时间
        b_time = time.time()
        str_b_time = int(b_time)
        time.sleep(2)    
        # #触发2级报警
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        str_c_time = self.Warninglevel(warning_name="HvilFltPrm", warning_level=1)#二级报警触发时间
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["高压互锁状态报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_logout_time, data_type="实时信息上报")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_c_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["高压互锁状态报警"])

 
    @pytest.mark.full
    def test_gb32960_General_Warning_2_divided_level3_alarms_caseid_101448(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout() #登入
        logger.info("Start GB32960 report") 
        time.sleep(31)
        str_a_time = self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=3)#绝缘三级报警触发时间 
        self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=0,time_stamp=1) #恢复报警)
        time.sleep(40) 
        str_c_time = self.Warninglevel(warning_name="HvSocHiFltPrm", warning_level=3)#soc过高三级报警触发时间
        time.sleep(60)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询第一个三级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_a_time+29, data_type="实时信息上报")
        logger.info(f'绝缘报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_a_time+29, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(a_gb_data,3,["绝缘报警"])
        #查询第一个三级报警补发数据
        re1_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time-30, end_time=str_a_time-1, data_type="补发信息上报")
        logger.info(f'补发数据: {re1_gb_data}')
        self.tsp.check_gb_data_cycle(re1_gb_data,start_time=str_a_time-30, end_time=str_a_time-1, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(re1_gb_data,0,[])       
        #查询第二个三级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_c_time+29, data_type="实时信息上报")
        logger.info(f'SOC过高报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_c_time, end_time=str_c_time+29, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(b_gb_data,3,["SOC过高报警"]) 
        # 查询第二个三级报警的补发数据
        re2_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time-30, end_time=str_c_time-1, data_type="补发信息上报")
        logger.info(f'补发数据: {re2_gb_data}')
        self.tsp.check_gb_data_cycle(re2_gb_data,start_time=str_c_time-30, end_time=str_c_time, data_type="补发信息上报" ,cycle_time=1)
        check_gb_data_extremumData(re2_gb_data,0,[]) 
      
    
    @pytest.mark.full
    def test_gb32960_Vehicle_estabilish_connection_with_GBserver_caseid_101466(self, ecu):
        self.gb_config = gb_config_data
        self.gb_config[5]["value"] = 1
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)     
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
    
    
    
    @pytest.mark.full
    def test_gb32960_DataCollect_exit_by_HvSysRlySts_OpenAndReqActvDcha_caseid_101495(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout() #登入
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False) #登出
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
    
    
    @pytest.mark.full
    def test_gb32960_DataCollect_exit_by_HvSysRlySts_Open_caseid_1903503(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout() #触发登入
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False) #触发登出
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
    
    
    
    @pytest.mark.full
    def test_gb32960_General_Warning_2_joint_level3_alarms_caseid_101447(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout() #登入
        logger.info("Start GB32960 report") 
        time.sleep(31)
        str_a_time = self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=3,time_stamp=20)#绝缘三级报警触发时间 
        str_b_time = self.Warninglevel(warning_name="HvSocHiFltPrm", warning_level=3)#soc过高三级报警触发时间
        time.sleep(60)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询第一个三级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_a_time+19, data_type="实时信息上报")
        logger.info(f'绝缘报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_a_time+19, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(a_gb_data[1:],3,["绝缘报警"]) #为了避免出现例如：14:01:00.999s发送的报警数据，但实际14:01:01才有第一包报警数据，所以这里从第2个开始检查
        #查询第二个三级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_b_time+29, data_type="实时信息上报")
        logger.info(f'SOC过高报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_b_time+29, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(b_gb_data[1:],3,["SOC过高报警"])   
        # 查询第1个三级报警的补发数据
        re1_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time-30, end_time=str_a_time-1, data_type="补发信息上报")
        logger.info(f'补发数据: {re1_gb_data}')
        self.tsp.check_gb_data_cycle(re1_gb_data,start_time=str_a_time-30, end_time=str_a_time-1, data_type="补发信息上报" ,cycle_time=1)
        check_gb_data_extremumData(re1_gb_data,0,[]) 
        #查询第二个三级报警30后的实时数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time+30, end_time=str_logout_time, data_type="实时信息上报")
        logger.info(f'实时数据: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time+30, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)



    @pytest.mark.full
    def test_gb32960_DataCollect_exit_by_HvSysRlySts_KeepSt_caseid_101496(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout() #触发登入
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False) #触发登出
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
    
    
    
    @pytest.mark.full
    def test_gb32960_ParamCfg_SupplementPeriod_is_2s_caseid_101542(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][2]['value'] = 2 #设置补发周期为2s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        str_start_time,t_login,t_login_buffer = self.login_or_logout()   
        logger.info("Start GB32960 report")
        time.sleep(10)
        self.ssh.set_airplane_mode(isOn.On) #设置飞行模式
        a_time=time.time()
        str_a_time = int(a_time)
        time.sleep(60)
        self.ssh.set_airplane_mode(isOn.Off) #取消飞行模式
        time.sleep(120)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][2]['value'] = 4 #结束设置补发周期为默认值4s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        reissue_gb_data=self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_a_time+60, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.check_gb_reissuegbdata_cycle(reissue_gb_data,cycle_time=4) # 验证断网期间补发数据上报周期为4s
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0



    @pytest.mark.full
    def test_gb32960_ParamCfg_SupplementPeriod_is_4s_caseid_101439(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][2]['value'] = 4 #设置补发周期为4s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        str_start_time,t_login,t_login_buffer = self.login_or_logout()   
        logger.info("Start GB32960 report")
        time.sleep(10)
        self.ssh.set_airplane_mode(isOn.On) #设置飞行模式
        a_time=time.time()
        str_a_time = int(a_time)
        time.sleep(60)
        self.ssh.set_airplane_mode(isOn.Off) #取消飞行模式
        time.sleep(120)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(10)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        reissue_gb_data=self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_a_time+60, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.check_gb_reissuegbdata_cycle(reissue_gb_data,cycle_time=4)  # 验证断网期间补发数据上报周期为4s
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
        

    @pytest.mark.full
    def test_gb32960_ParamCfg_SupplementPeriod_is_10s_caseid_101543(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][2]['value'] = 10 #设置补发周期为10s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        str_start_time,t_login,t_login_buffer = self.login_or_logout()   
        logger.info("Start GB32960 report")
        time.sleep(10)
        self.ssh.set_airplane_mode(isOn.On) #设置飞行模式
        a_time=time.time()
        str_a_time = int(a_time)
        time.sleep(60)
        self.ssh.set_airplane_mode(isOn.Off) #取消飞行模式
        time.sleep(120)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][2]['value'] = 4 #结束设置补发周期为默认值4s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        reissue_gb_data=self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_a_time+60, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.check_gb_reissuegbdata_cycle(reissue_gb_data,cycle_time=10) # 验证断网期间补发数据上报周期为10s
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0
        

    @pytest.mark.full
    def test_gb32960_ParamCfg_SupplementPeriod_is_30s_caseid_101541(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][2]['value'] = 30  #设置补发周期为30s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5) 
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)   
        str_start_time,t_login,t_login_buffer = self.login_or_logout()   
        logger.info("Start GB32960 report")
        time.sleep(10)
        self.ssh.set_airplane_mode(isOn.On) #设置飞行模式
        a_time=time.time()
        str_a_time = int(a_time)
        time.sleep(120)
        self.ssh.set_airplane_mode(isOn.Off) #取消飞行模式
        time.sleep(180)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][2]['value'] = 4 #结束设置补发周期为默认值4s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        assert len(login_data) != 0
        reissue_gb_data=self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_a_time+120, data_type="补发信息上报")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.check_gb_reissuegbdata_cycle(reissue_gb_data,cycle_time=30) # 验证断网期间补发数据上报周期为30s
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出")
        assert len(logout_data) != 0


    @pytest.mark.smoke
    def test_gb32960_Realtime_message_data_format_caseid_1903160(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)     
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(20)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info("车辆登入数据: {0}".format(login_data))
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        logger.info("车辆实时数据: {0}".format(a_data))
        assert len(a_data) != 0
        assert "dataCollectTime" in a_data[0]
        assert "vehicleData" in a_data[0]
        assert "driveMotorData" in a_data[0]
        assert "vehiclePositionData" in a_data[0]
        assert "extremumData" in a_data[0]
        assert "voltageData" in a_data[0]
        assert "temperatureData" in a_data[0]
    
        
    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningPeriod_is_30s_interval_31s_caseid_100095(self, ecu):
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][6]['value'] = 30 #设置WarningPeriod=30s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(30)     
        str_a_time = self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=1,time_stamp=31)
        time.sleep(60)  
        str_c_time = time.time() 
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][6]['value'] = 0 #设置WarningPeriod=0s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询是否存在报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_a_time+30, data_type="实时信息上报")
        logger.info(f'无报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_a_time+30, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,0,[])
        #查询1级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time+31, end_time=str_c_time, data_type="实时信息上报")
        logger.info(f'绝缘一级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_a_time+31, end_time=str_c_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,1,["绝缘报警"])


    @pytest.mark.full
    def test_gb32960_ParamCfg_WarningPeriod_is_60s_interval_61s_caseid_101528(self, ecu):
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][6]['value'] = 60 #设置WarningPeriod=60s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        str_a_time = self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=1,time_stamp=61)
        time.sleep(60)  
        str_c_time = time.time() 
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][6]['value'] = 0 #设置WarningPeriod=0s
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询是否存在报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_a_time+60, data_type="实时信息上报")
        logger.info(f'无报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_a_time+60, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,0,[])
        #查询1级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time+61, end_time=str_c_time, data_type="实时信息上报")
        logger.info(f'绝缘一级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_a_time+61, end_time=str_c_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,1,["绝缘报警"])
        

    @pytest.mark.sanity
    def test_gb32960_Extreme_data_caseid_101446(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)     
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(20)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入")
        logger.info("车辆登入数据: {0}".format(login_data))
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报")
        logger.info("车辆实时数据: {0}".format(a_data))
        assert len(a_data) != 0
        assert "dataCollectTime" in a_data[0]
        assert "extremumData" in a_data[0]
        assert "voltageData" in a_data[0]
        assert "temperatureData" in a_data[0]   
        








@allure.feature("互联服务/数据上报/GB32960")
@allure.story("转发模式数据上报")
class TestForwardmodeGB32960(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "GB32960Service_server",
                         "HighVoltageService_server", "VehicleTimeService_server",
                         "CarConfigService_server","ConfigMasterService_server"])
        self.mix.start_get_request_and_send_response_to_tcam_thread(["VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "GB32960Service_server",
                         "HighVoltageService_server", "VehicleTimeService_server",
                         "CarConfigService_server"], {'GetVIN':{'vin':self.tb_config['vin']}})
        self.gb_config = gb_config_data
        self.gb_config[5]["value"] = 0
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5)
        self.ssh.tcam_ssh.exec("reboot -f")
        time.sleep(300)

        sleep(2)
        self.vin = self.tb_config["vin"]
        # self.soa.check_GetVIN_req_and_feedback_resp(vin=self.vin,timeout=30)
    

    def before_each_func(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.NORMAL)
        self.soa.s2s_set_car_mode(car_mode=CarMode.NORMAL)
        self.soa.s2s_set_mntnmode(mntnmode=False)
        self.soa.notify_OutputState(on=False)
        self.soa.notify_HVThermalOutOfControl()
        self.soa.notify_NotifyHvBatteryCode()
        self.soa.notify_NotifyVIN(vin=self.tb_config["vin"])
        self.soa.notify_VehicleTimeInfo(sync_sts=TimeSyncSts.NTP)

        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))

    def after_each_func(self, ecu):
        self.soa.notify_OutputState(on=False)
        self.soa.s2s_set_car_mode(car_mode=CarMode.NORMAL)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))

    def after_class(self, ecu):
        self.mix.stop_get_request_and_send_response_to_tcam_thread()
        pass

    def login_or_logout(self,login_flage:bool=True, buffer:int=1):
        if login_flage:
            self.soa.notify_OutputState()
        else:
            self.soa.notify_OutputState(on=False)
        login_time = time.time()
        logger.info("Start GB32960 report")
        t_login = int(login_time-buffer)
        t_login_buffer = int(login_time+buffer)
        return login_time,t_login,t_login_buffer
    
    
    def Warninglevel(self, warning_name:str='HvPackUUnderFltPrm', warning_level:int=1,time_stamp:int=30):
        self.soa.notify_GB32960Data(gb32960_data) 
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"][warning_name] = warning_level
        self.soa.notify_GB32960Data(gb_data) 
        str_a_time = int(time.time())#一级报警触发时间
        time.sleep(time_stamp)
        return str_a_time

    def check_gb_reissuegbdata_cycle(self, gb_data_list:list,cycle_time):
        s_time = self.tsp.datetime_to_timestamp(gb_data_list[0]['updateTime'])
        for data in gb_data_list[1:]:
            updateTime = self.tsp.datetime_to_timestamp(data['updateTime'])
            logger.info("报文时间戳： {0}".format(updateTime))
            assert  updateTime - s_time <= cycle_time
            s_time = updateTime


    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_successfully_when_CarMode_Normal_UsageMode_Inactive_caseid_101386(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_successfully_when_CarMode_Normal_UsageMode_Convenience_caseid_101387(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_successfully_when_CarMode_Normal_UsageMode_Active_caseid_101388(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_successfully_when_CarMode_Normal_UsageMode_Driving_caseid_101389(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0



    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_successfully_when_CarMode_Crash_UsageMode_Inactive_caseid_101379(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.s2s_set_mntnmode(mntnmode=False)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_successfully_when_CarMode_Crash_UsageMode_Convenience_caseid_101380(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.s2s_set_mntnmode(mntnmode=False)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_successfully_when_CarMode_Crash_UsageMode_Active_caseid_101381(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.s2s_set_mntnmode(mntnmode=False)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_successfully_when_CarMode_Crash_UsageMode_Driving_caseid_100091(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_successfully_when_CarMode_Dyno_UsageMode_Inactive_caseid_101382(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.s2s_set_mntnmode(mntnmode=False)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_successfully_when_CarMode_Dyno_UsageMode_Convenience_caseid_101383(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.s2s_set_mntnmode(mntnmode=False)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_successfully_when_CarMode_Dyno_UsageMode_Active_caseid_101384(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.s2s_set_mntnmode(mntnmode=False)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_successfully_when_CarMode_Dyno_UsageMode_Driving_caseid_101385(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.s2s_set_mntnmode(mntnmode=False)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0



    @pytest.mark.full
    def test_gb32960_Forward_General_Warning_OverVoltageAlarmofBatteryCell_caseid_100062(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvCellUUnderFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellUUnderFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvCellUUnderFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["单体电池欠压报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["单体电池欠压报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["单体电池欠压报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",data_mode="转发模式")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["单体电池欠压报警"])


    @pytest.mark.full
    def test_gb32960_Forward_General_Warning_OverchargeAlarmofEnergyStorageDevice_caseid_100063(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvPackOverChrgFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvPackOverChrgFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvPackOverChrgFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["车载储能装置类型过充"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["车载储能装置类型过充"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["车载储能装置类型过充"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",data_mode="转发模式")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["车载储能装置类型过充"])



    @pytest.mark.full
    def test_gb32960_Forward_General_Warning_OverHighSOCAlarm_caseid_100064(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvSocHiFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvSocHiFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvSocHiFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["SOC过高报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["SOC过高报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["SOC过高报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",data_mode="转发模式")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["SOC过高报警"])


    @pytest.mark.full
    def test_gb32960_Forward_General_Warning_OverVoltageAlarmofEnergyStorageDevice_caseid_100068(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvPackUOverFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvPackUOverFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvPackUOverFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["车载储能装置类型过压报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["车载储能装置类型过压报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["车载储能装置类型过压报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",data_mode="转发模式")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["车载储能装置类型过压报警"])


    @pytest.mark.full
    def test_gb32960_Forward_General_Warning_SOCJumpAlarm_caseid_100069(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvSocHopFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvSocHopFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvSocHopFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["SOC跳变报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["SOC跳变报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["SOC跳变报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",data_mode="转发模式")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["SOC跳变报警"])


    @pytest.mark.full
    def test_gb32960_Forward_General_Warning_DCDCTemperatureAlarm_caseid_100072(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="FltTDcDcPrm", warning_level=1) #一级报警触发时间
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,1,["DC-DC温度报警"])


    @pytest.mark.full
    def test_gb32960_Forward_General_Warning_InsulationAlarm_caseid_100082(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvlsoFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvlsoFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["绝缘报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["绝缘报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["绝缘报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",data_mode="转发模式")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["绝缘报警"])



    @pytest.mark.full
    def test_gb32960_Forward_General_Warning_PoorBatteryCellConsistencyAlarm_caseid_100083(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvCellUDifFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellUDifFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvCellUDifFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["电池单体一致性差报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["电池单体一致性差报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["电池单体一致性差报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",data_mode="转发模式")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["电池单体一致性差报警"])



    @pytest.mark.full
    def test_gb32960_Forward_General_Warning_RechargeableEnergyStorageSystemSismatchAlarm_caseid_100086(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发2级报警
        str_a_time = self.Warninglevel(warning_name="HvBattMismatchFltPrm", warning_level=1) #二级报警触发时间
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["可充电储能系统不匹配报警"])


    @pytest.mark.full
    def test_gb32960_Forward_General_Warning_DriveMotorTemperatureAlarm_caseid_100089(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发2级报警
        str_a_time = self.Warninglevel(warning_name="IemGenericMotTAlrmStPrm", warning_level=1) #二级报警触发时间
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["驱动电机温度报警"])


    @pytest.mark.full
    def test_gb32960_Forward_General_Warning_HighVoltageInterlock_caseid_100092(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(1)     
        # 触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvilFltPrm", warning_level=1) #一级报警触发时间
        b_time = time.time()
        str_b_time = int(b_time)
        time.sleep(2)    
        # #触发2级报警
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        str_c_time = self.Warninglevel(warning_name="HvilFltPrm", warning_level=1)#二级报警触发时间
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["高压互锁状态报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_c_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["高压互锁状态报警"])


    @pytest.mark.sanity
    def test_gb32960_Forward_General_Warning_DriveMotorControllerTemperatureAlarm_caseid_101358(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发2级报警
        str_a_time = self.Warninglevel(warning_name="IemGenericInvrtTAlrmStPrm", warning_level=1) #二级报警触发时间
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["驱动电机控制器温度报警"])


    @pytest.mark.sanity
    def test_Forward_General_Warning_DCDCStatusAlarm_caseid_101359(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        #触发2级报警
        str_a_time = self.Warninglevel(warning_name="FltElecDcDcPrm", warning_level=1) #2级报警触发时间
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        time.sleep(30)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_a_time, end_time=str_logout_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["DC-DC状态报警"])


    @pytest.mark.sanity
    def test_gb32960_Forward_General_Warning_UnderVoltageAlarmofBatteryCell_caseid_101361(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvCellUUnderFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellUUnderFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvCellUUnderFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["单体电池欠压报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["单体电池欠压报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["单体电池欠压报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",data_mode="转发模式")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["单体电池欠压报警"])


    @pytest.mark.sanity
    def test_gb32960_Forward_General_Warning_TemperatureDifferenceAlarm_caseid_101365(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvCellTDifFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellTDifFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvCellTDifFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["温度差异报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["温度差异报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["温度差异报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",data_mode="转发模式")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["温度差异报警"])



    @pytest.mark.smoke
    def test_gb32960_Forward_General_Warning_BrakeSystemWarning_caseid_1903768(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        # 触发1级报警
        str_a_time = self.Warninglevel(warning_name="EscWarnIndcnReqPrm", warning_level=0) #一级报警触发时间
        time.sleep(1)
        # #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        gb_data["WarningData"]["AbsWarnIndcnReqPrm"] = 0
        gb_data["WarningData"]["BrkSysWarnIndcnReqPrm"] = 0
        gb_data["WarningData"]["BrkSysWarnIndcnReqSecPrm"] = 0    
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        # #触发3级报警
        str_c_time = self.Warninglevel(warning_name="BrkWarnIndcnReqPrm", warning_level=0)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["制动系统报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["制动系统报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["制动系统报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",data_mode="转发模式")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["制动系统报警"])
     


    @pytest.mark.sanity
    def test_gb32960_Forward_General_Warning_DriveMotorTemperatureAlarm_caseid_1903852(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvCellTOverFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvCellTOverFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvCellTOverFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["电池高温报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["电池高温报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["电池高温报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",data_mode="转发模式")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["电池高温报警"])


    @pytest.mark.sanity
    def test_gb32960_Forward_General_Warning_LowSOCAlarm_caseid_1903853(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvSocLoFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvSocLoFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvSocLoFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["SOC低报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["SOC低报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["SOC低报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",data_mode="转发模式")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["SOC低报警"])



    @pytest.mark.sanity
    def test_gb32960_Forward_General_Warning_UnderVoltageAlarmofEnergyStorageDevice_caseid_1903870(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(21)     
        #触发1级报警
        str_a_time = self.Warninglevel(warning_name="HvPackUUnderFltPrm", warning_level=1) #一级报警触发时间
        #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["WarningData"]["HvPackUUnderFltPrm"] = 2
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        #触发3级报警
        str_c_time = self.Warninglevel(warning_name="HvPackUUnderFltPrm", warning_level=3)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        # str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(60)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["车载储能装置类型欠压报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["车载储能装置类型欠压报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["车载储能装置类型欠压报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",data_mode="转发模式")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["车载储能装置类型欠压报警"])



    @pytest.mark.sanity
    def test_gb32960_Forward_caseid_100973(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(31)     
        # 触发1级报警
        str_a_time = self.Warninglevel(warning_name="EscWarnIndcnReqPrm", warning_level=0) #一级报警触发时间
        time.sleep(1)
        # #触发2级报警
        gb_data = copy.deepcopy(gb32960_data)
        gb_data["VehStatus"]["VehSts"] = 1
        gb_data["WarningData"]["AbsWarnIndcnReqPrm"] = 0
        gb_data["WarningData"]["BrkSysWarnIndcnReqPrm"] = 0
        gb_data["WarningData"]["BrkSysWarnIndcnReqSecPrm"] = 0    
        self.soa.notify_GB32960Data(gb_data) 
        b_time = time.time()
        str_b_time = int(b_time)#二级报警触发时间
        time.sleep(5)
        re_start_time = time.time()
        str_re_start_time = int(re_start_time)#30s补发开始时间
        time.sleep(25)
        e_time = time.time()
        str_e_time = int(e_time)
        time.sleep(5)         
        # #触发3级报警
        str_c_time = self.Warninglevel(warning_name="BrkWarnIndcnReqPrm", warning_level=0)#三级报警触发时间
        d_time = time.time()
        str_d_time = int(d_time)
        time.sleep(30)
        self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        time.sleep(30)
        #查询登入数据
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'登入数据: {login_data}')
        logger.info(f'登入时间: {str_start_time}')
        self.tsp.check_gb_data_cycle(login_data,start_time=str_start_time,end_time=t_login_buffer, data_type="车辆登入")
        #查询1级报警数据
        a_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'一级报警: {a_gb_data}')
        self.tsp.check_gb_data_cycle(a_gb_data,start_time=str_a_time, end_time=str_b_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(a_gb_data,1,["制动系统报警"])
        #查询2级报警数据
        b_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'二级报警: {b_gb_data}')
        self.tsp.check_gb_data_cycle(b_gb_data,start_time=str_b_time, end_time=str_e_time, data_type="实时信息上报",cycle_time=10)
        check_gb_data_extremumData(b_gb_data,2,["制动系统报警"])
        #查询3级报警数据
        c_gb_data =self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",data_mode="转发模式")
        logger.info(f'三级报警: {c_gb_data}')
        self.tsp.check_gb_data_cycle(c_gb_data,start_time=str_c_time, end_time=str_d_time, data_type="实时信息上报",cycle_time=1)
        check_gb_data_extremumData(c_gb_data,3,["制动系统报警"])
        #查询3级报警前30s补发数据
        reissue_gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",data_mode="转发模式")
        logger.info(f'补发数据: {reissue_gb_data}')
        self.tsp.check_gb_data_cycle(reissue_gb_data,start_time=str_re_start_time, end_time=str_c_time, data_type="补发信息上报",cycle_time=1)
        check_gb_data_extremumData(reissue_gb_data,2,["制动系统报警"])



    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_Precondition_Mismatch_UsageMode_Abandoned_caseid_101376(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(30)
        self.login_or_logout(False)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入",data_mode="转发模式")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'gb_data: {gb_data}')

    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_Precondition_Mismatch_CarMode_Transport_caseid_101377(self, ecu):
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.TRANSPORT)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(30)
        self.login_or_logout(False)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入",data_mode="转发模式")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'gb_data: {gb_data}')


    @pytest.mark.full
    def test_gb32960_Forward_LoginLogout_Precondition_Mismatch_CarMode_Factory_caseid_101378(self, ecu):
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.FACTORY)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(30)
        self.login_or_logout(False)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入",data_mode="转发模式")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'gb_data: {gb_data}')


    @pytest.mark.full
    def test_gb32960_Forward_dormanc_awakenserial_number_caseid_100250(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(30)
        self.login_or_logout(False)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(30)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入",data_mode="转发模式")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'gb_data: {gb_data}')


    @pytest.mark.full
    def test_gb32960_Forward_DataCollect_trigger_CarMode_Normal_UsageMode_Inactive_caseid_1903871(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.sanity
    def test_gb32960_Forward_DataCollect_trigger_CarMode_Normal_UsageMode_Convenience_caseid_101408(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_Forward_DataCollect_trigger_CarMode_Normal_UsageMode_Active_caseid_101409(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_DataCollect_trigger_CarMode_Normal_UsageMode_Driving_caseid_1965244(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_DataCollect_trigger_CarMode_Crash_UsageMode_Inactive_caseid_101399(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_Forward_DataCollect_trigger_CarMode_Crash_UsageMode_Convenience_caseid_101400(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_Forward_DataCollect_trigger_CarMode_Crash_UsageMode_Active_caseid_101401(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.5)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_DataCollect_trigger_CarMode_Crash_UsageMode_Driving_caseid_101402(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.CRASH)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.5)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0



    @pytest.mark.full
    def test_gb32960_Forward_DataCollect_trigger_CarMode_Dyno_UsageMode_Inactive_caseid_101403(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.5)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0
        

    @pytest.mark.full
    def test_gb32960_Forward_DataCollect_trigger_CarMode_Dyno_UsageMode_Convenience_caseid_101404(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.5)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_DataCollect_trigger_CarMode_Dyno_UsageMode_Active_caseid_101405(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.5)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_DataCollect_trigger_CarMode_Dyno_UsageMode_Driving_caseid_101406(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_car_mode_to_tcam(car_mode=CarMode.DYNO)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.5)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout()
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False)
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0


    @pytest.mark.full
    def test_gb32960_Forward_DataCollect_exit_by_HvSysRlySts_Open_caseid_101398_101397_101396(self, ecu):
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data)
        str_start_time,t_login,t_login_buffer = self.login_or_logout() #触发登入
        logger.info("Start GB32960 report")
        time.sleep(61)
        str_logout_time,t_logout,t_logout_buffer =self.login_or_logout(False) #触发登出
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        login_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_login,end_time=t_login_buffer, data_type="车辆登入",data_mode="转发模式")
        assert len(login_data) != 0
        a_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=login_data[0]["dataCollectTime"], end_time=str_logout_time, data_type="实时信息上报",data_mode="转发模式")
        self.tsp.check_gb_data_cycle(a_data,start_time=login_data[0]["dataCollectTime"],end_time=str_logout_time,data_type="实时信息上报")
        logout_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=t_logout, end_time=t_logout_buffer, data_type="车辆登出",data_mode="转发模式")
        assert len(logout_data) != 0

    @pytest.mark.full
    def test_gb32960_Forward_DataCollect_Precondition_Mismatch_RMSActive_deactivated_caseid_101392(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.gb_config = gb_config_data
        self.gb_config[6]["value"][0]['value'] = 0
        self.soa.notify_ConfigDataNotify(config_data=json.dumps(self.gb_config),publish_id=int(time.time()))
        time.sleep(5)
        gb_data = copy.deepcopy(gb32960_data)
        self.soa.notify_GB32960Data(gb_data) 
        str_start_time = self.login_or_logout()[0]
        logger.info("Start GB32960 report")
        time.sleep(60)
        self.login_or_logout(False)
        str_logout_time = self.login_or_logout(False)[0]
        logger.info("Stop GB32960 report")
        logger.info("开始上报时间：{0}, 结束上报时间: {1}".format(str_start_time, str_logout_time))
        time.sleep(20)
        assert not self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入",data_mode="转发模式")
        gb_data = self.tsp.get_gb32960data_direct(vin=self.vin, start_time=str_start_time, end_time=str_logout_time, data_type="车辆登入",data_mode="转发模式")
        logger.info(f'gb_data: {gb_data}')