#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :test_soa_heat.py
@time         :8/27/24 11:23
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import time
from time import sleep

import allure
import pytest
from xat_ecu.legacy.soa_partner.src.partner_const import LOGMASTER_SERVICE_CLIENT, HIGHVOLTAGE_SERVICE_CLIENT, WIPER_SERVICE_CLIENT
from xat_ecu.legacy.common.logger import logger

from framework.automotive.core.common_sil_test_base import CommonSILTestBase


@allure.feature("SOA服务接口")
@allure.story("架构基础/LogMasterService")
class TestLogMasterService(CommonSILTestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.ssh.bgm_ssh.type_commands(commands='cd /tmp;touch s2s_startup_flag')
        self.ssh.bgm_ssh.type_commands(commands="ps -ef | grep /app/bin/jetlogd | grep -v grep | awk '{print $2}' | xargs kill -9")
        self.ssh.bgm_ssh.type_commands(commands='su -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;nohup /app/bin/jetlogd &"', timeout=2)
        self.ssh.bgm_ssh.type_commands(commands="ps -ef | grep /app/bin/service_monitor | grep -v grep | awk '{print $2}' | xargs kill -9")
        self.ssh.bgm_ssh.type_commands(commands='su -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;nohup /app/bin/service_monitor  -c /app/etc/service_monitor.json &"', timeout=2)
        self.ssh.bgm_ssh.type_commands(commands="ps -ef | grep /app/bin/em2 | grep -v grep | awk '{print $2}' | xargs kill -9")
        self.ssh.bgm_ssh.type_commands(commands='su -c "source /app/etc/bgm_app_env.sh; nohup /app/bin/em2 &"', timeout=2)
        self.ssh.bgm_ssh.type_commands(commands="ps -ef | grep /app/bin/s2s_service | grep -v grep | awk '{print $2}' | xargs kill -9")
        self.ssh.bgm_ssh.type_commands(commands='su -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;nohup /app/bin/s2s_service &"', timeout=2)
        time.sleep(20)
        self.soa.update([("LogMasterService", "client"),
                         ("HighVoltageService", "client"),
                         WIPER_SERVICE_CLIENT
                         ])
        self.soa.method_default_timeout = 10
        self.mock_mcu.start_run()
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.bus_comm.set("backbonefr", "BcmVddmBackBoneFr00", 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.bus_comm.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.bus_comm.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.bus_comm.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        sleep(0.5)
        self.soa.empty_all()
        logger.info(f"case开始运行")

    def after_each_func(self, ecu):
        logger.info(f"case结束运行")
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        
    @pytest.mark.smoke
    @allure.title("获取雨刮单刮模式&通知雨刮单刮模式 ")
    def test_caseid_1979708(self): # 原mock mcu用例
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 0)
        self.soa.empty_all(0.5)
        for OneshotSts in [1, 0]:
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', OneshotSts)
            self.soa.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperOneshotSts",
                                      {"info": {"id": 0, "sts": OneshotSts}})
            self.soa.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperOneshotSts", {"wipers": [0]},
                                                  {"out": [{"id": 0, "sts": OneshotSts}]})


