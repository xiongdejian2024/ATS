#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_poweroutlet_ctrl_abc.py
@Author      : qian.feng@jiduauto.com
@Time        : 2023/11/21 11:30
@Description: BGM车控车设RelayControl
"""

import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("车控车设")
@allure.story("12v电源继电器功能")
@pytest.mark.sam
class TestPowerOutletRelayCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([
                        "TailGateService_client", 
                        "CentralLockService_client", 
                        "LightService_client",
                        "VehicleModeService_client",
                        "KeyService_client",
                        ])
        sleep(2)

    def before_each_func(self, ecu):
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        sleep(2)

    def after_each_func(self, ecu):
        sleep(2)

        
    def after_class(self, ecu):
        try:
            self.mix.restore_poweroutlet_relay_simulation_environment()
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("461690 电源继电器控制_诊断连接Abandoned电源继电器断开上切Drving继电器闭合")
    @pytest.mark.full
    def test_poweroutlet_ctrl_caseid_118433(self):
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 1)
        self.mix.set_common_precontion(UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)

    @allure.title("461690 电源继电器控制_诊断连接Abandoned电源继电器断开上切Inactive继电器闭合")
    @pytest.mark.sanity
    def test_caseid_118427(self):
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 1)
        self.mix.set_common_precontion(UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)

    @allure.title("461690 电源继电器控制_诊断连接Abandoned电源继电器断开上切Convenience继电器闭合")
    @pytest.mark.full
    def test_caseid_118430(self):
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 1)
        self.mix.set_common_precontion(UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)

    @allure.title("461690 电源继电器控制_诊断连接Abandoned电源继电器断开上切Active继电器闭合")
    @pytest.mark.full
    def test_caseid_118432(self):
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 1)
        self.mix.set_common_precontion(UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)
        self.mix.set_common_precontion(UsageMode.ACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)

    @allure.title("461690 PowerOutlet继电器控制_UM=Abandoned_PowerOutlet继电器断开")
    @pytest.mark.smoke
    def test_caseid_1985399(self):
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.mix.set_common_precontion(UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Abandoned&&0=kNoReq =>1条件不满足不发闭合请求")
    @pytest.mark.full
    def test_caseid_1985417(self):
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)
        self.mix.set_common_precontion(UsageMode.ABANDONED)
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Abandoned&&0=kNoReq =>2继电器闭合请求忽略")
    @pytest.mark.full
    def test_caseid_1985425(self):
        self.mix.set_common_precontion(UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Convenience&&=1：kOn =>2继电器断开请求忽略")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1985428(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Inactive&&0==>1==>2继电器闭合")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1985416(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Drving&&0=kNoReq =>2继电器断开请求忽略")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1985421(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Active&&0=kNoReq =>2继电器断开请求忽略")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1985422(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        self.soa.set_power_outlet_req(PowerOutLetReq.NoReq)
        self.mix.set_common_precontion(UsageMode.ACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Inactive诊断激活线连接&&=1：kOn =>2继电器断开请求忽略")
    @pytest.mark.full
    def test_caseid_1985426(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        sleep(30)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 1)
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Active&&=1：kOn =>0继电器请求0")
    @pytest.mark.full
    def test_caseid_1985429(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1)   
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 1)
        self.mix.set_common_precontion(UsageMode.ACTIVE) 
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)  
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 11)   
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 0)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_InActive&&=1：kOn =>0继电器请求0")
    @pytest.mark.full
    def test_caseid_1985431(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 0)
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 1)
        sleep(2)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2)
        sleep(3)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 0)

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Convenience电源继电器闭合 =>2:kOff继电器断开请求忽略")
    @pytest.mark.full
    def test_caseid_1988033(self):
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)   
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, poweroutproxy=PowerOutLetReq.NoReq)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, poweroutproxy=PowerOutLetReq.NoReq)

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Active电源继电器闭合 =>2:kOff继电器断开请求忽略")
    @pytest.mark.full
    def test_caseid_1985434(self):
        self.mix.set_common_precontion(UsageMode.ACTIVE)   
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 11)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, poweroutproxy=PowerOutLetReq.NoReq)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, poweroutproxy=PowerOutLetReq.NoReq)

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Inactive==>Abandoned补发NoReq")
    @pytest.mark.sanity
    def test_caseid_1986699(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1)  
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 1) 
        self.mix.set_common_precontion(UsageMode.ABANDONED)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 0)  
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 0) 

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Inactive==>Abandoned补发NoReq")
    @pytest.mark.sanity
    def test_caseid_1986698(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1)  
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 1) 
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)  
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 0) 

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Inactive==>Abandoned补发NoReq")
    @pytest.mark.sanity
    def test_caseid_1986697(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1)  
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 1) 
        self.mix.set_common_precontion(UsageMode.ACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 11)  
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 0) 

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Inactive==>Convenience补发NoReq")
    @pytest.mark.sanity
    def test_caseid_1986696(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1)  
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 1) 
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 2)  
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 0) 

    @allure.title("MSO-SVRIF-6847 设置12v继电器仲裁逻辑_设置继电器无请求同时先关闭再开启_继电器关闭3s后恢复默认值")
    @pytest.mark.full
    def test_caseid_1985452(self):
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1)  
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2) 
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        time.sleep(2.8)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 0) 

    @allure.title("MSO-SVRIF-6847 设置12v继电器仲裁逻辑_设置继电器Req =1&&1s内设置Req =0&&2s内设置Req =2_继电器最终断开状态")
    @pytest.mark.full
    def test_caseid_1985455(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1)   
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 1) 
        self.soa.set_power_outlet_req(PowerOutLetReq.NoReq)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 1) 
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2)
        time.sleep(2.8)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 0) 

    @allure.title("MSO-SVRIF-6847 设置12v继电器仲裁逻辑_设置继电器Req=1计时3s无新请求动作_继电器闭合请求恢复默认值")
    @pytest.mark.full
    def test_caseid_1985454(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1)   
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 1) 
        time.sleep(3.1)
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)

    @allure.title("MSO-SVRIF-6847 设置12v继电器仲裁逻辑_设置继电器开启3s内设置关闭_继电器关闭请求发出")
    @pytest.mark.full
    def test_caseid_1985453(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1)   
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 1) 
        time.sleep(1)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2)
        time.sleep(3.1)
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)

    @allure.title("MSO-SVRIF-6847 设置12v继电器仲裁逻辑_设置继电器Req=2&&1s内同时设置设置继电器Req=1_继电器关闭后3s恢复0")
    @pytest.mark.full
    def test_caseid_1985451(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1)   
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2)
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2)
        time.sleep(2.5)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 0)

    @allure.title("MSO-SVRIF-6847 设置12v继电器仲裁逻辑_设置继电器Req=2&&1s内同时设置设置继电器Req=0_继电器关闭后3s恢复0")
    @pytest.mark.full
    def test_caseid_1985450(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1)   
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2)
        self.soa.set_power_outlet_req(PowerOutLetReq.NoReq)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2)
        time.sleep(2.5)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 0)

    @allure.title("MSO-SVRIF-6847 设置12v继电器仲裁逻辑_设置继电器Req==2计时3s无请求_继电器关闭")
    @pytest.mark.full
    def test_caseid_1988034(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1)   
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2)
        self.soa.set_power_outlet_req(PowerOutLetReq.NoReq)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2)
        time.sleep(2.5)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 0)

    # @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Drving&&=2：kOff =>闭合请求忽略")
    # @pytest.mark.full
    # def test_caseid_1985445(self):
    #     self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)
    #     self.mix.set_common_precontion(UsageMode.DRIVING)
    #     self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)   
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, poweroutproxy=PowerOutLetReq.NoReq)
    #     self.soa.set_power_outlet_req(PowerOutLetReq.Off)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, poweroutproxy=PowerOutLetReq.NoReq)

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Active&&=2：kOff =>闭合请求忽略")
    @pytest.mark.full
    def test_caseid_1985444(self):
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)
        self.mix.set_common_precontion(UsageMode.ACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 11)   
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, poweroutproxy=PowerOutLetReq.NoReq)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, poweroutproxy=PowerOutLetReq.NoReq)

    @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Convenience&&=2：kOff 闭合请求忽略")
    @pytest.mark.full
    def test_caseid_1985443(self):
        self.bus_comm.check_relay_proxyreq(PowerOutLetReq.NoReq)
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 2)   
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, poweroutproxy=PowerOutLetReq.NoReq)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, poweroutproxy=PowerOutLetReq.NoReq)

    # @allure.title("MSO-SVRIF-6847 设置12v继电器状态_Convenience&&=2：kOff 闭合请求忽略")
    # @pytest.mark.full
    # def test_caseid_1985443(self):
    #     self.io.bgm_diag_line_down()
    #     logger.info(f'断开诊断激活线')
    #     sleep(30)
    #     self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
    #     self.sd_tester.send_data([0x11, 0x01])
    #     sleep(30)
    #     self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off, poweroutproxy=PowerOutLetReq.NoReq)
    #     self.soa.set_power_outlet_req(PowerOutLetReq.On)
    #     self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 1)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
    #     self.soa.set_power_outlet_req(PowerOutLetReq.Off)
    #     self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)
    #     time.sleep(3)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)

    @allure.title("PwrLvlElecMai!=1且Usagemode=driving12v电源继电器闭合下切Abandoned继电器释放")
    @pytest.mark.full
    def test_caseid_118420(self):
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.mix.set_common_precontion(UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)

    @allure.title("Inactive诊断激活线断开12v电源继电器断开_诊断激活线闭合12v电源继电器闭合")
    @pytest.mark.restart
    @pytest.mark.smoke
    def test_caseid_118421(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(5)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off, time_wait=1)
        self.io.bgm_diag_line_up()  # 恢复诊断激活线连接状态
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, time_wait=1)

    @allure.title("Convenience诊断激活线断开且EgyLvlElecMai！=1_12v电源继电器断开_EgyLvlElecMai=0_12v电源继电器闭合")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118435(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(5)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
        sleep(.5)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429d03', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_egylvlelec(mai=1, subtype=1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off, time_wait=1)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '0000', '6f429d03', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, time_wait=1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d00', check_method=Check_Method.response, recover=False)  # 退诊断

    @allure.title("Inactive诊断激活线连接且ElPowerLevel!=1_12v电源继电器闭合_ElPowerLevel=1_12v电源继电器断开")
    @pytest.mark.sanity
    def test_caseid_118434(self):
        self.io.bgm_diag_line_up()  # 恢复诊断激活线连接状态
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        sleep(.5)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False) # 退诊断
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)

    @allure.title("PwrLvlElecMai_Usagemode_active")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118436(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(5)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.mix.set_common_precontion(UsageMode.ACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
        sleep(.5)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, time_wait=1)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off, time_wait=1)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False) # 退诊断
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)

    @allure.title("PwrLvlElecMai_Usagemode_Driving闭合")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118437(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(5)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        sleep(.5)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, time_wait=1)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, time_wait=1)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False) # 退诊断

    @allure.title("PowerOutlet继电器控制_Remote闭锁_PowerOutlet继电器OFF")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1919348(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(5)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.On)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.soa.set_power_outlet_req(poweroutletreq = PowerOutLetReq.NoReq)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.NoReq)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(60.1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)

    @allure.title("PowerOutlet继电器控制_外部NFC闭锁1min&&NoReq_PowerOutlet继电器断开")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1985392(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(5)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.On)
        self.soa.set_power_outlet_req(poweroutletreq = PowerOutLetReq.NoReq)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.NoReq)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        sleep(60.1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)

    @allure.title("PowerOutlet继电器控制_外部NFC闭锁1min&&NoReq_PowerOutlet继电器断开")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1985393(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(5)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.On)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, time_wait=1) # 服务设置维持2s会变为Noreq
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(60.1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.On)
        sleep(3)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.NoReq)

    @allure.title("PowerOutlet继电器控制_内部闭锁1min&&NoReq_PowerOutlet继电器闭合")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1985397(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(5)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.On)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, time_wait=0.5) # 服务设置维持2s会变为Noreq
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(60.1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, time_wait=1)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.NoReq)

    @allure.title("PowerOutlet继电器控制_外部闭锁1min内RlyPwrCmdProxyReq = 2_Off_PowerOutlet继电器断开")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1985398(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(5)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.On)
        sleep(.3)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On) 
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm,  source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        sleep(20)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off, time_wait=1) 
        sleep(3)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.NoReq)

    @allure.title("PowerOutlet继电器控制_UM=Inactive&&RlyPwrCmdProxyReq = 2:Off_PowerOutlet继电器断开")
    @pytest.mark.restart
    @pytest.mark.smoke
    def test_caseid_1985400(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(5)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.On)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, time_wait=1) 
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off, time_wait=1) 
        sleep(3)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.NoReq)

    # @allure.title("PowerOutlet继电器控制_UM=Inactive&&服务请求闭合_PowerOutlet继电器闭合服务请求Noreq计时420s继电器断开")
    # @pytest.mark.update
    # @pytest.mark.longtime
    # @pytest.mark.restart
    # @pytest.mark.sanity
    # def test_caseid_1985402(self):
    #     self.io.bgm_diag_line_down()
    #     logger.info(f'断开诊断激活线')
    #     sleep(5)
    #     self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
    #     self.sd_tester.send_data([0x11, 0x01])
    #     sleep(30)
    #     self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
    #     self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
    #     self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
    #     self.soa.set_power_outlet_req(PowerOutLetReq.On)
    #     self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.On)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On) 
    #     sleep(3)
    #     self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.NoReq)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
    #     sleep(420)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off, time_wait=1) 

    # @allure.title("PowerOutlet继电器控制_UM=Convenience&&车辆能量受限egylvlelec=1_PowerOutlet继电器断开")
    # @pytest.mark.update
    # @pytest.mark.restart
    # @pytest.mark.sanity
    # def test_caseid_1985406(self):
    #     self.io.bgm_diag_line_down()
    #     logger.info(f'断开诊断激活线')
    #     sleep(5)
    #     self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
    #     self.sd_tester.send_data([0x11, 0x01])
    #     sleep(30)
    #     self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
    #     self.mix.set_common_precontion(UsageMode.CONVENIENCE)
    #     self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, time_wait=1)
    #     sleep(.5)
    #     self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429d03', check_method=Check_Method.response, recover=False)
    #     self.bus_comm.check_egylvlelec(mai=1, subtype=1)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off, time_wait=1)
    #     self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d')

    # @allure.title("PowerOutlet继电器控制_UM=Active&&车辆能量受限_PowerOutlet继电器断开")
    # @pytest.mark.update
    # @pytest.mark.restart
    # @pytest.mark.sanity
    # def test_caseid_1985408(self):
    #     self.io.bgm_diag_line_down()
    #     logger.info(f'断开诊断激活线')
    #     sleep(5)
    #     self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
    #     self.sd_tester.send_data([0x11, 0x01])
    #     sleep(30)
    #     self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
    #     self.mix.set_common_precontion(UsageMode.ACTIVE)
    #     self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
    #     sleep(.5)
    #     self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429d03', check_method=Check_Method.response, recover=False)
    #     self.bus_comm.check_egylvlelec(mai=1, subtype=1)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)
    #     self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d')

    # @allure.title("Inactive且服务请求12电源继电器闭合&&车辆能量受限egylvlelec=1_PowerOutlet继电器断开")
    # @pytest.mark.update
    # @pytest.mark.restart
    # @pytest.mark.sanity
    # def test_caseid_1985439(self):
    #     self.io.bgm_diag_line_down()
    #     logger.info(f'断开诊断激活线')
    #     sleep(5)
    #     self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
    #     self.sd_tester.send_data([0x11, 0x01])
    #     sleep(30)
    #     self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
    #     self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
    #     self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
    #     self.soa.set_power_outlet_req(PowerOutLetReq.On)
    #     self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.On)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, time_wait=1) 
    #     self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429d03', check_method=Check_Method.response, recover=False)
    #     self.bus_comm.check_egylvlelec(mai=1, subtype=1)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off, time_wait=1)
    #     self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d')

    @allure.title("PowerOutlet继电器控制_离车落锁1min_PowerOutlet继电器断开")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1985472(self):
        self.sd_tester.write_ccp(ccp={94: 0x80, 142:0x83, 10: 0x2})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(5)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.On)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, time_wait=1) 
        sleep(.5)     
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(60)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off) 
        self.bus_comm.check_power_outlet_relay_proxy_req(proxy_req=PowerOutLetReq.NoReq)

    # @allure.title("PowerOutlet继电器控制_UM=Inactive诊断激活线连接车身能量受限继电器断开")
    # @pytest.mark.update
    # @pytest.mark.full
    # def test_caseid_1985474(self):
    #     self.io.bgm_diag_line_up()
    #     logger.info(f'诊断激活线连接')
    #     self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
    #     self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
    #     self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On, time_wait=1) 
    #     self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429d03', check_method=Check_Method.response, recover=False)
    #     self.bus_comm.check_egylvlelec(mai=1, subtype=1)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off, time_wait=1)
    #     self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d')
