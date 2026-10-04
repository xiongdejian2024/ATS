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


@allure.feature("车控车设")
@allure.story("被动安全WTI告警")
class TestWTIServicePassiveSafety(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["SeatService_client", "WTIService_client"])
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.All,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Unlock,
        )
        sleep(2)

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(3)

    def after_class(self, ecu):
        pass

    @allure.title("WTI_安全带指示灯_主驾安全带触发2级告警_安全带指示灯state==1:CommonTelltaleStateOn")
    @pytest.mark.sanity
    def test_caseid_1982743(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.FrontLeft,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Unlock,
        )
        sleep(0.5)
        self.soa.get_warning_msg_List(name="Driver Seat Belt Warning", info="1")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="1"
        )

        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.get_warning_msg_List(name="Driver Seat Belt Warning", info="0")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="0"
        )

    @allure.title("WTI_安全带指示灯_副驾安全带触发2级告警_安全带指示灯state==1:CommonTelltaleStateOn")
    @pytest.mark.sanity
    def test_caseid_1982750(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.FrontRight, seat_sts=SeatOccptSts.Fmale)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.FrontRight,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Unlock,
        )
        sleep(0.5)
        self.soa.get_warning_msg_List(name="Passenger Seat Belt Warning", info="1")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="1"
        )
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.soa.get_warning_msg_List(name="Passenger Seat Belt Warning", info="0")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="0"
        )

    @allure.title("WTI_安全带指示灯_后排左侧安全带触发2及告警_安全带指示灯state==1:CommonTelltaleStateOn")
    @pytest.mark.sanity
    def test_caseid_1982751(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.RearLeft, seat_sts=SeatOccptSts.OccptLrg)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.RearLeft,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Unlock,
        )
        sleep(0.5)
        # self.soa.get_warning_msg_List(name="Second Row Left Seat Belt Warning", info="1")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="1"
        )
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        # self.soa.get_warning_msg_List(name="Second Row Left Seat Belt Warning", info="1")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="0"
        )

    @allure.title("WTI_安全带指示灯_后排右侧安全带触发2及告警_安全带指示灯state==1:CommonTelltaleStateOn")
    @pytest.mark.sanity
    @pytest.mark.verify
    def test_caseid_1982752(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.RearRight, seat_sts=SeatOccptSts.OccptLrg)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.RearRight,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Unlock,
        )
        # self.soa.get_warning_msg_List(name="Second Row Right Seat Belt Warning", info="1")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="1"
        )

        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        # self.soa.get_warning_msg_List(name="Second Row Right Seat Belt Warning", info="0")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="0"
        )

    @allure.title("WTI_安全带指示灯_后排中间安全带触发2及告警_安全带指示灯state==1:CommonTelltaleStateOn")
    @pytest.mark.sanity
    def test_caseid_1982753(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.RearMiddle, seat_sts=SeatOccptSts.OccptLrg)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.RearMiddle,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Unlock,
        )
        sleep(0.5)
        # self.soa.event_check_warning_info_list(name="Second Row Middle Seat Belt Warning", info="1")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="1"
        )
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        # self.soa.event_check_warning_info_list(name="Second Row Middle Seat Belt Warning", info="0",)
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="0"
        )

    @allure.title("WTI_安全带指示灯_车内安全带故障status==5_安全带指示灯state==1:CommonTelltaleStateOn")
    @pytest.mark.sanity
    def test_caseid_1982754(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.All, seat_sts=SeatOccptSts.OccptLrg)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.All,
            blt_flt_sts=BltFltSts.Fault,
            blt_lock_sts=BltLockSts.Lock,
        )
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="1"
        )
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="0"
        )
        
    @allure.title("MSO-SVRIF-3130_WTI_安全带指示灯_主驾安全带触发3级告警_安全带指示灯state==2:CommonTelltaleStateFlash")
    @pytest.mark.full
    def test_caseid_1982755(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,veh_spd=6.2)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.FrontLeft,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Unlock,
        )
        self.soa.get_warning_msg_List(name="Driver Seat Belt Warning", info="2")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="2"
        )
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.get_warning_msg_List(name="Driver Seat Belt Warning", info="0")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="0"
        )
        
    @allure.title("MSO-SVRIF-3130_WTI_安全带指示灯_后排左侧安全带触发3级告警_安全带指示灯state==2:CommonTelltaleStateFlash")
    @pytest.mark.full
    def test_caseid_1982757(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,veh_spd=6.2)
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.RearLeft,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Unlock,
        )
        self.soa.get_belt_warning(seats=SeatsAlrm.SeatRearRow,seat_id=SeatId.RearLeft,warn_sts=BeltWarning.Level2Low)
        self.soa.get_warning_msg_List(name="Second Row Left Seat Belt Warning", info="2")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="2"
        )
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.soa.get_warning_msg_List(name="Second Row Left Seat Belt Warning", info="0")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="0"
        )
        
    @allure.title("MSO-SVRIF-3130_WTI_安全带指示灯_后排右侧安全带触发3级告警_安全带指示灯state==2:CommonTelltaleStateFlash")
    @pytest.mark.full
    def test_caseid_1982758(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,veh_spd=6.2)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.RearRight,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Unlock,
        )
        self.soa.get_belt_warning(seats=SeatsAlrm.SeatRearRow,seat_id=SeatId.RearRight,warn_sts=BeltWarning.Level2Low)
        self.soa.get_warning_msg_List(name="Second Row Right Seat Belt Warning", info="2")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="2"
        )
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.soa.get_warning_msg_List(name="Second Row Right Seat Belt Warning", info="0")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="0"
        )

    @allure.title("MSO-SVRIF-3130_WTI_安全带指示灯优先级_副驾安全带指示灯state==3&&后排右安全带指示灯state==2")
    @pytest.mark.full
    def test_caseid_1982760(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,veh_spd=6.2)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.FrontRight,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Unlock,
        )
        sleep(35)
        self.soa.get_belt_warning(seats=SeatsAlrm.SeatFrontRow,seat_id=SeatId.FrontRight,warn_sts=BeltWarning.Level2High)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.RearRight,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Unlock,
        )
        self.soa.get_belt_warning(seats=SeatsAlrm.SeatRearRow,seat_id=SeatId.RearRight,warn_sts=BeltWarning.Level1)
        self.soa.get_warning_msg_List(name="Passenger Seat Belt Warning", info="3")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="3"
        )

        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.soa.get_warning_msg_List(name="Passenger Seat Belt Warning", info="0")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="0"
        )
        
    @allure.title("MSO-SVRIF-3130_WTI_安全带指示灯优先级_主驾安全带指示灯state==1&&后排左安全带指示灯state==2")
    @pytest.mark.full
    def test_caseid_1982761(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.FrontLeft,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Unlock,
        )
        self.soa.get_belt_warning(seats=SeatsAlrm.SeatFrontRow,seat_id=SeatId.FrontLeft,warn_sts=BeltWarning.Level1)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,veh_spd=6.2)
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.RearLeft,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Unlock,
        )
        self.soa.get_belt_warning(seats=SeatsAlrm.SeatRearRow,seat_id=SeatId.RearLeft,warn_sts=BeltWarning.Level2Low)
        self.soa.get_warning_msg_List(name="Driver Seat Belt Warning", info="2")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="2"
        )

        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.get_warning_msg_List(name="Driver Seat Belt Warning", info="0")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(
            name="Seat Belt", state="0"
        )
        
    @allure.title("MSO-SVRIF-3130_WTI_安全带指示灯优先级_主驾安全带指示灯state==2&&后排右安全带指示灯state==0")
    @pytest.mark.full
    def test_caseid_1982762(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.RearRight,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Lock,
        )
        self.soa.get_belt_warning(seats=SeatsAlrm.SeatRearRow,seat_id=SeatId.RearRight,warn_sts=BeltWarning.OccupiedAndFasten)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_blt_sts(
            seat_id=SeatId.FrontLeft,
            blt_flt_sts=BltFltSts.NoFault,
            blt_lock_sts=BltLockSts.Unlock,
        )
        self.soa.get_belt_warning(seats=SeatsAlrm.SeatFrontRow,seat_id=SeatId.FrontLeft,warn_sts=BeltWarning.Level1)
        self.soa.get_warning_msg_List(name="Driver Seat Belt Warning", info="1")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="1")
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.get_warning_msg_List(name="Driver Seat Belt Warning", info="0")
        self.soa.get_and_event_check_seatbelt_sign_warning_light_list(name="Seat Belt", state="0")

    @allure.title("MSO-SVRIF-3189_WTI_安全气囊故障信息_Aondond-Convenience模式5s计时器内设置RestrntSysMsgReq==2_Airbag Failure==0")
    @pytest.mark.full
    def test_caseid_1983141(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_airbag_warning_sts(sts=AirbagWarningSts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_airbag_warning_sts(sts=AirbagWarningSts.On)
        self.soa.get_warning_msg_List(name="Airbag Failure", info="0")
        
    @allure.title("MSO-SVRIF-3189_WTI_安全气囊故障信息_Active模式下安全气囊RestrntSysMsgReq=1_Airbag Failure==0")
    @pytest.mark.full
    def test_caseid_1983143(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_airbag_warning_sts(sts=AirbagWarningSts.Off)
        sleep(5.1)
        self.soa.get_warning_msg_List(name="Airbag Failure", info="0")
        
    @allure.title("MSO-SVRIF-3189_WTI_安全气囊故障信息_Drving&Failure==1气囊故障恢复RestrntSysMsgReq！=2_Failure==0")
    @pytest.mark.full
    def test_caseid_1983144(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_airbag_warning_sts(sts=AirbagWarningSts.On)
        sleep(1)
        self.soa.get_and_event_check_warning_info_list(name="Airbag Failure", info="1")
        # self.soa.get_warning_msg_List(name="Airbag Failure", info="1")
        # self.soa.event_check_warning_info_list(name="Airbag Failure", info="1")
        self.bus_comm.set_airbag_warning_sts(sts=AirbagWarningSts.Off)
        self.soa.get_warning_msg_List(name="Airbag Failure", info="0")