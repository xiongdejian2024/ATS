#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@Description: 日志管理测试用例
@Examples:
"""
import copy
import re
import os
import string
import sys
import uuid
import pytest
import requests
import ast
from jsonpath_ng import parse as ng_parse

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import (
    send_can_wake_data,
    get_signal_value_from_pdu_data2,
    partner_client_method_request,
)
from xat_ecu.legacy.soa_partner.src.Operator import SOAOperator
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_ecu.legacy.soa_partner.src import partner_client
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.interfaces.dp1.log_trigger_handler import (
    log_bgm_config_data
)
from xat_cases.legacy.soa.case_helper.gnss_server import GNSSServiceServer
from xat_ecu.legacy.soa_partner.src.base_partner import *

from xat_ecu.legacy.common.data_type_handing import DataTypeHanding, int_to_4_bytes_list
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.api.config_center.configfile_utils import *
from xat_ecu.legacy.sdk.tcp_framework.tcp_communicate import *
from xat_ecu.legacy.driver.ssh_interface import command_send
from collections import defaultdict

CONFIGMASTER_SERVICE_CLIENT = "ConfigMasterService_client"

@allure.feature("MPU软件平台")
@allure.story("日志管理")
class TestLogManage(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # self.mix.log_special_obj.start_v2t_monitor()
        # self.mix.log_special_obj.config_trigger_to_valid(trigger_type='bgm_remote', own_data=copy.deepcopy(log_bgm_config_data), source=1)
        # self.mix.log_special_obj.stop_v2t_monitor()
        self.vid = self.tc_config['vid']
        self.soa.update(
            [
                ("RemoteLogManagerService", "client", "BGM_RemoteLogManagerService"),
                ("ConfigMasterService", "client"),
                # ("V2TRoutingForwarder", "client", "V2TLogTCAMForwarder"),
                ("V2TRoutingForwarder", "client", "V2TLogBGMForwarder"),
                ("LogMasterService", "client"),
            ]
        )
        # self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)


    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info(f"case开始运行{'=' * 70}")
        self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
        self.ssh.type_commands(DeviceName.TCAM, 'ping -I rmnet_data1 www.baidu.com -c 4')
        # self.io.hazard_light_close()
        # self.io.io.charge_lid_close()
        # self.io.io.brake_up()
        # self.io.io.hood_door2_open()
        # self.io.io.drvr_door_outswitch_unpressed()
        # self.io.io.drvr_door_close()
        # self.mix.set_usage_mode(UsageMode.INACTIVE)
        # self.mix.set_car_mode(CarMode.NORMAL)


    def after_each_func(self, ecu):
        self.socket.tcp_client.close()
        logger.info(f"case结束运行{'=' * 70}")
        self.io.bgm_diag_line_up()
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        sleep(3)
        # 关闭飞行模式
        self.ssh.set_airplane_mode(sts=isOn.Off)
        super().after_each_func(ecu)
        self.ssh.type_commands(DeviceName.TCAM, 'ping -I rmnet_data1 www.baidu.com -c 4')


    def after_class(self, ecu):
        self.io.bgm_diag_line_up()
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        # 关闭飞行模式
        self.ssh.set_airplane_mode(sts=isOn.Off)
        interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
        if 'rmnet_data1' not in interface:
            logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(2)
        # self.mix.log_special_obj.start_v2t_monitor()
        # self.mix.log_special_obj.config_trigger_to_valid(trigger_type='bgm_remote', own_data=copy.deepcopy(log_bgm_config_data), source=1)
        # self.mix.log_special_obj.stop_v2t_monitor()
        super().after_class(self, ecu)


#  =====================================================触发上传测试case===============================================================


    @pytest.mark.full123
    @allure.title('语音触发上传 异常场景：休眠唤醒') 
    def test_caseid_1993074_1993075_1993145(self):
            chars = string.ascii_letters + string.digits
            request_id = ''.join(random.choice(chars) for _ in range(20))
            soa_parameters={"triggerSourceInfo": {"source":2, "event": 'local_voice', "request_id": request_id, "ctrlParam": "123"}}
            vehicle_log_msg=self.mix.log_special_obj.vehicle_network_sleep_exception_log_fetcher(trigger_mode=3, device_name=DeviceName.BGM,soa_parameters=soa_parameters,
                                                                                                 timeout=30*60)
                    # 解析日志
            self.mix.log_special_obj.parse_log_and_check(vehicle_log_msg=vehicle_log_msg,vid=self.vid, device_name=DeviceName.BGM)


    @pytest.mark.full123
    @allure.title('按键触发上传 异常场景：休眠唤醒') 
    def test_caseid_1993044_1993045_1993144(self):
            chars = string.ascii_letters + string.digits
            request_id = ''.join(random.choice(chars) for _ in range(20))
            soa_parameters={"triggerSourceInfo": {"source":2, "event": 'local_button', "request_id": request_id, "ctrlParam": "123"}}
            vehicle_log_msg=self.mix.log_special_obj.vehicle_network_sleep_exception_log_fetcher(trigger_mode=3, device_name=DeviceName.BGM,soa_parameters=soa_parameters,
                                                                                                 timeout=20*60)
                    # 解析日志
            self.mix.log_special_obj.parse_log_and_check(vehicle_log_msg=vehicle_log_msg,vid=self.vid, device_name=DeviceName.BGM)


    @pytest.mark.full123
    @allure.title('云端触发上传 异常场景：休眠唤醒') 
    def test_caseid_1993014_1993015_1993143(self):
            chars = string.ascii_letters + string.digits
            request_id = ''.join(random.choice(chars) for _ in range(20))
            soa_parameters={"triggerSourceInfo": {"source":1, "event": 'webuser', "request_id": request_id, "ctrlParam": "123"}}
            vehicle_log_msg=self.mix.log_special_obj.vehicle_network_sleep_exception_log_fetcher(trigger_mode=3, device_name=DeviceName.BGM,soa_parameters=soa_parameters,
                                                                                                 timeout=20*60)
                    # 解析日志
            self.mix.log_special_obj.parse_log_and_check(vehicle_log_msg=vehicle_log_msg,vid=self.vid, device_name=DeviceName.BGM)


    @allure.title('语音触发上传 异常场景：断电') 
    def test_caseid_1993066_1993067_1993152(self):
            chars = string.ascii_letters + string.digits
            request_id = ''.join(random.choice(chars) for _ in range(20))
            soa_parameters={"triggerSourceInfo": {"source": 2, "event": 'local_voice', "request_id": request_id, "ctrlParam": "123"}}
            vehicle_log_msg=self.mix.log_special_obj.vehicle_power_off_exception_log_fetcher(trigger_mode=3, device_name=DeviceName.BGM,soa_parameters=soa_parameters,
                                                                                                 timeout=20*60)
                    # 解析日志
            self.mix.log_special_obj.parse_log_and_check(vehicle_log_msg=vehicle_log_msg,vid=self.vid, device_name=DeviceName.BGM)


    @allure.title('按键触发上传 异常场景：断电') 
    def test_caseid_1993036_1993037_1993151(self):
            chars = string.ascii_letters + string.digits
            request_id = ''.join(random.choice(chars) for _ in range(20))
            soa_parameters={"triggerSourceInfo": {"source": 2, "event": 'local_button', "request_id": request_id, "ctrlParam": "123"}}
            vehicle_log_msg=self.mix.log_special_obj.vehicle_power_off_exception_log_fetcher(trigger_mode=3, device_name=DeviceName.BGM,soa_parameters=soa_parameters,
                                                                                                 timeout=20*60)
                    # 解析日志
            self.mix.log_special_obj.parse_log_and_check(vehicle_log_msg=vehicle_log_msg,vid=self.vid, device_name=DeviceName.BGM)


    @allure.title('云端触发上传 异常场景：断电') 
    def test_caseid_1993006_1993007_1993150(self):
            chars = string.ascii_letters + string.digits
            request_id = ''.join(random.choice(chars) for _ in range(20))
            soa_parameters={"triggerSourceInfo": {"source": 1, "event": 'webuser', "request_id": request_id, "ctrlParam": "123"}}
            vehicle_log_msg=self.mix.log_special_obj.vehicle_power_off_exception_log_fetcher(trigger_mode=3, device_name=DeviceName.BGM,soa_parameters=soa_parameters,
                                                                                                 timeout=20*60)
                    # 解析日志
            self.mix.log_special_obj.parse_log_and_check(vehicle_log_msg=vehicle_log_msg,vid=self.vid, device_name=DeviceName.BGM)


    @pytest.mark.sanity
    @allure.title('语音触发上传 异常场景：诊断复位') 
    def test_caseid_1993072_1993073_1993166(self):
            chars = string.ascii_letters + string.digits
            request_id = ''.join(random.choice(chars) for _ in range(20))
            soa_parameters={"triggerSourceInfo": {"source": 2, "event": 'local_voice', "request_id": request_id, "ctrlParam": "123"}}
            vehicle_log_msg=self.mix.log_special_obj.vehicle_reset_1181_exception_log_fetcher(trigger_mode=3, device_name=DeviceName.BGM,soa_parameters=soa_parameters,
                                                                                                 timeout=20*60)
                    # 解析日志
            self.mix.log_special_obj.parse_log_and_check(vehicle_log_msg=vehicle_log_msg,vid=self.vid, device_name=DeviceName.BGM)


    @pytest.mark.sanity
    @allure.title('按键触发上传 异常场景：诊断复位') 
    def test_caseid_1993042_1993043_1993165(self):
            chars = string.ascii_letters + string.digits
            request_id = ''.join(random.choice(chars) for _ in range(20))
            soa_parameters={"triggerSourceInfo": {"source": 2, "event": 'local_button', "request_id": request_id, "ctrlParam": "123"}}
            vehicle_log_msg=self.mix.log_special_obj.vehicle_reset_1181_exception_log_fetcher(trigger_mode=3, device_name=DeviceName.BGM,soa_parameters=soa_parameters,
                                                                                                 timeout=20*60)
                    # 解析日志
            self.mix.log_special_obj.parse_log_and_check(vehicle_log_msg=vehicle_log_msg,vid=self.vid, device_name=DeviceName.BGM)


    @pytest.mark.sanity
    @allure.title('云端触发上传 异常场景：诊断复位') 
    def test_caseid_1993012_1993013_1993164_1986154(self):
            chars = string.ascii_letters + string.digits
            request_id = ''.join(random.choice(chars) for _ in range(20))
            soa_parameters={"triggerSourceInfo": {"source": 1, "event": 'webuser', "request_id": request_id, "ctrlParam": "123"}}
            vehicle_log_msg=self.mix.log_special_obj.vehicle_reset_1181_exception_log_fetcher(trigger_mode=3, device_name=DeviceName.BGM,soa_parameters=soa_parameters,
                                                                                                 timeout=20*60)
                    # 解析日志
            self.mix.log_special_obj.parse_log_and_check(vehicle_log_msg=vehicle_log_msg,vid=self.vid, device_name=DeviceName.BGM)


    @pytest.mark.sanity
    @allure.title('语音触发上传 异常场景：断网')  
    def test_caseid_1993159_1993068_1993069(self):
        # 语音触发上传异常断网
        chars = string.ascii_letters + string.digits
        request_id = ''.join(random.choice(chars) for _ in range(20))
        self.mix.log_special_obj.trigger_updatelog_check(vid=self.vid, device_name=DeviceName.BGM, timeout=20 * 60,
                                     partner_key="RemoteLogManagerService_client_BGM_RemoteLogManagerService",
                                     method_name="ReqUploadLog",
                                     soa_parameters={"triggerSourceInfo": {"source": 2,
                                                                           "event": 'local_voice',
                                                                           "request_id": request_id,
                                                                           "ctrlParam": "123"}},
                                     error_conditions=True
                                     )
        

    @pytest.mark.sanity
    @allure.title('按键触发上传 异常场景：断网')  
    def test_caseid_1993158_1993039_1993038(self):
        # 按键触发上传异常断网
        chars = string.ascii_letters + string.digits
        request_id = ''.join(random.choice(chars) for _ in range(20))
        self.mix.log_special_obj.trigger_updatelog_check(vid=self.vid, device_name=DeviceName.BGM, timeout=20 * 60,
                                     partner_key="RemoteLogManagerService_client_BGM_RemoteLogManagerService",
                                     method_name="ReqUploadLog",
                                     soa_parameters={"triggerSourceInfo": {"source": 2,
                                                                           "event": 'local_button',
                                                                           "request_id": request_id,
                                                                           "ctrlParam": "123"}},
                                     error_conditions=True
                                     )


    @pytest.mark.sanity
    @allure.title('云端触发上传 异常场景：断网')  
    def test_caseid_1993157_1993008_1993009(self):
        # 云端触发上传异常断网
        chars = string.ascii_letters + string.digits
        request_id = ''.join(random.choice(chars) for _ in range(20))
        self.mix.log_special_obj.trigger_updatelog_check(vid=self.vid, device_name=DeviceName.BGM, timeout=20 * 60,
                                     partner_key="RemoteLogManagerService_client_BGM_RemoteLogManagerService",
                                     method_name="ReqUploadLog",
                                     soa_parameters={"triggerSourceInfo": {"source": 1,
                                                                           "event": 'webuser',
                                                                           "request_id": request_id,
                                                                           "ctrlParam": "123"}},
                                     error_conditions=True
                                     )


    @pytest.mark.smoke
    @allure.title('语音触发上传 正常场景')  
    def test_caseid_1993080_1993081_1993138_1986178_1986178(self):
        chars = string.ascii_letters + string.digits
        request_id = ''.join(random.choice(chars) for _ in range(20))
        self.mix.log_special_obj.trigger_updatelog_check(vid=self.vid, device_name=DeviceName.BGM, timeout=20 * 60,
                                     partner_key="RemoteLogManagerService_client_BGM_RemoteLogManagerService",
                                     method_name="ReqUploadLog",
                                     soa_parameters={"triggerSourceInfo": {"source": 2,
                                                                           "event": 'local_voice',
                                                                           "request_id": request_id,
                                                                           "ctrlParam": "123"}})

    @pytest.mark.smoke
    @allure.title('按键触发上传 正常场景')  
    def test_caseid_1993082_1993083_1993137_1986177_1986204_1986177(self):
        chars = string.ascii_letters + string.digits
        request_id = ''.join(random.choice(chars) for _ in range(20))
        self.mix.log_special_obj.trigger_updatelog_check(vid=self.vid, device_name=DeviceName.BGM, timeout=20 * 60,
                                     partner_key="RemoteLogManagerService_client_BGM_RemoteLogManagerService",
                                     method_name="ReqUploadLog",
                                     soa_parameters={"triggerSourceInfo": {"source": 2,
                                                                           "event": 'local_button',
                                                                           "request_id": request_id,
                                                                           "ctrlParam": "123"}})

    @pytest.mark.smoke
    @allure.title('云端触发上传 正常场景')  
    def test_caseid_1993088_1993089_1993136_1986206_1988617(self):
        chars = string.ascii_letters + string.digits
        request_id = ''.join(random.choice(chars) for _ in range(20))
        self.mix.log_special_obj.trigger_updatelog_check(vid=self.vid, device_name=DeviceName.BGM, timeout=20 * 60,
                                     partner_key="RemoteLogManagerService_client_BGM_RemoteLogManagerService",
                                     method_name="ReqUploadLog",
                                     soa_parameters={"triggerSourceInfo": {"source": 1,
                                                                           "event": 'webuser',
                                                                           "request_id": request_id,
                                                                           "ctrlParam": "123"}})
         
    @pytest.mark.smoke
    @allure.title('FOTA失败触发上传')  
    def test_caseid_1986172(self):
        chars = string.ascii_letters + string.digits
        request_id = ''.join(random.choice(chars) for _ in range(20))
        self.mix.log_special_obj.trigger_updatelog_check(vid=self.vid, device_name=DeviceName.BGM, timeout=20 * 60,
                                     partner_key="RemoteLogManagerService_client_BGM_RemoteLogManagerService",
                                     method_name="ReqUploadLog",
                                     soa_parameters={"triggerSourceInfo": {"source": 1,
                                                                           "event": 'fota_fail',
                                                                           "request_id": request_id,
                                                                           "ctrlParam": "123"}})


    
