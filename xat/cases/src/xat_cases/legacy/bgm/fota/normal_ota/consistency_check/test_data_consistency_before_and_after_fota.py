import os
import sys
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *

@pytest.mark.fota_update
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("VehicleModeService", "client"),
                         ("VehicleSetStatusService", "client"),
                         ("OuterRearViewService", "client"),
                         ("LightService", "client"),
                         ("ClimateControlService", "client"),
                         ("WiperService", "client"),
                         ("KeyService", "client"),
                         ("TailWingService", "client"),
                         ("WindowAppService", "client"),
                         ("CentralLockService","client")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        self.ssh.update_ua_skip(DOMAIN.BGM, True)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.mix.set_enter_boot_condition(UsageMode.CONVENIENCE, low_volt_power=14, vehspd=0)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front, WiperMode.Off)
        sleep(1)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.io.bgm_diag_line_down()
        
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        
    def after_class(self, ecu):
        super().after_class(self, ecu) 

    @pytest.mark.V_2_0
    @pytest.mark.smoke
    @allure.title("FOTA前后数据一致性检查-DID值比对-成功") 
    def test_fota_caseid_1989831(self):
        check_did_list = ["f190", "f106", "f18c", "ed20", "f1ae", "f1aa", "f1ab"]
        before_fota_data = dict.fromkeys(check_did_list, "before_data")
        before_fota_data["f190"] = self.sd_tester.read_did_and_check([TA.BGM_SOC,TA.BGM_MCU],0xF190,SESSION.DEFAULT,check_data=['62f190','62f190'],check_length=40)
        before_fota_data["f106"] = self.sd_tester.read_did_and_check(TA.BGM_MCU,0xf106,SESSION.DEFAULT,'62f106',check_length=3122)
        before_fota_data["f18c"] = self.sd_tester.read_did_and_check([TA.BGM_SOC,TA.BGM_MCU],0xF18C,SESSION.DEFAULT,['62f18c','62f18c'],check_length=14)
        before_fota_data["ed20"] = self.sd_tester.read_did_and_check([TA.BGM_SOC,TA.BGM_MCU],0xED20,SESSION.DEFAULT,[f'62ed20f1aa',f'62ed20f1aa'])
        before_fota_data["f1ae"] = self.sd_tester.read_did_and_check(TA.BGM_SOC,0xf1ae,SESSION.DEFAULT,'62f1ae',check_length=40) 
        before_fota_data["f1aa"] = self.sd_tester.read_did_and_check([TA.BGM_SOC,TA.BGM_MCU],0xf1aa,SESSION.DEFAULT,['62f1aa','62f1aa'],check_length=[22,22])
        before_fota_data["f1ab"] = self.sd_tester.read_did_and_check([TA.BGM_SOC,TA.BGM_MCU],0xf1ab,SESSION.DEFAULT,['62f1ab','62f1ab'],check_length=[22,22])
        logger.info(before_fota_data)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        after_fota_data = dict.fromkeys(check_did_list, "after_data")
        after_fota_data["f190"] = self.sd_tester.read_did_and_check([TA.BGM_SOC,TA.BGM_MCU],0xF190,SESSION.DEFAULT,check_data=['62f190','62f190'],check_length=40)
        after_fota_data["f106"] = self.sd_tester.read_did_and_check(TA.BGM_MCU,0xf106,SESSION.DEFAULT,'62f106',check_length=3122)
        after_fota_data["f18c"] = self.sd_tester.read_did_and_check([TA.BGM_SOC,TA.BGM_MCU],0xF18C,SESSION.DEFAULT,['62f18c','62f18c'],check_length=14)
        after_fota_data["ed20"] = self.sd_tester.read_did_and_check([TA.BGM_SOC,TA.BGM_MCU],0xED20,SESSION.DEFAULT,[f'62ed20f1aa',f'62ed20f1aa'])
        after_fota_data["f1ae"] = self.sd_tester.read_did_and_check(TA.BGM_SOC,0xf1ae,SESSION.DEFAULT,'62f1ae',check_length=40)
        after_fota_data["f1aa"] = self.sd_tester.read_did_and_check([TA.BGM_SOC,TA.BGM_MCU],0xf1aa,SESSION.DEFAULT,['62f1aa','62f1aa'],check_length=[22,22])
        after_fota_data["f1ab"] = self.sd_tester.read_did_and_check([TA.BGM_SOC,TA.BGM_MCU],0xf1ab,SESSION.DEFAULT,['62f1ab','62f1ab'],check_length=[22,22])
        logger.info(after_fota_data)
        assert sorted(before_fota_data.items()) == sorted(after_fota_data.items())

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_智能补电参数默认") 
    def test_fota_caseid_1995456(self):
        self.sd_tester.read_bms_did_value(0xBB00, "4b", default_mode=True)
        self.sd_tester.read_bms_did_value("0xbb02", "4b", default_mode=True)
        self.sd_tester.read_bms_did_value(0xBB04, "8C", default_mode=True)
        self.sd_tester.read_bms_did_value(0xBB06, "0032", default_mode=True)
        self.sd_tester.read_bms_did_value(0xBB08, "01F4", default_mode=True)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        self.sd_tester.read_bms_did_value(0xBB00, "4b", default_mode=True)
        self.sd_tester.read_bms_did_value("0xbb02", "4b", default_mode=True)
        self.sd_tester.read_bms_did_value(0xBB04, "8C", default_mode=True)
        self.sd_tester.read_bms_did_value(0xBB06, "0032", default_mode=True)
        self.sd_tester.read_bms_did_value(0xBB08, "01F4", default_mode=True)

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_VMM_展车模式记忆") 
    def test_fota_caseid_1992566(self):
        self.bus_comm.set_epb_sts(sts=3)
        self.mix.set_and_check_exhibition_mode(status=True)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        self.mix.check_exhibition_mode(status=True)

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_VMM_维修模式记忆") 
    def test_fota_caseid_1995457(self):
        self.bus_comm.set_epb_sts(sts=3)
        self.soa.set_and_check_maintain_mode(status=True)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        self.soa.check_maintain_mode(status=True)

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_后视镜_后视镜角度一致") 
    def test_fota_caseid_1995458(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,vehmtnst=VehMtnSts.StandStillVal3)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All,mode=MirrStsTyp.Unfold)
        self.bus_comm.set_rearview_angle(left_horizon=100,left_vertical=58)
        self.soa.set_viewmirror_angle(viewPos=ViewPos.RearLeft,hori_angle=100,vert_angle=58)
        self.soa.get_viewmirror_angle(views=ViewPos.RearLeft,viewPos=ViewPos.RearLeft,hori_angle=100,vert_angle=58)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        sleep(5)
        self.soa.get_viewmirror_angle(views=ViewPos.RearLeft,viewPos=ViewPos.RearLeft,hori_angle=100,vert_angle=58)

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_外灯_Off") 
    def test_fota_caseid_1995459(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        self.soa.event_check_extilight_mode(mode=ExteriorLightMode.Off)

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_外灯_Auto") 
    def test_fota_caseid_1995460(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        self.soa.event_check_extilight_mode(mode=ExteriorLightMode.Auto)

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_外灯_On") 
    def test_fota_caseid_1995461(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        self.soa.event_check_extilight_mode(mode=ExteriorLightMode.LowHeam)

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_内灯_Off") 
    def test_fota_caseid_1995462(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.soa.get_internal_light_mode(LightMode.Off)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        self.soa.get_internal_light_mode(LightMode.Off)

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_内灯_Auto") 
    def test_fota_caseid_1995463(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.soa.get_internal_light_mode(LightMode.Auto)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        self.soa.get_internal_light_mode(LightMode.Auto)

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_内灯_On") 
    def test_fota_caseid_1995464(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.soa.get_internal_light_mode(LightMode.On)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        self.soa.get_internal_light_mode(LightMode.On)

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_尾翼_尾翼状态一致") 
    def test_fota_caseid_1995465(self):
        self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x2})
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(1)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd',timeout=15) 
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')   
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] ==0

    @pytest.mark.V_2_0
    @pytest.mark.full1
    @allure.title("FOTA前后数据一致性检查_空调_Manual") 
    def test_fota_caseid_1995466(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        sleep(5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)

    @pytest.mark.V_2_0
    @pytest.mark.full1
    @allure.title("FOTA前后数据一致性检查_空调_Auto") 
    def test_fota_caseid_1995467(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        sleep(5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_雨刮_雨刮模式") 
    def test_fota_caseid_1995468(self):
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front, WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_雨刮_雨刮维修激活") 
    def test_fota_caseid_1995469(self):
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        self.soa.get_wiper_maintaince_pos(isOn.On)

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_雨刮_雨刮维修关闭") 
    def test_fota_caseid_1995470(self):
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        self.soa.get_wiper_maintaince_pos(isOn.Off)

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_解闭锁成功触发源") 
    def test_fota_caseid_1995471(self):
        LockgCenStsTrigSrcBefore = self.bus_comm.ipdu.get_recent_signal_raw_value(self.bus_comm.ipdu.connectivitycanfd.VgmConnFr12,
                                                              'LockgCenStsTrigSrc')
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        LockgCenStsTrigSrcAfter = self.bus_comm.ipdu.get_recent_signal_raw_value(self.bus_comm.ipdu.connectivitycanfd.VgmConnFr12,
                                                              'LockgCenStsTrigSrc')
        assert LockgCenStsTrigSrcBefore == LockgCenStsTrigSrcAfter, "FOTA前后数据一致性检查_解闭锁成功触发源FOTA前后不一致"

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("FOTA前后数据一致性检查_锁状态") 
    def test_fota_caseid_1995472(self):
        LockgCenStsLockStBefore = self.bus_comm.ipdu.get_recent_signal_raw_value(self.bus_comm.ipdu.connectivitycanfd.VgmConnFr12,
                                                              'LockgCenStsLockSt')
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        LockgCenStsLockStAfter = self.bus_comm.ipdu.get_recent_signal_raw_value(self.bus_comm.ipdu.connectivitycanfd.VgmConnFr12,
                                                              'LockgCenStsLockSt')
        assert LockgCenStsLockStBefore == LockgCenStsLockStAfter, "FOTA前后数据一致性检查_锁状态FOTA前后不一致"

    @pytest.mark.V_2_0
    @pytest.mark.full
    @pytest.mark.windows
    @allure.title("FOTA前后数据一致性检查_车窗_锁车自动关窗开启") 
    def test_fota_caseid_1995473(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.io.set_five_door_sts(Door.close)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        self.bus_comm.check_multiple_signals_thread_start([("bodycan",'CemBodyFr68','WinOpenDrvrReq',1), ("bodycan",'CemBodyFr68','WinOpenPassReq',1), ("bodycan",'CemBodyFr68','WinOpenReLeReq',1), ("bodycan",'CemBodyFr68','WinOpenReRiReq',1)],timeout=15)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.Telm)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        result = self.bus_comm.check_multiple_signals_thread_stop("CemBodyFr68")
        logger.info(f'获取到的原始数据为{result}')
        assert result


    @pytest.mark.V_2_0
    @pytest.mark.full
    @pytest.mark.windows
    @allure.title("FOTA前后数据一致性检查_车窗_雨天自动关窗开启") 
    def test_fota_caseid_1995474(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.io.set_five_door_sts(Door.close)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.Telm)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(True)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @allure.title("fota升级_Auto_关闭ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995712(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.set_eco_sts(sts=False)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off) 

    @allure.title("fota升级_Manual_关闭ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995713(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.set_eco_sts(sts=False)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)

    @allure.title("fota升级_Off_关闭ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995715(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.soa.set_eco_sts(sts=True)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)

    @allure.title("fota升级_Off_打开ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995714(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.soa.set_eco_sts(sts=True)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)

    @allure.title("fota升级_Manual_打开ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995711(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.set_eco_sts(sts=False)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)

    @allure.title("fota升级_Auto_打开ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995710(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.set_eco_sts(sts=True)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)

    