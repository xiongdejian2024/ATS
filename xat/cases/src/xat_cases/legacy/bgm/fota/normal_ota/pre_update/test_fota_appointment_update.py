import os
import sys
import pytest
import allure
from time import sleep
import random
import copy
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([
            ("FotaMasterService","client"),
            ("UpdateAgentService","client","BGM_UA_Service"),
            ("RtcAlarmService","client"),
            ("AcuModeManagerService","server"),
            ("VehicleSetStatusService","client"),
            ("InteractiveService","server"),
            ("CentralLockService","client"),
            ("VehicleModeService","client"),
            ("HighVoltageService","client"),
            ])
        
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
                                    FOTA_Skip_Debug.start_download,
                                    FOTA_Skip_Debug.update_precondition_check
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
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
    
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("HMI任务发布") 
    def test_fota_caseid_1982047(self):  
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value   
         
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("立即升级_Active阶段触发") 
    def test_fota_caseid_1982046(self):  
        # 确保FOTA当前状态为ACTIVE
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA当前状态不为ACTIVE，无法启动升级"
        # 发送FOTA升级请求
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        time.sleep(8) #FOTA Master 收到StartUpdate请求后，会进入条件检测，待检测通过后，状态机才会切为UPDATE
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.UPDATE.value
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota) #进入pre_update后 取消fota，避免进入升级后，单case执行时间过长
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("立即升级-BGM在QUERY状态下收到StartUpdate请求，忽略处理") 
    def test_fota_caseid_1994267(self):  
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_START_UPDATE discarded', timeout=30):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("立即升级-BGM在IDLE状态下收到StartUpdate请求，忽略处理") 
    def test_fota_caseid_1994266(self):  
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_START_UPDATE discarded', timeout=30):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("立即升级-BGM在NEW_TASK状态下收到StartUpdate请求，忽略处理") 
    def test_fota_caseid_1994265(self):  
        try:
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
            self.sd_tester.reset_bgm()
            self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_START_UPDATE discarded', timeout=30):
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value
        finally:
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
                                    FOTA_Skip_Debug.start_download,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ])     

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("立即升级-BGM在DOWNLOADING状态下收到StartUpdate请求，忽略处理") 
    def test_fota_caseid_1994264(self): 
        try:
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
            self.sd_tester.reset_bgm()
            self.mix.back_fota_to(FOTAMasteSts.DOWNLOADING, taskid=self.taskid)
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_START_UPDATE discarded', timeout=30):
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value
        finally:
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
                                    FOTA_Skip_Debug.start_download,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ])

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("立即升级-BGM在UPDATE状态下收到StartUpdate请求，忽略处理") 
    def test_fota_caseid_1994263(self):  
        self.mix.back_fota_to(FOTAMasteSts.UPDATE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_START_UPDATE discarded', timeout=30):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.UPDATE.value
        self.sd_tester.diag_cancel()

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("立即升级-BGM在FAILED_NOT_DRIVING状态下收到StartUpdate请求，忽略处理") 
    def test_fota_caseid_1994259(self):  
        self.mix.back_fota_to(FOTAMasteSts.FAILED_NOT_DRIVING, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_START_UPDATE discarded', timeout=30):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("立即升级-BGM在RESCUE状态下收到StartUpdate请求，忽略处理") 
    def test_fota_caseid_1994258(self):  
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_START_UPDATE discarded', timeout=30):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.UPDATE.value
        self.sd_tester.diag_cancel()        

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("立即升级_非Active阶段触发") 
    def test_fota_caseid_1982045(self):  
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value        

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("预约升级_非Active阶段触发") 
    def test_fota_caseid_1982043(self):  
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=60)}  # appointmenttime固定为当前时间1分钟后
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='DoActionBeforeDiscardEvent:event EVENT_SET_APPOINTMENT discarded', timeout=120):
            self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        

           
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("预约升级_Active阶段设置_同一任务_无预约_发送成功") 
    def test_fota_caseid_1982044(self): 
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=300)}  # time固定为当前时间5min后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        assert self.soa.get_fota_NotifyAppointTime(MASTER_NotifyAppointTime_EVENT.AppointmentTime) == args.get("time") and self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='SetBookEvent:rt:0', unexpect_keywords='failed to SetBookEvent', timeout=60)
    
    @pytest.mark.V_2_1_ONLY
    @pytest.mark.smoke
    @allure.title("车机预约升级_Active阶段_同一任务_无预约_发送成功") 
    def test_fota_caseid_1990249(self):      
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=240, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)        
        appoint_time = self.mix.generate_fota_appointment_time(delay_seconds=300)
        args={"taskId":self.taskid, "time":appoint_time}  # time固定为当前时间5min后
        self.soa.send_cancel_service_book_event(service_name="FotaMasterService")

        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args=args)
        time.sleep(5)
        real_update_time = self.soa.get_fota_notifybookinfolist(NotifyBookInfoListEVENT.startTime)
        assert ( real_update_time - appoint_time <= 540) and (real_update_time - appoint_time >= 0) and (appoint_time%60 == 0)
        assert self.soa.get_fota_NotifyAppointTime(MASTER_NotifyAppointTime_EVENT.AppointmentTime) == args.get("time") and self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='SetBookEvent:rt:0', unexpect_keywords='failed to SetBookEvent', timeout=60)

        # TODO，检查BGM记录RtcAlarmService.SetBookEvent中参数timerHandler(解析FOTA持久化文件state.pb中timerHandler)
        # TODO，检查BGM发送CallTspApi，其中参数appointmentTime=Time（Time为SetAppointment中传入的参数值Time）

    @pytest.mark.V_2_1_ONLY
    @pytest.mark.smoke
    @allure.title("车机预约升级_Active阶段_同一任务_无预约_发送成功_触发立即升级") 
    def test_fota_caseid_1990248(self):     
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=240, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
        appoint_time = self.mix.generate_fota_appointment_time(delay_seconds=60)
        args={"taskId":self.taskid, "time":appoint_time}  # time固定为当前时间5min后
        self.soa.send_cancel_service_book_event(service_name="FotaMasterService")

        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args=args)
        time.sleep(5)
        real_update_time = self.soa.get_fota_notifybookinfolist(NotifyBookInfoListEVENT.startTime)
        assert ( real_update_time - appoint_time <= 540) and (real_update_time - appoint_time >= 0) and (appoint_time%60 == 0)
        assert self.soa.get_fota_NotifyAppointTime(MASTER_NotifyAppointTime_EVENT.AppointmentTime) == args.get("time") and self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='SetBookEvent:rt:0', unexpect_keywords='failed to SetBookEvent', timeout=60)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)  
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=360)

    @pytest.mark.V_2_1_ONLY
    @allure.title("车机预约升级_到达预约时间_xmin内触发立即升级") 
    @pytest.mark.parametrize('delay_time', [
                              pytest.param(10, id="1990245", marks=[pytest.mark.full, pytest.mark.V_2_1]),
                              pytest.param(538, id="1990244", marks=[pytest.mark.full, pytest.mark.V_2_1]),
                              pytest.param(540, id="1990246", marks=[pytest.mark.sanity, pytest.mark.V_2_1]),
                              pytest.param(1, id="1990247", marks=[pytest.mark.smoke, pytest.mark.V_2_1]),
                            ])
    def test_fota_caseid_(self, delay_time): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=240, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)

        appoint_time = self.mix.generate_fota_appointment_time(delay_seconds=60)
        args={"taskId":self.taskid, "time":appoint_time}  # time固定为当前时间5min后
        
        self.soa.send_cancel_service_book_event(service_name="FotaMasterService")
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args=args)
        time.sleep(5)
        real_update_time = self.soa.get_fota_notifybookinfolist(NotifyBookInfoListEVENT.startTime)
        assert ( real_update_time - appoint_time <= 540) and (real_update_time - appoint_time >= 0) and (appoint_time%60 == 0)
        assert self.soa.get_fota_NotifyAppointTime(MASTER_NotifyAppointTime_EVENT.AppointmentTime) == args.get("time") and self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='SetBookEvent:rt:0', unexpect_keywords='failed to SetBookEvent', timeout=60)
        
        time.sleep((real_update_time - appoint_time) + delay_time) # sleep (real_update_time-appoint_time)时间后，使得预约时间到达，delay_time表示预约时间到达后等待的时间
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.REACH_APPOINTMENT.value, timeout=300)

        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['SetUsageModeUp', 'KeepAlive','VfcType :23'], timeout=360):
            sleep(2)
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)  
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=30)

    @pytest.mark.V_2_1_ONLY
    @allure.title("车机预约升级_到达预约时间_BGM调用SetAutoDrivingModeKeepAlive和VFC_Diagnostic持续6min") 
    def test_fota_caseid_1990240_1990241(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=240, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)

        appoint_time = self.mix.generate_fota_appointment_time(delay_seconds=60)
        args={"taskId":self.taskid, "time":appoint_time}  # time固定为当前时间5min后
        
        self.soa.send_cancel_service_book_event(service_name="FotaMasterService")
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args=args)
        time.sleep(5)
        real_update_time = self.soa.get_fota_notifybookinfolist(NotifyBookInfoListEVENT.startTime)
        assert ( real_update_time - appoint_time <= 540) and (real_update_time - appoint_time >= 0) and (appoint_time%60 == 0)
        assert self.soa.get_fota_NotifyAppointTime(MASTER_NotifyAppointTime_EVENT.AppointmentTime) == args.get("time") and self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='SetBookEvent:rt:0', unexpect_keywords='failed to SetBookEvent', timeout=60)
        
        time.sleep((real_update_time - appoint_time) + 540) # sleep (real_update_time-appoint_time)时间后，使得预约时间到达，delay_time表示预约时间到达后等待的时间
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.REACH_APPOINTMENT.value, timeout=300)

        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['KeepAlive','VfcType :23'], timeout=360):
            sleep(2)
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)  
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=30)

    @pytest.mark.V_2_1_ONLY
    @pytest.mark.full
    @allure.title("车机预约升级_到达预约时间_10min1s后触发立即升级") 
    def test_fota_caseid_1990243(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=240, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)

        appoint_time = self.mix.generate_fota_appointment_time(delay_seconds=60)
        args={"taskId":self.taskid, "time":appoint_time}  # time固定为当前时间5min后
        self.soa.send_cancel_service_book_event(service_name="FotaMasterService")

        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args=args)
        time.sleep(5)
        real_update_time = self.soa.get_fota_notifybookinfolist(NotifyBookInfoListEVENT.startTime)
        assert (real_update_time - appoint_time <= 540) and (real_update_time - appoint_time >= 0) and (appoint_time%60 == 0)
        assert self.soa.get_fota_NotifyAppointTime(MASTER_NotifyAppointTime_EVENT.AppointmentTime) == args.get("time") and self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='SetBookEvent:rt:0', unexpect_keywords='failed to SetBookEvent', timeout=60)
        
        time.sleep(real_update_time-appoint_time+601) #到达预约时间后，BGM delay 1min，总共超时时间为10min1s
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.ACTIVE.value, timeout=60)
        assert not self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['KeepAlive'], timeout=360) # 检查6min后停发唤醒报文
    
    @pytest.mark.V_2_1_ONLY
    @pytest.mark.full
    @allure.title("车机预约升级_Active阶段设置_同一任务_有预约时间不同_修改记录时间") 
    def test_fota_caseid_1990242(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=240, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)

        appoint_time = self.mix.generate_fota_appointment_time(delay_seconds=60)
        args={"taskId":self.taskid, "time":appoint_time}  # time固定为当前时间5min后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args=args)
        time.sleep(1)
        
        appoint_time_new = self.mix.generate_fota_appointment_time(delay_seconds=120)
        args_new={"taskId":self.taskid, "time":appoint_time_new}  # time固定为当前时间5min后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args=args_new)
        time.sleep(1)
        
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time_new, "Appiontment Information Error"
        assert self.soa.get_fota_NotifyAppointTime(MASTER_NotifyAppointTime_EVENT.AppointmentTime) == args_new.get("time") and self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='SetBookEvent:rt:0', unexpect_keywords='failed to SetBookEvent', timeout=60)
    
    @pytest.mark.V_2_1_ONLY
    @pytest.mark.full
    @allure.title("车机预约升级_BGM记录数据检查") 
    def test_fota_caseid_1992567(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=240, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
        appoint_time = self.mix.generate_fota_appointment_time(delay_seconds=60)
        
        args={"taskId":self.taskid, "time":appoint_time}  # time固定为当前时间5min后
        self.soa.send_cancel_service_book_event(service_name="FotaMasterService")
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args=args)
        time.sleep(5)
        real_update_time = self.soa.get_fota_notifybookinfolist(NotifyBookInfoListEVENT.startTime)
        
        args_real_time = {"taskId":self.taskid, "time":real_update_time} 
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args=args_real_time)
        time.sleep(5)
        
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == args_real_time.get("time") and self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='SetBookEvent:rt:0', unexpect_keywords='failed to SetBookEvent', timeout=60)
        
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("预约升级_Active阶段设置_同一任务_无预约_发送成功_触发立即升级") 
    def test_fota_caseid_1984601(self): 
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=300)}  # time固定为当前时间5min后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        time.sleep(2) #等待FOTA预约时间触发结束
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)  
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=360)
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("预约升级_Active阶段设置_同一任务_有预约时间不同_发送失败") 
    def test_fota_caseid_1982041(self): 
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=300) + 1}  # time固定为当前时间5min后+1,制造错误格式预约时间
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) != args.get("time") and self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='SetBookEvent: failed to SetBookEvent:', timeout=60)
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("预约升级_Active阶段设置_不同任务") 
    def test_fota_caseid_1982042(self): 
        args={"taskId":random.randint(0,self.taskid),"time":self.mix.generate_fota_appointment_time(delay_seconds=300)}  # appointmenttime固定为当前时间5分钟后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) != args.get("time")
    
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("预约升级_Active阶段取消_同一任务_有预约") 
    def test_fota_caseid_1982040(self): 
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=300)}  # appointmenttime固定为当前时间5分钟后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == args.get("time")
        time.sleep(2) #等待FOTA预约时间触发结束
        self.soa.send_fota_request(MASTER_REQUEST.CancelAppointment,args={"taskId":self.taskid})  
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) != args.get("time")
    
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("预约升级_Active阶段取消_不同任务_有预约") 
    def test_fota_caseid_1982037(self): 
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=300)}  # appointmenttime固定为当前时间5分钟后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        time.sleep(2)
        self.soa.send_fota_request(MASTER_REQUEST.CancelAppointment,args={"taskId":random.randint(0,self.taskid)})  
        assert self.soa.get_fota_NotifyAppointTime(MASTER_NotifyAppointTime_EVENT.AppointmentTime) == args.get("time")
    
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("预约升级_Reachappointment阶段取消_同一任务_有预约") 
    def test_fota_caseid_1982039(self): 
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=120)}  # appointmenttime固定为当前时间2分钟后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        # time.sleep(120)  #等待2分钟，进入Reachappointment状态
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.REACH_APPOINTMENT.value, timeout=720)
        self.soa.send_fota_request(MASTER_REQUEST.CancelAppointment,args={"taskId":self.taskid})  
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) != args.get("time")
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("预约升级_Reachappointment阶段取消_不同任务") 
    def test_fota_caseid_1982036(self): 
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=120)}  # appointmenttime固定为当前时间2分钟后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        # time.sleep(120)  #等待2分钟，进入Reachappointment状态
        # assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.REACH_APPOINTMENT.value, timeout=720)
        self.soa.send_fota_request(MASTER_REQUEST.CancelAppointment,args={"taskId":random.randint(0, self.taskid)})  
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == args.get("time")    

        
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("预约升级_非Active/Reachappointment阶段取消") 
    def test_fota_caseid_1982038(self): 
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=120)}  # appointmenttime固定为当前时间2分钟后
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.CancelAppointment,args={"taskId":self.taskid})  
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) != args.get("time")
        
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("预约升级_到达预约时间≤10min_超时>5min") 
    def test_fota_caseid_1982035(self): 
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=120)}  # appointmenttime固定为当前时间2分钟后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        # time.sleep(120)  #等待2分钟，进入Reachappointment状态
        # assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REACH_APPOINTMENT.value
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.REACH_APPOINTMENT.value, timeout=720)
        time.sleep(360)  #等待6分钟，退出Reachappointment状态
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
    
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("预约升级_到达预约时间_5分钟内触发立即升级") 
    def test_fota_caseid_1982034(self): 
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=120)}  # appointmenttime固定为当前时间2分钟后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        # time.sleep(120)  #等待2分钟，进入Reachappointment状态
        # assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REACH_APPOINTMENT.value
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.REACH_APPOINTMENT.value, timeout=720)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=30)
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("预约升级_到达预约时间>10min") 
    def test_fota_caseid_1982033(self): 
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=120)}  # appointmenttime固定为当前时间2分钟后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        time.sleep(20)
        self.io.bgm_power_off()
        time.sleep(720)  #等待12分钟，到达预约时间超过10分钟场景
        time.sleep(600)  #再等待10min，随机数
        self.io.bgm_power_on()
        time.sleep(30)  #等待BGM上电后的业务启动时间
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) != args.get("time")
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_Reach Appointment(04F4/04F2)") 
    def test_fota_caseid_1983087(self): 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"04F2"',
                                                                                   '"stateCode":"04F4"'], timeout=900):
            self.mix.back_fota_to(FOTAMasteSts.REACH_APPOINTMENT, taskid=self.taskid)        

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_Cancel Appointment(04F3)") 
    def test_fota_caseid_1983088(self): 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"04F3"'], timeout=900):
            args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=120)}  # appointmenttime固定为当前时间2分钟后
            self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
            # time.sleep(120)  #等待2分钟，进入Reachappointment状态
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.REACH_APPOINTMENT.value, timeout=720)
            self.soa.send_fota_request(MASTER_REQUEST.CancelAppointment,args={"taskId":self.taskid})  
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("夜间自动升级_到达预约时间_初级校验失败(0420/0421/0422)") 
    def test_fota_caseid_1983162(self):
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=120)}  # appointmenttime固定为当前时间2分钟后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0420',
                                                                                   '"stateCode":"0421',
                                                                                   '"stateCode":"0422',
                                                                                   '"stateCode":"0423'], timeout=180):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.FirstCheck_HVSOCLow_0x04_0x20.value}})
            self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.FirstCheck_NotInPark_0x04_0x21.value}})
            self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.FirstCheck_VehicleSpeed_0x04_0x22.value}})
            self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.UserChoosePause_0x04_0x23.value}})

    @pytest.mark.V_2_1_ONLY
    @allure.title("车机预约升级_到达预约时间_BGM发送VFC_Diagnostic报文超过6min_返回Active") 
    def test_fota_caseid_1992568(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=240, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)

        appoint_time = self.mix.generate_fota_appointment_time(delay_seconds=60)
        args={"taskId":self.taskid, "time":appoint_time}  # time固定为当前时间5min后

        self.soa.send_cancel_service_book_event(service_name="FotaMasterService")
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args=args)
        time.sleep(5)
        real_update_time = self.soa.get_fota_notifybookinfolist(NotifyBookInfoListEVENT.startTime)
        assert ( real_update_time - appoint_time <= 540) and (real_update_time - appoint_time >= 0) and (appoint_time%60 == 0)
        assert self.soa.get_fota_NotifyAppointTime(MASTER_NotifyAppointTime_EVENT.AppointmentTime) == args.get("time") and self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='VfcType :23', timeout=360)
        
        time.sleep((real_update_time - appoint_time) + 600) # sleep (real_update_time-appoint_time)时间后，使得预约时间到达，delay_time表示预约时间到达后等待的时间
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.ACTIVE.value, timeout=300)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("Active阶段多次设置/取消_发送成功") 
    def test_fota_caseid_1985165(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=120)}  # appointmenttime固定为当前时间2分钟后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == args.get("time")
        self.soa.send_fota_request(MASTER_REQUEST.CancelAppointment,args={"taskId":self.taskid})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) != args.get("time")
        sleep(2)
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == args.get("time")
        
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("预约升级_Active阶段多次设置_发送成功_上下电升级成功") 
    def test_fota_caseid_1985164(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=120)}  # appointmenttime固定为当前时间2分钟后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == args.get("time")
        self.soa.send_fota_request(MASTER_REQUEST.CancelAppointment,args={"taskId":self.taskid})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) != args.get("time")
        sleep(2)
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        self.sd_tester.reset_bgm()
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == args.get("time")        

    @pytest.mark.V_2_2
    @pytest.mark.full
    @allure.title("到达预约时间_随机(0-59)delaywork逻辑") 
    def test_fota_caseid_1996201(self): 
        args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=120)}  # appointmenttime固定为当前时间2分钟后
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['random_ms:'], timeout=190):        
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.REACH_APPOINTMENT.value, timeout=190)

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota_PatchTime(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([
            ("FotaMasterService","client"),
            ("UpdateAgentService","client","BGM_UA_Service"),
            ("RtcAlarmService","client"),
            ("V2TRoutingForwarder","client","V2TOTAFotaForwarder")
            ])
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
                                    FOTA_Skip_Debug.start_download,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.taskid_tmp = 99999 #赋值个平台不存在的taskid

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
                    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.mix.fota_back_to_idle()
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
    
    @pytest.mark.V_2_1
    @pytest.mark.sanity
    @allure.title("任务信息解析_type50_无appointPatchTime参数") 
    def test_fota_caseid_1996197(self):  
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data'].pop("appointPatchTime")
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.ACTIVE.value, timeout=600)
        appointment_time = self.mix.generate_fota_appointment_time(delay_seconds=120) # appointmenttime固定为当前时间2分钟后
        args={"taskId":self.taskid_tmp,"time":appointment_time}
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"04F2"',
                                                                                   'SetBookEvent:rt:0',
                                                                                   f'"appointmentTime":"{appointment_time}"'], unexpect_keywords=['failed to SetBookEvent'], timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid_tmp}) == appointment_time
        assert self.soa.get_fota_NotifyAppointTime(MASTER_NotifyAppointTime_EVENT.AppointmentTime) == appointment_time
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"04F4"',
                                                                                  f'"appointmentTime":"{appointment_time}"'], timeout=190):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.REACH_APPOINTMENT.value, timeout=190)

    @pytest.mark.V_2_1
    @pytest.mark.sanity
    @allure.title("任务信息解析_type50_appointPatchTime参数=0") 
    def test_fota_caseid_1996198(self):  
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']['appointpatchtime'] = 0
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.ACTIVE.value, timeout=600)
        appointment_time = self.mix.generate_fota_appointment_time(delay_seconds=120) # appointmenttime固定为当前时间2分钟后
        args={"taskId":self.taskid_tmp,"time":appointment_time}
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"04F2"',
                                                                                   'SetBookEvent:rt:0',
                                                                                   f'"appointmentTime":"{appointment_time}"'], unexpect_keywords=['failed to SetBookEvent'], timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid_tmp}) == appointment_time
        assert self.soa.get_fota_NotifyAppointTime(MASTER_NotifyAppointTime_EVENT.AppointmentTime) == appointment_time
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"04F4"',
                                                                                  f'"appointmentTime":"{appointment_time}"'], timeout=190):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.REACH_APPOINTMENT.value, timeout=190)

    @pytest.mark.V_2_1
    @pytest.mark.sanity
    @allure.title("任务信息解析_type50_appointPatchTime参数=-60") 
    def test_fota_caseid_1996199(self):  
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']['appointPatchTime'] = -60
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.ACTIVE.value, timeout=600)
        appointment_time = self.mix.generate_fota_appointment_time(delay_seconds=3780) # appointmenttime固定为当前时间2分钟后
        real_appointment_time = appointment_time - 60*60
        args={"taskId":self.taskid_tmp,"time":appointment_time}
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"04F2"',
                                                                                   'SetBookEvent:rt:0',
                                                                                   f'"appointmentTime":"{real_appointment_time}"'], unexpect_keywords=['failed to SetBookEvent'], timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid_tmp}) == real_appointment_time
        assert self.soa.get_fota_NotifyAppointTime(MASTER_NotifyAppointTime_EVENT.AppointmentTime) == real_appointment_time
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"04F4"',
                                                                                  f'"appointmentTime":"{real_appointment_time}"'], timeout=300):
            self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.REACH_APPOINTMENT.value, timeout=300)   

    @pytest.mark.V_2_1
    @pytest.mark.smoke
    @allure.title("任务信息解析_type50_appointPatchTime参数=3") 
    def test_fota_caseid_1996200(self):  
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']['appointPatchTime'] = 3
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.ACTIVE.value, timeout=600)
        appointment_time = self.mix.generate_fota_appointment_time(delay_seconds=120) # appointmenttime固定为当前时间2分钟后
        real_appointment_time = appointment_time + 3*60
        args={"taskId":self.taskid_tmp,"time":appointment_time}
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"04F2"',
                                                                                   'SetBookEvent:rt:0',
                                                                                   f'"appointmentTime":"{real_appointment_time}"'], unexpect_keywords=['failed to SetBookEvent'], timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid_tmp}) == real_appointment_time
        assert self.soa.get_fota_NotifyAppointTime(MASTER_NotifyAppointTime_EVENT.AppointmentTime) == real_appointment_time
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"04F4"',
                                                                                  f'"appointmentTime":"{real_appointment_time}"'], timeout=370):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.REACH_APPOINTMENT.value, timeout=370)            
                          
if __name__ == "__main__":
    pass

    




