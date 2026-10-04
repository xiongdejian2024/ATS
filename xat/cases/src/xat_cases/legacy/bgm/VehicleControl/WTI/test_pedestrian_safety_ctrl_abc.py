#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_WTIService_passivesafety.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/21 11:30
@Description: BGM车控车乘客安全
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
from xat_ecu.legacy.soa_partner.src.partner_const import *


@allure.feature("车控车设")
@allure.story("被动安全WTI告警")
class TestWTIServicePassiveSafety(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["SeatService_client", "WTIService_client", "InterCommService_client_BGM_InterCommService"])
        sleep(2)

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)

    def after_class(self, ecu):
        pass

    @allure.title("WTI_安全带指示灯_主驾安全带触发2级告警_安全带指示灯state==1:CommonTelltaleStateOn")
    @pytest.mark.full
    def test_caseid_1982743(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault,
                                  blt_lock_sts=BltLockSts.Unlock)
        sleep(.5)
        self.soa.get_warning_msg_List(name="Driver Seat Belt Warning", info="1")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="1")

        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.get_warning_msg_List(name="Driver Seat Belt Warning", info="0")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="0")

    @allure.title("WTI_安全带指示灯_副驾安全带触发2级告警_安全带指示灯state==1:CommonTelltaleStateOn")
    @pytest.mark.full
    def test_caseid_1982750(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.FrontRight, seat_sts=SeatOccptSts.Fmale)
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontRight, blt_flt_sts=BltFltSts.NoFault,
                                  blt_lock_sts=BltLockSts.Unlock)
        sleep(.5)
        self.soa.get_warning_msg_List(name="Passenger Seat Belt Warning", info="1")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="1")
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.soa.get_warning_msg_List(name="Passenger Seat Belt Warning", info="0")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="0")

    @allure.title(
        "WTI_安全带指示灯_后排左侧安全带触发2及告警_安全带指示灯state==1:CommonTelltaleStateOn")
    @pytest.mark.full
    def test_caseid_1982751(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.RearLeft, seat_sts=SeatOccptSts.OccptLrg)
        self.bus_comm.set_blt_sts(seat_id=SeatId.RearLeft, blt_flt_sts=BltFltSts.NoFault,
                                  blt_lock_sts=BltLockSts.Unlock)
        sleep(.5)
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="1")
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="0")

    @allure.title(
        "WTI_安全带指示灯_后排右侧安全带触发2及告警_安全带指示灯state==1:CommonTelltaleStateOn")
    @pytest.mark.full
    def test_caseid_1982752(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.RearRight, seat_sts=SeatOccptSts.OccptLrg)
        self.bus_comm.set_blt_sts(seat_id=SeatId.RearRight, blt_flt_sts=BltFltSts.NoFault,
                                  blt_lock_sts=BltLockSts.Unlock)
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="1")

        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="0")

    @allure.title(
        "WTI_安全带指示灯_后排中间安全带触发2及告警_安全带指示灯state==1:CommonTelltaleStateOn")
    @pytest.mark.full
    def test_caseid_1982753(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.RearMiddle, seat_sts=SeatOccptSts.OccptLrg)
        self.bus_comm.set_blt_sts(seat_id=SeatId.RearMiddle, blt_flt_sts=BltFltSts.NoFault,
                                  blt_lock_sts=BltLockSts.Unlock)
        sleep(.5)
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="1")

        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="0")

    @allure.title(
        "WTI_安全带指示灯_车内安全带故障status==5_安全带指示灯state==1:CommonTelltaleStateOn")
    @pytest.mark.full
    def test_caseid_1982754(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.All, seat_sts=SeatOccptSts.OccptLrg)
        self.bus_comm.set_blt_sts(seat_id=SeatId.All, blt_flt_sts=BltFltSts.Fault,
                                  blt_lock_sts=BltLockSts.Lock)
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="1")

        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="0")

    @allure.title(
        "WTI_安全带指示灯_主驾安全带触发4级告警_安全带指示灯state==3:CommonTelltaleStateFlash")
    @pytest.mark.full
    def test_caseid_1982759(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault,blt_lock_sts=BltLockSts.Unlock)
        self.soa.get_belt_warning(seats=SeatsAlrm.SeatFrontRow,seat_id=SeatId.FrontLeft,warn_sts=BeltWarning.Level1)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,veh_spd=9.8)  # 表显车速大于35km/h
        sleep(2)
        self.soa.get_belt_warning(seats=SeatsAlrm.SeatFrontRow,seat_id=SeatId.FrontLeft,warn_sts=BeltWarning.Level2High)
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="3")
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)#设置安全带告警降级
        # self.mix.set_seats_present_sts(drv_seat=SeatPresSts.NoPres)
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="0")

    @allure.title(
        "MSO-SVRIF-3417_WTI_安全气囊报警灯_Abondoned模式下安全气囊指示灯闪烁RestrntSysLampReq==3_AirbagStatus==1")
    @pytest.mark.full
    def test_caseid_1982792(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_diag_connect_sts(con_act=1, con_sts=1)
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.LampFlash)
        self.soa.get_and_event_check_airbag_sign_warning_light_list(name="Airbag", state="1")
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.get_and_event_check_airbag_sign_warning_light_list(name="Airbag", state="0")

    @allure.title("MSO-SVRIF-3417_WTI_安全气囊报警灯__AirbagStatus==1&&RestrntSysLampReq==0：LampOff_AirbagStatus==0")
    @pytest.mark.full
    def test_caseid_1982802(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_diag_connect_sts(con_act=1, con_sts=1)
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.LampOn)
        self.soa.get_and_event_check_airbag_sign_warning_light_list(name="Airbag", state="1")
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.LampOff)
        self.soa.get_and_event_check_airbag_sign_warning_light_list(name="Airbag", state="0")

    @allure.title(" MSO-SVRIF-3417_WTI_安全气囊报警灯_Active模式下安全气囊指示灯闪烁_AirbagStatus==2")
    @pytest.mark.full
    def test_caseid_1982806(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_diag_connect_sts(con_act=1, con_sts=1)
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.LampFlash)
        self.soa.get_and_event_check_airbag_sign_warning_light_list(name="Airbag", state="2")
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.LampOff)
        self.soa.get_and_event_check_airbag_sign_warning_light_list(name="Airbag", state="0")

    @allure.title(
        "MSO-SVRIF-3417_WTI_安全气囊报警灯_Drving模式下安全气囊指示灯status==2闪烁后信号丢失Ukwn_Airbag-status==1")
    @pytest.mark.full
    def test_caseid_1982808(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_diag_connect_sts(con_act=1, con_sts=1)
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.LampFlash)
        self.soa.get_and_event_check_airbag_sign_warning_light_list(name="Airbag", state="2")
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.Unknown)
        self.soa.get_and_event_check_airbag_sign_warning_light_list(name="Airbag", state="0")

    @allure.title(" MSO-SVRIF-3417_WTI_安全气囊报警灯_abondone模式下安全气囊指示灯闪烁_AirbagStatus==0")
    @pytest.mark.full
    def test_caseid_1982809(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.soa.hmi_set_diag_connect_sts(con_act=1, con_sts=1)
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.LampFlash)
        self.soa.check_no_wti_event("Airbag")

    @allure.title(
        "MSO-SVRIF-3417_WTI_安全气囊报警灯_Inactive模式上切Convenience安全气囊指示灯RestrntSysLampReq==2：LampFlash_AirbagStatus==2")
    @pytest.mark.full
    def test_caseid_1982810(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_diag_connect_sts(con_act=1, con_sts=1)
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.LampFlash)
        self.soa.check_no_wti_event("Airbag")
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(.5)
        self.soa.get_and_event_check_airbag_sign_warning_light_list(name="Airbag", state="2")

    @allure.title("MSO-SVRIF-3417_WTI_安全气囊报警灯_Active模式下安全气囊指示灯闪烁_AirbagStatus==2")
    @pytest.mark.full
    def test_caseid_1982811(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_diag_connect_sts(con_act=1, con_sts=1)
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.LampFlash)
        self.soa.get_and_event_check_airbag_sign_warning_light_list(name="Airbag", state="2")
        sleep(5.1)
        self.soa.check_no_wti_event("Airbag")

    @allure.title("WTI_安全气囊报警灯_convenience模式下安全气囊指示灯常亮RestrntSysLampReq==3_AirbagStatus==1")
    @pytest.mark.full
    def test_caseid_1982802(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_diag_connect_sts(con_act=1, con_sts=1)
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.LampOn)
        self.soa.get_and_event_check_airbag_sign_warning_light_list(name="Airbag", state="1")
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.Unknown)
        self.soa.get_and_event_check_airbag_sign_warning_light_list(name="Airbag", state="0")

    @allure.title(
        "WTI_安全气囊故障信息_convenience模式下安全气囊RestrntSysMsgReq==2_Airbag Failure==2")
    @pytest.mark.full
    def test_caseid_1983136(self):
        result1 = "Airbag Failure"
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_diag_connect_sts(con_act=1, con_sts=1)
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.LampOff)
        self.soa.check_no_wti_event("Airbag")
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.LampOn)
        self.soa.get_and_event_check_airbag_sign_warning_light_list(name="Airbag", state="1")
        sleep(2)

    @allure.title(
        "WTI_安全气囊故障信息_Inactive-Drving模式5s计时器内RestrntSysMsgReq==2_Airbag Failure==2")
    @pytest.mark.full
    def test_caseid_1983138(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.Unknown)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(4.7)
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.LampFlash)
        self.soa.get_and_event_check_airbag_sign_warning_light_list(name="Airbag", state="2")
        sleep(2)

    @allure.title(
        "WTI_安全气囊故障信息_Aondond-Active模式5s计时器超时设置RestrntSysMsgReq==2_Airbag 无告警")
    @pytest.mark.full
    def test_caseid_1983139(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.Unknown)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        sleep(5.1)
        self.bus_comm.set_airbagsign_light_active_sts(AirbagLampReqSts.LampFlash)
        self.soa.check_no_wti_event("Airbag")
        sleep(2)

    @allure.title(
        "WTI_安全气囊故障信息_Aondond-Convenience模式5s计时器内设置RestrntSysMsgReq==2_Airbag Failure==0")
    @pytest.mark.full
    def test_caseid_1983141(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_airbag_warning_sts(AirbagWarningSts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(4.8)
        self.bus_comm.set_airbag_warning_sts(AirbagWarningSts.On)
        self.soa.check_no_wti_event("Airbag Failure")
        sleep(2)

    @allure.title(
        "WTI_安全气囊故障信息_Active模式下安全气囊RestrntSysMsgReq=1_Airbag Failure==0")
    @pytest.mark.full
    def test_caseid_1983143(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_airbag_warning_sts(AirbagWarningSts.NotVld1)
        self.bus_comm.set_airbag_warning_sts(AirbagWarningSts.Off)
        self.soa.check_no_wti_event("Airbag Failure")
        sleep(2)

    @allure.title("WTI_行人保护系统故障信息_usagemode循环_行人保护故障激活_Info:1")
    @pytest.mark.full
    def test_caseid_1983145(self):
        usgmod = ["ACTIVE", "INACTIVE", "CONVENIENCE", "ACTIVE", "DRIVING"]
        for i in usgmod:
            self.mix.set_common_precontion(usage_mode=getattr(UsageMode, i))
            self.bus_comm.set_pedestrian_protection_fault_sts(PedestProtectFltSts.NotVld1)

            self.bus_comm.set_pedestrian_protection_fault_sts(PedestProtectFltSts.On)
            self.soa.get_and_event_check_warning_info_list(name="Pedestrian System Failure", info="1")
            self.bus_comm.set_pedestrian_protection_fault_sts(PedestProtectFltSts.Off)
            self.soa.get_and_event_check_warning_info_list(name="Pedestrian System Failure", info="0")
        sleep(2)

    @allure.title("WTI_行人保护系统故障信息_usagemode循环_行人保护故障激活_Info:1")
    @pytest.mark.full
    def test_caseid_1983145(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_pedestrian_protection_fault_sts(PedestProtectFltSts.NotVld1)

        self.bus_comm.set_pedestrian_protection_fault_sts(PedestProtectFltSts.On)
        self.soa.get_and_event_check_warning_info_list(name="Pedestrian System Failure", info="1")
        self.bus_comm.set_pedestrian_protection_fault_sts(PedestProtectFltSts.Off)
        self.soa.get_and_event_check_warning_info_list(name="Pedestrian System Failure", info="0")
        sleep(2)

    @allure.title("WTI_行人保护系统故障信息_行人保护故障未激活循环恢复检测_Info:1")
    @pytest.mark.full
    @pytest.mark.verify
    def test_caseid_1983146(self):
        self.bus_comm.set_pedestrian_protection_fault_sts(PedestProtectFltSts.Off)
        for ForFlt in ["NotVld1", "Off", "NotVld2"]:
            self.bus_comm.set_pedestrian_protection_fault_sts(PedestProtectFltSts.On)
            self.soa.get_and_event_check_warning_info_list(name="Pedestrian System Failure", info="1")
            self.bus_comm.set_pedestrian_protection_fault_sts(getattr(PedestProtectFltSts, ForFlt))
            self.soa.get_and_event_check_warning_info_list(name="Pedestrian System Failure", info="0")
        sleep(2)

    @allure.title("WTI_Usagemode循环_行人保护系统激活信息_行人保护系统激活_Info:1")
    @pytest.mark.full
    def test_caseid_1983147(self):
        usgmod = ["ACTIVE", "INACTIVE", "CONVENIENCE", "ACTIVE", "DRIVING"]
        for i in usgmod:
            self.mix.set_common_precontion(usage_mode=getattr(UsageMode, i))
            self.bus_comm.set_pedestrian_protection_warning_sts(PedestProtectImpctSts.Off)
            sleep(.5)
            self.bus_comm.set_pedestrian_protection_warning_sts(PedestProtectImpctSts.On)
            self.soa.get_and_event_check_warning_info_list(name="Pedestrian System Enabled", info="1")
            self.bus_comm.set_pedestrian_protection_warning_sts(PedestProtectImpctSts.Off)
            self.soa.get_and_event_check_warning_info_list(name="Pedestrian System Enabled", info="0")
        sleep(2)
