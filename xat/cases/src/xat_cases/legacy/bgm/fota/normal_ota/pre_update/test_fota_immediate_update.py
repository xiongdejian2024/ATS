import os
import sys
import pytest
import allure
from time import sleep
import random

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common.common import set_bench_vlan9_ip

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("VehicleSetStatusService","client"),
                         ("InteractiveService","server"),
                         ("CentralLockService","client"),
                         ("VehicleModeService","client"),
                         ("HighVoltageService","client"),
                        #  ("UpdateAgentService","server","CDC_UA_Service")
                        #  ("UpdateAgentService","server","ACU_UA_Service") #待jiabin解决 启同一个server 俩个不同有效实例报错的问题
                         ])
        self.soa.start_send_InteractiveService_response()
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])

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
                                    FOTA_Skip_Debug.cdc_acu_doip_check
                                    ]) 
        self.ssh.update_ua_skip(DOMAIN.BGM, False)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
                    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.io.tcam_power_on()
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("升级前状态检查_非过桥任务_TCAM_DOIP未连接_检查不通过_上传ErrorCode_0x04_0x15") 
    def test_fota_caseid_1988584(self): 
        try:    
            self.mix.set_normal_fota_update_condition_new(vehspd=0, gear=Gear.Park,  display_hv_soc=80, thermaloutofcontrol=False, low_volt_soc=70, is_jidu_charger=False,
                                                        local_diag_sts=DiagActLineSts.DisActive, usage_mode=UsageMode.CONVENIENCE, is_hw_ver_match=True, maintenance_mode_sts=False,
                                                        park_comfort_mode_sts=False, pet_mode_sts="0")
            self.io.tcam_power_off()
            sleep(20)
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0415"', timeout=120):
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        finally:
            pass
            self.io.tcam_power_on()
            sleep(300)#等待TCAM恢复
        
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("升级前状态检查_非过桥任务_ACU_DOIP未连接_检查不通过_上传ErrorCode_0x04_0x15") 
    def test_fota_caseid_1988585(self): 
        # self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=250, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
        # self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        # self.mix.update_version_debug(self.taskid, [DOMAIN.ACU])
        # self.soa.start_send_ua_response(DOMAIN.ACU)
        # self.soa.start_send_ua_event(DOMAIN.ACU, self.soa.pack_ua_event_args(UA_Sts.IDLE))
        # self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        # self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        # self.soa.ck_s2s_req_v20("UpdateAgentService_server_ACU_UA_Service", ["StartDownload"], timeout=600)
        # self.soa.change_ua_event_and_getstatus(DOMAIN.ACU, UA_Sts.READY_TO_INSTALL)
        # assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 300)
        # self.mix.set_normal_fota_update_condition_new(vehspd=0, gear=Gear.Park,  display_hv_soc=80, thermaloutofcontrol=False, low_volt_soc=70, is_jidu_charger=False,
        #                                               local_diag_sts=DiagActLineSts.DisActive, usage_mode=UsageMode.CONVENIENCE, is_hw_ver_match=True, maintenance_mode_sts=False,
        #                                               park_comfort_mode_sts=False, pet_mode_sts="0")
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0415"', timeout=600):
        #     self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        #     # assert FOTA_ConditionCheck_Code.CR_HWPN_ERROR.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        # assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
    #待jiabin解决 启同一个server 俩个不同有效实例报错的问题
        pass

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("升级前状态检查_检查不通过（非诊断令牌失败）_停发心跳") 
    def test_fota_caseid_1989677(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=0, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
        with self.log_manage.check_jetlog_by_keywords(log_type=" ARB_MGR:", unexpect_keywords='Received heart beat for FotaUpdate:fota update', timeout=20):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("升级前状态检查_检查不通过（诊断令牌失败）_停发心跳") 
    def test_fota_caseid_1989676(self): 
        self.mix.set_normal_fota_update_condition(vehspd=250, gear=Gear.Park, display_hv_soc=0, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.Active)
        with self.log_manage.check_jetlog_by_keywords(log_type=" ARB_MGR:", unexpect_keywords='Received heart beat for FotaUpdate:fota update', timeout=20):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 

    # @pytest.mark.V_1_4
    # @pytest.mark.smoke
    # @allure.title("升级前状态检查_检查通过") 
    # def test_fota_caseid_1982023(self): 
    #     self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=250, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
    #     self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
    #     assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.UPDATE.value 
    #     self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
    
    @allure.title("升级前状态检查_检查通过") 
    @pytest.mark.parametrize('hv_soc, lv_soc, usagemode, petmode', [
                              pytest.param(26, 71, UsageMode.ACTIVE, "255", id="1988291", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 71, UsageMode.DRIVING, "255", id="1988292", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 71, UsageMode.ABANDONED, "255", id="1988293", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 71, UsageMode.INACTIVE, "255", id="1988294", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 71, UsageMode.CONVENIENCE, "255", id="1988295", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              
                              pytest.param(25, 71, UsageMode.ACTIVE, "255", id="1988296", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 71, UsageMode.DRIVING, "255", id="1988297", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 71, UsageMode.ABANDONED, "255", id="1988298", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 71, UsageMode.INACTIVE, "255", id="1988299", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 71, UsageMode.CONVENIENCE, "255", id="1988300", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              
                              pytest.param(26, 70, UsageMode.ACTIVE, "255", id="1988301", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 70, UsageMode.DRIVING, "255", id="1988302", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 70, UsageMode.ABANDONED, "255", id="1988303", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 70, UsageMode.INACTIVE, "255", id="1988304", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 70, UsageMode.CONVENIENCE, "255", id="1988305", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              
                              pytest.param(25, 70, UsageMode.ACTIVE, "255", id="1988306", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 70, UsageMode.DRIVING, "255", id="1988307", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 70, UsageMode.ABANDONED, "255", id="1988308", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 70, UsageMode.INACTIVE, "255", id="1988309", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 70, UsageMode.CONVENIENCE, "255", id="1988310", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              
                              pytest.param(26, 71, UsageMode.ACTIVE, "1", id="1988311", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 71, UsageMode.DRIVING, "1", id="1988312", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 71, UsageMode.ABANDONED, "1", id="1988313", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 71, UsageMode.INACTIVE, "1", id="1988314", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 71, UsageMode.CONVENIENCE, "1", id="1988315", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              
                              pytest.param(25, 71, UsageMode.ACTIVE, "1", id="1988316", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 71, UsageMode.DRIVING, "1", id="1988317", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 71, UsageMode.ABANDONED, "1", id="1988318", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 71, UsageMode.INACTIVE, "1", id="1988319", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 71, UsageMode.CONVENIENCE, "1", id="1988320", marks=[pytest.mark.full, pytest.mark.V_2_0]),

                              pytest.param(26, 70, UsageMode.ACTIVE, "1", id="1988321", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 70, UsageMode.DRIVING, "1", id="1988322", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 70, UsageMode.ABANDONED, "1", id="1988323", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 70, UsageMode.INACTIVE, "1", id="1988324", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 70, UsageMode.CONVENIENCE, "1", id="1988325", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              

                              pytest.param(25, 70, UsageMode.ACTIVE, "1", id="1988326", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 70, UsageMode.DRIVING, "1", id="1988327", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 70, UsageMode.ABANDONED, "1", id="1988328", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 70, UsageMode.INACTIVE, "1", id="1988329", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 70, UsageMode.CONVENIENCE, "1", id="1988330", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              
                              pytest.param(26, 71, UsageMode.ACTIVE, "0", id="1988331", marks=[pytest.mark.full, pytest.mark.V_2_0]), # label correct
                              pytest.param(26, 71, UsageMode.DRIVING, "0", id="1988332", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 71, UsageMode.ABANDONED, "0", id="1988333", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 71, UsageMode.INACTIVE, "0", id="1988334", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 71, UsageMode.CONVENIENCE, "0", id="1988335", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              
                              pytest.param(25, 71, UsageMode.ACTIVE, "0", id="1988336", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 71, UsageMode.DRIVING, "0", id="1988337", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 71, UsageMode.ABANDONED, "0", id="1988338", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 71, UsageMode.INACTIVE, "0", id="1988339", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 71, UsageMode.CONVENIENCE, "0", id="1988340", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              
                              pytest.param(26, 70, UsageMode.ACTIVE, "0", id="1988341", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 70, UsageMode.DRIVING, "0", id="1988342", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 70, UsageMode.ABANDONED, "0", id="1988343", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 70, UsageMode.INACTIVE, "0", id="1988344", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(26, 70, UsageMode.CONVENIENCE, "0", id="1988345", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              
                              pytest.param(25, 70, UsageMode.ACTIVE, "0", id="1988346", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 70, UsageMode.DRIVING, "0", id="1988347", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 70, UsageMode.ABANDONED, "0", id="1988348", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 70, UsageMode.INACTIVE, "0", id="1988349", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(25, 70, UsageMode.CONVENIENCE, "0", id="1988350", marks=[pytest.mark.sanity, pytest.mark.V_2_0]),
                            ])
    def test_fota_caseid_(self, hv_soc, lv_soc, usagemode, petmode): 
        self.mix.set_normal_fota_update_condition_new(vehspd=0, gear=Gear.Park,  display_hv_soc=hv_soc, thermaloutofcontrol=False, low_volt_soc=lv_soc, is_jidu_charger=False,
                                                      local_diag_sts=DiagActLineSts.DisActive, usage_mode=usagemode, is_hw_ver_match=True, maintenance_mode_sts=False,
                                                      park_comfort_mode_sts=False, pet_mode_sts=petmode)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=15)
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        time.sleep(.5)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
                
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("升级前状态检查_检查不通过_诊断仪接入") 
    def test_fota_caseid_1985327(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=250, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.Active)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"040C"', timeout=20):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("升级前状态检查_检查不通过_立即升级_VMM处于Driving") 
    def test_fota_caseid_1982022(self): 
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
        self.mix.set_normal_fota_update_condition(vehspd=3, gear=Gear.Drv, display_hv_soc=240, thermaloutofcontrol=True, low_volt_soc=69, local_diag_sts=DiagActLineSts.DisActive)
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" fota:", keywords=[
                                                                                   '"stateCode":"032B"',
                                                                                   '"stateCode":"0406"',
                                                                                   '"stateCode":"0402"',
                                                                                   '"stateCode":"0403"',
                                                                                   '"stateCode":"0404"',
                                                                                   '"stateCode":"0405"'], timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal1)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("升级前状态检查_检查不通过_预约升级_VMM处于Active") 
    def test_fota_caseid_1982021(self): 
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=250, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
        appoint_time = self.mix.generate_fota_appointment_time()
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time})
        time.sleep(300)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"032B"', timeout=20):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal1)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
    
    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @allure.title("升级前状态检查_检查不通过_当前在宠物模式下_上报errorcode_0x0411") 
    def test_fota_caseid_1988588(self): 
        self.mix.set_normal_fota_update_condition_new(vehspd=0, gear=Gear.Park,  display_hv_soc=80, thermaloutofcontrol=False, low_volt_soc=70, is_jidu_charger=False,
                                                      local_diag_sts=DiagActLineSts.DisActive, usage_mode=UsageMode.CONVENIENCE, is_hw_ver_match=True, maintenance_mode_sts=False,
                                                      park_comfort_mode_sts=False, pet_mode_sts="2")        
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0411"', timeout=20):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert FOTA_ConditionCheck_Code.CR_PET_MODE_ERROR.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
    
    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @allure.title("升级前状态检查_检查不通过_当前在维修模式下_上报errorcode_0x0412") 
    def test_fota_caseid_1988627(self): 
        self.mix.set_normal_fota_update_condition_new(vehspd=0, gear=Gear.Park,  display_hv_soc=80, thermaloutofcontrol=False, low_volt_soc=70, is_jidu_charger=False,
                                                      local_diag_sts=DiagActLineSts.DisActive, usage_mode=UsageMode.CONVENIENCE, is_hw_ver_match=True, maintenance_mode_sts=True,
                                                      park_comfort_mode_sts=False, pet_mode_sts="0")        
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0412"', timeout=20):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert FOTA_ConditionCheck_Code.CR_MNTN_MODE_ERROR.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value

    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @allure.title("升级前状态检查_检查不通过_当前在维持上电模式下_上报errorcode_0x0413") 
    def test_fota_caseid_1988628(self): 
        self.mix.set_normal_fota_update_condition_new(vehspd=0, gear=Gear.Park,  display_hv_soc=80, thermaloutofcontrol=False, low_volt_soc=70, is_jidu_charger=False,
                                                      local_diag_sts=DiagActLineSts.DisActive, usage_mode=UsageMode.CONVENIENCE, is_hw_ver_match=True, maintenance_mode_sts=False,
                                                      park_comfort_mode_sts=True, pet_mode_sts="0")        
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0413"', timeout=20):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert FOTA_ConditionCheck_Code.CR_PARKING_COMFORT_MODE_ERROR.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
    
    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @allure.title("升级前状态检查_检查不通过_硬件版本号不匹配_上报errorcode_0x0410") 
    def test_fota_caseid_1988587(self): 
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        self.mix.update_version_debug(self.taskid, ['DDM'])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)   
             
        self.mix.set_normal_fota_update_condition_new(vehspd=0, gear=Gear.Park,  display_hv_soc=80, thermaloutofcontrol=False, low_volt_soc=70, is_jidu_charger=False,
                                                      local_diag_sts=DiagActLineSts.DisActive, usage_mode=UsageMode.CONVENIENCE, is_hw_ver_match=True, maintenance_mode_sts=False,
                                                      park_comfort_mode_sts=False, pet_mode_sts="0")        
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0410"', timeout=20):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert FOTA_ConditionCheck_Code.CR_HWPN_ERROR.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value  
    
    @pytest.mark.V_2_1
    @pytest.mark.sanity
    @allure.title("升级前状态检查_其他条件均满足_非集度私桩") 
    def test_fota_caseid_1992983(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=250, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
        self.bus_comm.set_fota_JiDUCharging(isConnect=True, isPrivate=False)     
        assert self.soa.send_request_and_return_resp("HighVoltageService_client", method_name="GetChargingInfo",args={})["out"]["isConnect"], "Charging not Connect"
        assert 3 not in self.soa.send_request_and_return_resp("HighVoltageService_client", method_name="getEquipmentInfo",args={})["out"]["equipmentTypes"]
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0409"', timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert FOTA_ConditionCheck_Code.CR_CHARGING_ERROR.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value

    @pytest.mark.V_2_1
    @pytest.mark.sanity
    @allure.title("升级前状态检查_其他条件均满足_集度私桩") 
    def test_fota_caseid_1992982(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=240, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
        self.bus_comm.set_fota_JiDUCharging(isConnect=True, isPrivate=True)   
        assert self.soa.send_request_and_return_resp("HighVoltageService_client", method_name="GetChargingInfo",args={})["out"]["isConnect"], "Charging not Connect"
        assert 3 in self.soa.send_request_and_return_resp("HighVoltageService_client", method_name="getEquipmentInfo",args={})["out"]["equipmentTypes"]  
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords='"stateCode":"0409"', timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value

    @pytest.mark.V_2_1
    @pytest.mark.sanity
    @allure.title("升级前状态检查_其他条件均满足_无充电桩") 
    def test_fota_caseid_1992981(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=240, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
        self.bus_comm.set_fota_JiDUCharging(isConnect=False, isPrivate=False)     
        assert not self.soa.send_request_and_return_resp("HighVoltageService_client", method_name="GetChargingInfo",args={})["out"]["isConnect"], "Charging not Connect"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords='"stateCode":"0409"', timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value

    @pytest.mark.V_2_1
    @pytest.mark.sanity
    @allure.title("升级前状态检查_FirstCheck_HVSOCLow_0x04_0x25(CR_CHARGING_ERROR)") 
    def test_fota_caseid_1992985(self):    
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0425', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.FirstCheck_NoJIDUCharger_0x04_0x25.value}}) 

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @allure.title("终极校验_其他条件均满足_放电_ErrorCode_0x04_0x16") 
    def test_fota_caseid_1995476(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=250, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
        self.bus_comm.set_fota_Discharging(isDischarging=True)
        assert self.soa.send_request_and_return_resp("HighVoltageService_client", method_name="GetChargingInfo",args={})["out"]["isDischarging"], "is not Discharging"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0416"', timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert FOTA_ConditionCheck_Code.CR_DISCHARGING_ERROR.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @allure.title("终极校验_其他条件均满足_不放电") 
    def test_fota_caseid_1995475(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=240, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
        self.bus_comm.set_fota_Discharging(isDischarging=False)
        assert not self.soa.send_request_and_return_resp("HighVoltageService_client", method_name="GetChargingInfo",args={})["out"]["isDischarging"], "is Discharging"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords='"stateCode":"0416"', timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端code_ReadytoUpdate(04F0)") 
    def test_fota_caseid_1983125(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=250, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
        self.mix.fota_back_to_idle()
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"04F0"', timeout=900):
            self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota_cdc(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("VehicleSetStatusService","client"),
                         ("InteractiveService","server"),
                         ("CentralLockService","client"),
                         ("VehicleModeService","client"),
                         ("HighVoltageService","client"),
                         ("UpdateAgentService","server","CDC_UA_Service")
                        #  ("UpdateAgentService","server","ACU_UA_Service") #待jiabin解决 启同一个server 俩个不同有效实例报错的问题
                         ])
        self.soa.start_send_InteractiveService_response()

        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect
                                    ]) 
        self.ssh.update_ua_skip(DOMAIN.BGM, False)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.soa.empty_all()
                    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.soa.stop_send_ua_event(DOMAIN.CDC)
        self.soa.stop_send_ua_response(DOMAIN.CDC)


    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("升级前状态检查_检查不通过_域控制器DOIP连接失败_上报errorcode_0x0415") 
    def test_fota_caseid_1988586(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=250, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
        self.mix.update_version_debug(self.taskid, [DOMAIN.CDC])
        self.soa.start_send_ua_response(DOMAIN.CDC)
        self.soa.start_send_ua_event(DOMAIN.CDC, self.soa.pack_ua_event_args(UA_Sts.IDLE))
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=600)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.READY_TO_INSTALL)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 300)
        self.mix.set_normal_fota_update_condition_new(vehspd=0, gear=Gear.Park,  display_hv_soc=80, thermaloutofcontrol=False, low_volt_soc=70, is_jidu_charger=False,
                                                      local_diag_sts=DiagActLineSts.DisActive, usage_mode=UsageMode.CONVENIENCE, is_hw_ver_match=True, maintenance_mode_sts=False,
                                                      park_comfort_mode_sts=False, pet_mode_sts="0")
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0415"', timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            # assert FOTA_ConditionCheck_Code.CR_HWPN_ERROR.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota_cdc_code(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        self.ssh.update_ua_skip(DOMAIN.BGM, False)
        self.mix.update_version_debug(self.taskid,[DOMAIN.CDC])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("VehicleSetStatusService","client"),
                         ("InteractiveService","server"),
                         ("CentralLockService","client"),
                         ("VehicleModeService","client"),
                         ("HighVoltageService","client"),
                         ("UpdateAgentService","server","CDC_UA_Service")
                        #  ("UpdateAgentService","server","ACU_UA_Service") #待jiabin解决 启同一个server 俩个不同有效实例报错的问题
                         ])
        self.soa.start_send_InteractiveService_response()
        self.io.bgm_diag_line_down()
        self.soa.empty_all()
                    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        try:
            self.soa.stop_send_ua_event(DOMAIN.CDC)
            self.soa.stop_send_ua_response(DOMAIN.CDC)
        except:
            assert False

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端code_PreUPSOAInitError(0332)") 
    def test_fota_caseid_1986140(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=250, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
        self.mix.update_version_debug(self.taskid, [DOMAIN.CDC])
        self.soa.start_send_ua_response(DOMAIN.CDC)
        self.soa.start_send_ua_event(DOMAIN.CDC, self.soa.pack_ua_event_args(UA_Sts.IDLE))
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=600)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.READY_TO_INSTALL)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 300)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0332"', timeout=900):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            self.soa.stop_send_ua_event(DOMAIN.CDC)
            self.soa.stop_send_ua_response(DOMAIN.CDC)
            self.soa.stop_soa()
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端code_FNSOAInitError(0331)") 
    def test_fota_caseid_1986141(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=250, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
        self.mix.update_version_debug(self.taskid, [DOMAIN.CDC])
        self.soa.start_send_ua_response(DOMAIN.CDC)
        self.soa.start_send_ua_event(DOMAIN.CDC, self.soa.pack_ua_event_args(UA_Sts.IDLE))
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=600)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.READY_TO_INSTALL)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 300)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "PreUpdate", timeout=180)
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          ua_update_sts=UA_UpdatedStatus.UPDATE_COMPLETE.value
                                                          )                        
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0333"', timeout=600):
            self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "Active", timeout=180)
            self.soa.stop_send_ua_event(DOMAIN.CDC)
            self.soa.stop_send_ua_response(DOMAIN.CDC)
            self.soa.stop_soa()

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端code_ACSOAInitError(0333)") 
    def test_fota_caseid_1986142(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=250, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
        self.mix.update_version_debug(self.taskid, [DOMAIN.CDC])
        self.soa.start_send_ua_response(DOMAIN.CDC)
        self.soa.start_send_ua_event(DOMAIN.CDC, self.soa.pack_ua_event_args(UA_Sts.IDLE))
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=600)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.READY_TO_INSTALL)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 300)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "PreUpdate", timeout=180)
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          ua_update_sts=UA_UpdatedStatus.UPDATE_COMPLETE.value
                                                          )                        
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0333"', timeout=600):
            self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "Active", timeout=180)
            self.soa.stop_send_ua_event(DOMAIN.CDC)
            self.soa.stop_send_ua_response(DOMAIN.CDC)
            self.soa.stop_soa()
                        
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota_CheckLevel(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
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
                                    FOTA_Skip_Debug.cdc_acu_doip_check
                                    ]) 
        self.ssh.update_ua_skip(DOMAIN.BGM, False)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])

        self.soa.update([("FotaMasterService","client"),
                         ("HighVoltageService","client"),
                         ])
        self.io.bgm_diag_line_down()
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
        self.soa.soa_partner.stop_single_partner("FotaMasterService_client")
        self.soa.soa_partner.stop_single_partner("HighVoltageService_client")
        time.sleep(30)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.sd_tester.reset_bgm()

    def after_class(self, ecu):
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service")])
        super().after_class(self, ecu)
        # self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)

    # @pytest.mark.V_2_2
    # @pytest.mark.full
    # @allure.title("终极校验_强校验条件_HighVoltageService_HV电池电量&&热失控&&充电桩&&放电_不响应method") 
    # def test_fota_caseid_1995482(self): 
    #     self.io.bgm_power_off()
    #     self.soa.update([("FotaMasterService","client"),
    #                      ("HighVoltageService","server"),
    #                      ])
    #     time.sleep(30)     
    #     self.io.bgm_power_on()
    #     time.sleep(30)     
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0404',
    #                                                                                '"stateCode":"0405',
    #                                                                                '"stateCode":"0409',
    #                                                                                '"stateCode":"0416',
    #                                                                                ], timeout=60):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)   
    #     self.soa.soa_partner.stop_single_partner("FotaMasterService_client")
    #     self.soa.soa_partner.stop_single_partner("HighVoltageService_server")

    # @pytest.mark.V_2_2
    # @pytest.mark.full
    # @allure.title("终极校验_强校验条件_HighVoltageService_HV电池电量&&热失控&&充电桩&&放电_服务未链接") 
    # def test_fota_caseid_1995481(self): 
    #     self.io.bgm_power_off()
    #     self.soa.update([("FotaMasterService","client"),
    #                      ("HighVoltageService","server"),
    #                      ])
    #     time.sleep(30)     
    #     self.io.bgm_power_on()
    #     time.sleep(30)     
    #     self.soa.soa_partner.stop_single_partner("HighVoltageService_server")
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0332',
    #                                                                                '"stateCode":"040D',
    #                                                                                ], timeout=270):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)   
    #     self.soa.soa_partner.stop_single_partner("FotaMasterService_client")
 
    # @pytest.mark.V_2_2
    # @pytest.mark.full
    # @allure.title("终极校验_强校验条件_ChassisService_车速&&档位_不响应method") 
    # def test_fota_caseid_1995477(self): 
    #     self.io.bgm_power_off()
    #     self.soa.update([("FotaMasterService","client"),
    #                      ("ChassisService","server"),
    #                      ])
    #     time.sleep(10)     
    #     self.io.bgm_power_on()
    #     time.sleep(30)     
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0402',
    #                                                                                '"stateCode":"0403',
    #                                                                                ], timeout=60):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)   
    #     self.soa.soa_partner.stop_single_partner("FotaMasterService_client")
    #     self.soa.soa_partner.stop_single_partner("ChassisService_server")

    # @pytest.mark.V_2_2
    # @pytest.mark.full
    # @allure.title("终极校验_强校验条件_LowVoltageService_小电池电量_服务未链接") 
    # def test_fota_caseid_1995484(self): 
    #     self.io.bgm_power_off()
    #     self.soa.update([("FotaMasterService","client"),
    #                      ("LowVoltageService","server"),
    #                      ])
    #     time.sleep(10)     
    #     self.io.bgm_power_on()
    #     time.sleep(30)     
    #     self.soa.soa_partner.stop_single_partner("LowVoltageService_server")       
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0406',
    #                                                                                ], timeout=270):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)   
    #     self.soa.soa_partner.stop_single_partner("FotaMasterService_client")
        
    # @pytest.mark.V_2_2
    # @pytest.mark.full
    # @allure.title("终极校验_弱校验条件_ VehicleSetStatusService_维修模式&&维持上电模式_不响应method") 
    # def test_fota_caseid_1995485(self): 
    #     self.io.bgm_power_off()
    #     self.soa.update([("FotaMasterService","client"),
    #                      ("VehicleSetStatusService","server"),
    #                      ])
    #     time.sleep(10)     
    #     self.io.bgm_power_on()
    #     time.sleep(30)     
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['"stateCode":"0412',
    #                                                                                         '"stateCode":"0413',
    #                                                                                         ], timeout=60):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)   
    #     self.soa.soa_partner.stop_single_partner("FotaMasterService_client")
    #     self.soa.soa_partner.stop_single_partner("VehicleSetStatusService_server")

    @pytest.mark.V_2_2
    @pytest.mark.full
    @allure.title("终极校验_弱校验条件_ interactiveservice_宠物模式_不响应method") 
    def test_fota_caseid_1995488(self): 
        self.io.bgm_power_off()
        self.soa.update([("FotaMasterService","client"),
                         ("InteractiveService","server"),
                         ])
        time.sleep(10)     
        self.io.bgm_power_on()
        time.sleep(30)     
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['"stateCode":"0411'
                                                                                            ], timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)   
        self.soa.soa_partner.stop_single_partner("FotaMasterService_client")
        self.soa.soa_partner.stop_single_partner("InteractiveService_server")

    @pytest.mark.V_2_2
    @pytest.mark.full
    @allure.title("终极校验_弱校验条件_ interactiveservice_宠物模式_服务未链接") 
    def test_fota_caseid_1995487(self): 
        self.io.bgm_power_off()
        self.soa.update([("FotaMasterService","client"),
                         ("InteractiveService","server"),
                         ])
        time.sleep(10)     
        self.io.bgm_power_on()
        time.sleep(30)     
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['"stateCode":"0411'
                                                                                            ], timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)   
        self.soa.soa_partner.stop_single_partner("FotaMasterService_client")
        self.soa.soa_partner.stop_single_partner("InteractiveService_server")
        
if __name__ == "__main__":
    pass

    




