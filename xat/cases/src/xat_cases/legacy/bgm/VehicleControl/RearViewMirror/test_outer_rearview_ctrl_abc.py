#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_outer_rearview_ctrl_abc.py
@Author      : xiangyue.li@jiduauto.com
@Time        : 2023/11/9 11:30
@Description : BGM车控车设外后视镜功能
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
@allure.story("后视镜功能")
class TestOuterRearViewCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(
            ["VehicleSetStatusService_client", "OuterRearViewService_client", "CentralLockService_client","VehicleModeService_client","SentryModeService_client"]
        )
        sleep(2)

    def before_each_func(self, ecu):
        self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x2, 94: 0x80, 142:0x83, 10: 0x2})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.io.set_five_door_sts(Door.close)        
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE, time_wait=1)  # 延时1s避免打断逻辑异常
        self.bus_comm.set_brake_pedal_sts(YesOrNo.No)
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        
    @allure.title("右后视镜向右调节")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.verify
    def test_caseid_1960087(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.hmi_set_start_adjust_viewmirror(
            viewPos=ViewPos.RearRight, direction=Direction.Right
        )
        self.bus_comm.check_extr_mirr_adj_req(ViewPos.RearRight, MirrDirReq.Right)

    @allure.title("右后视镜向左调节")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1960089(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.hmi_set_start_adjust_viewmirror(
            viewPos=ViewPos.RearRight, direction=Direction.Left
        )
        self.bus_comm.check_extr_mirr_adj_req(ViewPos.RearRight, MirrDirReq.Left)

    @allure.title("右后视镜向上调节")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1960090(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.hmi_set_start_adjust_viewmirror(
            viewPos=ViewPos.RearRight, direction=Direction.Up
        )
        self.bus_comm.check_extr_mirr_adj_req(ViewPos.RearRight, MirrDirReq.Up)

    @allure.title("右后视镜向下调节")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1960088(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.hmi_set_start_adjust_viewmirror(
            viewPos=ViewPos.RearRight, direction=Direction.Down
        )
        self.bus_comm.check_extr_mirr_adj_req(ViewPos.RearRight, MirrDirReq.Down)

    @allure.title("左后视镜向右调节")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1960091(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.hmi_set_start_adjust_viewmirror(
            viewPos=ViewPos.RearLeft, direction=Direction.Right
        )
        self.bus_comm.check_extr_mirr_adj_req(ViewPos.RearLeft, MirrDirReq.Right)

    @allure.title("左后视镜向左调节")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1960093(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.hmi_set_start_adjust_viewmirror(
            viewPos=ViewPos.RearLeft, direction=Direction.Left
        )
        self.bus_comm.check_extr_mirr_adj_req(ViewPos.RearLeft, MirrDirReq.Left)

    @allure.title("左后视镜向上调节")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1960094(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.hmi_set_start_adjust_viewmirror(
            viewPos=ViewPos.RearRight, direction=Direction.Left
        )
        self.bus_comm.check_extr_mirr_adj_req(ViewPos.RearLeft, MirrDirReq.Left)

    @allure.title("左后视镜向下调节")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1960092(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.hmi_set_start_adjust_viewmirror(
            viewPos=ViewPos.RearRight, direction=Direction.Left
        )
        self.bus_comm.check_extr_mirr_adj_req(ViewPos.RearLeft, MirrDirReq.Left)

    @allure.title("后视镜在折叠的情况下下翻")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1960095(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Fold)
        self.bus_comm.set_rear_view_direction(pos=ViewPos.All,direction=MirrDirReq.Idle)
        self.soa.hmi_set_start_adjust_viewmirror(viewPos=ViewPos.All,direction=Direction.Down)
        self.bus_comm.check_extr_mirr_adj_req(viewPos=ViewPos.All,req=MirrDirReq.Down)


    @allure.title("后视镜在展开的情况下下翻")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1960096(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.bus_comm.set_rear_view_direction(pos=ViewPos.All,direction=MirrDirReq.Idle)
        self.soa.hmi_set_start_adjust_viewmirror(viewPos=ViewPos.All,direction=Direction.Down)
        self.bus_comm.check_extr_mirr_adj_req(viewPos=ViewPos.All,req=MirrDirReq.Down)

    @allure.title("屏幕按钮点击外后视镜折叠")
    @pytest.mark.smoke
    def test_caseid_1960051(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.bus_comm.check_rear_view_autofold_req(req=AutoFoldReq.FoldIn)

    @allure.title("休眠唤醒_后视镜折叠")
    @pytest.mark.full
    def test_caseid_1994566(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.bus_comm.check_rear_view_autofold_req(req=AutoFoldReq.FoldIn)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.bus_comm.check_rear_view_autofold_req(req=AutoFoldReq.FoldIn)
        
    @allure.title("io重启_后视镜折叠")
    @pytest.mark.full
    def test_caseid_1994565(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.bus_comm.check_rear_view_autofold_req(req=AutoFoldReq.FoldIn)
        self.io.io_reset_bgm()
        sleep(3)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.bus_comm.check_rear_view_autofold_req(req=AutoFoldReq.FoldIn)

    @allure.title("诊断重启_后视镜折叠")
    @pytest.mark.full
    def test_caseid_1994564(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.bus_comm.check_rear_view_autofold_req(req=AutoFoldReq.FoldIn)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.bus_comm.check_rear_view_autofold_req(req=AutoFoldReq.FoldIn)
                
    @allure.title("屏幕按钮点击外后视镜展开")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1960052(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Fold)
        self.soa.hmi_set_rear_view_unfold(view_pos=ViewId.RearViewAll,is_auto=False)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)

    @allure.title("NFC闭锁后视镜自动折叠")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1960050(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.set_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.mix.set_common_precontion()
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_central_lock_event_sts(evn_update_sts=True, evn_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.soa.get_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)
        
    @allure.title("Telematics解锁后视镜自动展开")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1960036(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.io.set_five_door_sts(Door.close)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Fold)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.Telm)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)
        
    @allure.title("KeyRem解锁后视镜自动展开")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1960039(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.io.set_five_door_sts(Door.close)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Fold)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)
        
    @allure.title("NFC解锁后视镜自动展开")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1960049(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.io.set_five_door_sts(Door.close)
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Fold)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)
        
    @allure.title("主驾门Pe闭锁后视镜自动折叠")
    @pytest.mark.full
    def test_caseid_1960048(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.set_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.mix.set_common_precontion()
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.soa.get_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)

    @allure.title("副驾门Pe闭锁后视镜自动折叠")
    @pytest.mark.full
    def test_caseid_1960046(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.set_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.mix.set_common_precontion()
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.soa.get_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)
        
    @allure.title("左后门Pe闭锁后视镜自动折叠")
    @pytest.mark.full
    def test_caseid_1960044(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.set_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.mix.set_common_precontion()
        self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.soa.get_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)
        
    @allure.title("右后门Pe闭锁后视镜自动折叠")
    @pytest.mark.full
    def test_caseid_1960042(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.set_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.mix.set_common_precontion()
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.soa.get_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)

    @allure.title("KeyRem闭锁后视镜自动折叠")
    @pytest.mark.full
    def test_caseid_1960040(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.set_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.mix.set_common_precontion()
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.soa.get_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)

    @allure.title("Keyls落锁后视镜自动折叠")
    @pytest.mark.full
    def test_caseid_1960038(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.set_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.mix.set_common_precontion()
        self.io.set_hood_sts(HoodSts.Close)     
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.soa.get_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)

    @allure.title("Telematics落锁后视镜自动折叠")
    @pytest.mark.full
    def test_caseid_1960037(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.set_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.mix.set_common_precontion()
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.soa.get_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)

    @allure.title("后视镜折叠后整车下电，上电后保持折叠")
    @pytest.mark.full
    def test_caseid_1960032(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.bus_comm.check_rear_view_autofold_req(req=AutoFoldReq.FoldIn)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(10)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.bus_comm.check_rear_view_autofold_req(req=AutoFoldReq.FoldIn)
        
    @allure.title("触发哨兵模式后视镜折叠禁用")
    @pytest.mark.full
    def test_caseid_1960033(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.On)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.soa.send_event_notify("SentryModeService_client", "NotifySentryModeSts", {"sentryModeSts":{"mainSts":1,"workSts":1}})
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)
        
    @allure.title("进入洗车模式后视镜自动折叠")
    @pytest.mark.full
    def test_caseid_1960035(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.soa.set_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.soa.hmi_set_wash_mode(isOn.On)
        self.soa.get_rearview_autosts(view_pos=ViewId.RearViewAll,sts=True)
                                     
    @allure.title("主驾门Pe解锁后视镜自动展开")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1960047(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Fold)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        self.bus_comm.set_blue_id_type_sts(key_id=2,type=BlueType.BLE_Key,con_sts=ConnSts.Connect)
        # self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrOpenReqOutdSwt2 ", 1)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=1)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)

    @allure.title("副驾门Pe解锁后视镜自动展开")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1960045(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Fold)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        self.bus_comm.set_blue_id_type_sts(key_id=2,type=BlueType.BLE_Key,con_sts=ConnSts.Connect)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=1)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)
        
    @allure.title("左后门Pe解锁后视镜自动展开")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1960043(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Fold)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        self.bus_comm.set_blue_id_type_sts(key_id=2,type=BlueType.BLE_Key,con_sts=ConnSts.Connect)
        # self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DoorLeReOpenReqOutdSwt2", 1)
        self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=1)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)
        
    @allure.title("右后门Pe解锁后视镜自动展开")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1960041(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Fold)
        self.soa.hmi_set_rear_view_fold(view_pos=ViewId.RearViewAll,is_auto=True)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        self.bus_comm.set_blue_id_type_sts(key_id=2,type=BlueType.BLE_Key,con_sts=ConnSts.Connect)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=1)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)

    @allure.title("退出洗车模式后视镜自动展开")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1960034(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_wash_mode(isOn.On)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Fold)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.soa.hmi_set_wash_mode(isOn.Off)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)
        
    @allure.title("休眠唤醒_主驾目标角度")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1987110(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.bus_comm.set_rearview_angle(left_horizon=100.0,left_vertical=58.0)
        self.soa.set_viewmirror_angle(viewPos=ViewPos.RearLeft,hori_angle=100.0,vert_angle=58.0)
        self.soa.get_viewmirror_angle(views=ViewPos.RearLeft,viewPos=ViewPos.RearLeft,hori_angle=100.0,vert_angle=58.0)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.soa.get_viewmirror_angle(views=ViewPos.RearLeft,viewPos=ViewPos.RearLeft,hori_angle=100.0,vert_angle=58.0)
        
    @allure.title("休眠唤醒_副驾目标角度")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1987111(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.bus_comm.set_rearview_angle(right_horizon=100.0,right_vertical=58.0)
        self.soa.set_viewmirror_angle(viewPos=ViewPos.RearRight,hori_angle=100.0,vert_angle=58.0)
        self.soa.get_viewmirror_angle(views=ViewPos.RearRight,viewPos=ViewPos.RearRight,hori_angle=100.0,vert_angle=58.0)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.soa.get_viewmirror_angle(views=ViewPos.RearRight,viewPos=ViewPos.RearRight,hori_angle=100.0,vert_angle=58.0)

    @allure.title("诊断重启_主驾目标角度")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994551(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.bus_comm.set_rearview_angle(left_horizon=100.0,left_vertical=58.0)
        self.soa.set_viewmirror_angle(viewPos=ViewPos.RearLeft,hori_angle=100.0,vert_angle=58.0)
        self.soa.get_viewmirror_angle(views=ViewPos.RearLeft,viewPos=ViewPos.RearLeft,hori_angle=100.0,vert_angle=58.0)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        sleep(15)
        self.soa.get_viewmirror_angle(views=ViewPos.RearLeft,viewPos=ViewPos.RearLeft,hori_angle=100.0,vert_angle=58.0)
        
    @allure.title("诊断重启_副驾目标角度")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994552(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.bus_comm.set_rearview_angle(right_horizon=100.0,right_vertical=58.0)
        self.soa.set_viewmirror_angle(viewPos=ViewPos.RearRight,hori_angle=100.0,vert_angle=58.0)
        self.soa.get_viewmirror_angle(views=ViewPos.RearRight,viewPos=ViewPos.RearRight,hori_angle=100.0,vert_angle=58.0)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        sleep(15)
        self.soa.get_viewmirror_angle(views=ViewPos.RearRight,viewPos=ViewPos.RearRight,hori_angle=100.0,vert_angle=58.0)

    @allure.title("io重启_主驾目标角度")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994553(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.bus_comm.set_rearview_angle(left_horizon=100.0,left_vertical=58.0)
        self.soa.set_viewmirror_angle(viewPos=ViewPos.RearLeft,hori_angle=100.0,vert_angle=58.0)
        sleep(3)
        self.soa.get_viewmirror_angle(views=ViewPos.RearLeft,viewPos=ViewPos.RearLeft,hori_angle=100.0,vert_angle=58.0)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_viewmirror_angle(views=ViewPos.RearLeft,viewPos=ViewPos.RearLeft,hori_angle=100.0,vert_angle=58.0)
        
    @allure.title("io重启_副驾目标角度")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994554(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.bus_comm.set_rearview_angle(right_horizon=100.0,right_vertical=58.0)
        self.soa.set_viewmirror_angle(viewPos=ViewPos.RearRight,hori_angle=100.0,vert_angle=58.0)
        sleep(3)
        self.soa.get_viewmirror_angle(views=ViewPos.RearRight,viewPos=ViewPos.RearRight,hori_angle=100.0,vert_angle=58.0)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_viewmirror_angle(views=ViewPos.RearRight,viewPos=ViewPos.RearRight,hori_angle=100.0,vert_angle=58.0)

    @allure.title("休眠唤醒_后视镜展开")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994563(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_rear_view_unfold(view_pos=ViewId.RearViewAll,is_auto=False)
        sleep(15)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)
                
    @allure.title("io重启_后视镜展开")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994562(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_rear_view_unfold(view_pos=ViewId.RearViewAll,is_auto=False)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)
        
    @allure.title("诊断重启_后视镜展开")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994561(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.soa.hmi_set_rear_view_unfold(view_pos=ViewId.RearViewAll,is_auto=False)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.bus_comm.check_rear_view_fold_sts_req(req=FoldHmiReq.NotPsd)
        
    @allure.title("休眠唤醒_后视镜加热开启")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994560(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3,ccp={182: 5, 13: 4})
        self.soa.hmi_set_outview_heat_mode(sts=True)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",1)
        result_ori = self.bus_comm.check_signal_thread_stop('HmiDefrstrElecStsRe')  
        logger.info(f'获取到的原始数据HmiDefrstrElecStsRe为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",1)
        result_ori = self.bus_comm.check_signal_thread_stop('HmiDefrstrElecStsRe')  
        logger.info(f'获取到的原始数据HmiDefrstrElecStsRe为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        
    @allure.title("休眠唤醒_后视镜加热关闭")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994557(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3,ccp={182: 5, 13: 4})
        self.soa.hmi_set_outview_heat_mode(sts=False)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",0)
        result_ori = self.bus_comm.check_signal_thread_stop('HmiDefrstrElecStsRe')  
        logger.info(f'获取到的原始数据HmiDefrstrElecStsRe为{result_ori}')
        result = get_signal_times_interval(result_ori, 0)
        logger.info("期望值的统计结果:{}".format(result))
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",0)
        result_ori = self.bus_comm.check_signal_thread_stop('HmiDefrstrElecStsRe')  
        logger.info(f'获取到的原始数据HmiDefrstrElecStsRe为{result_ori}')
        result = get_signal_times_interval(result_ori, 0)
        logger.info("期望值的统计结果:{}".format(result))
        
    @allure.title("io重启_后视镜加热开启")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994559(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3,ccp={182: 5, 13: 4})
        self.soa.hmi_set_outview_heat_mode(sts=True)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",1)
        result_ori = self.bus_comm.check_signal_thread_stop('HmiDefrstrElecStsRe')  
        logger.info(f'获取到的原始数据HmiDefrstrElecStsRe为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",1)
        result_ori = self.bus_comm.check_signal_thread_stop('HmiDefrstrElecStsRe')  
        logger.info(f'获取到的原始数据HmiDefrstrElecStsRe为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        
    @allure.title("io重启_后视镜加热关闭")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994556(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3,ccp={182: 5, 13: 4})
        self.soa.hmi_set_outview_heat_mode(sts=False)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",0)
        result_ori = self.bus_comm.check_signal_thread_stop('HmiDefrstrElecStsRe')  
        logger.info(f'获取到的原始数据HmiDefrstrElecStsRe为{result_ori}')
        result = get_signal_times_interval(result_ori, 0)
        logger.info("期望值的统计结果:{}".format(result))
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",0)
        result_ori = self.bus_comm.check_signal_thread_stop('HmiDefrstrElecStsRe')  
        logger.info(f'获取到的原始数据HmiDefrstrElecStsRe为{result_ori}')
        result = get_signal_times_interval(result_ori, 0)
        logger.info("期望值的统计结果:{}".format(result))
        
    @allure.title("诊断重启_后视镜加热开启")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994558(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3,ccp={182: 5, 13: 4})
        self.soa.hmi_set_outview_heat_mode(sts=True)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",1)
        result_ori = self.bus_comm.check_signal_thread_stop('HmiDefrstrElecStsRe')  
        logger.info(f'获取到的原始数据HmiDefrstrElecStsRe为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",1)
        result_ori = self.bus_comm.check_signal_thread_stop('HmiDefrstrElecStsRe')  
        logger.info(f'获取到的原始数据HmiDefrstrElecStsRe为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        
    @allure.title("诊断重启_后视镜加热关闭")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994555(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3,ccp={182: 5, 13: 4})
        self.soa.hmi_set_outview_heat_mode(sts=False)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",0)
        result_ori = self.bus_comm.check_signal_thread_stop('HmiDefrstrElecStsRe')  
        logger.info(f'获取到的原始数据HmiDefrstrElecStsRe为{result_ori}')
        result = get_signal_times_interval(result_ori, 0)
        logger.info("期望值的统计结果:{}".format(result))
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",0)
        result_ori = self.bus_comm.check_signal_thread_stop('HmiDefrstrElecStsRe')  
        logger.info(f'获取到的原始数据HmiDefrstrElecStsRe为{result_ori}')
        result = get_signal_times_interval(result_ori, 0)
        logger.info("期望值的统计结果:{}".format(result))
        
    # @allure.title("4219")
    # @pytest.mark.full1
    # def test_caseid_1987617(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3,ccp={182: 3, 13: 4})
    #     self.bus_comm.set_singal("bodycan","PdmBodyFr03","AmbTRawAtPassSideQly",3)
    #     self.bus_comm.set_singal("bodycan","PdmBodyFr03","AmbTRawAtPassSideAmbTVal",10.0)
    #     self.soa.hmi_set_outview_heat_mode(sts=True)
    #     sleep(10)
    #     self.bus_comm.check_singal("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",1)
    #     # self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",1)
    #     # result_ori = self.bus_comm.check_signal_thread_stop('HmiDefrstrElecStsRe')  
    #     # logger.info(f'获取到的原始数据HmiDefrstrElecStsRe为{result_ori}')
    #     # result = get_signal_times_interval(result_ori, 1)
    #     # logger.info("期望值的统计结果:{}".format(result))
    #     sleep(3)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0x19],recv=[0x62, 0x42,0x19,0x01])
               
    # @allure.title("421A")
    # @pytest.mark.full
    # def test_caseid_1987618(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3,ccp={182: 5, 13: 4})        
    #     self.soa.hmi_set_outview_heat_mode(sts=True)
    #     self.bus_comm.check_signal_thread_start("backbonefr","CemBackBoneFr19","HmiDefrstrElecStsRe",1)
    #     result_ori = self.bus_comm.check_signal_thread_stop('HmiDefrstrElecStsRe',timeout=2)  
    #     logger.info(f'获取到的原始数据HmiDefrstrElecStsRe为{result_ori}')
    #     result = get_signal_times_interval(result_ori, 1)
    #     logger.info("期望值的统计结果:{}".format(result))
    #     sleep(3)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0x1A],recv=[0x62, 0x42,0x1A,0x01])     
