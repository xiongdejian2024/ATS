import os
import re
import sys
import pytest
import allure
from time import sleep

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
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("UpdateAgentService","server","CDC_UA_Service")])
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
                                    FOTA_Skip_Debug.update_precondition_check,
                                    FOTA_Skip_Debug.cdc_acu_doip_check
                                    ], allow_sleep=False) 
        self.mix.update_version_debug(self.taskid,[DOMAIN.CDC])    

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.reset_bgm()
        self.io.bgm_diag_line_down()
        self.soa.start_send_ua_response(DOMAIN.CDC)
        self.soa.start_send_ua_event(DOMAIN.CDC, self.soa.pack_ua_event_args(UA_Sts.IDLE))
        self.mix.fota_back_to_idle()
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("下载唤醒策略_下载失败")    
    def test_fota_caseid_1983264(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=30)
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC,
                                                            UA_Sts.DOWNLOAD,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_FINAL_FAILED.value,
                                                            errorCode=UA_ErrorCode.DL_HTTPS_TimeoutError_0x02_0x08.value)
        sleep(3)
        assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=False, up_inactive=False), "下载失败时检查条件不满足"
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.mix.back_fota_to(FOTAMasteSts.IDLE, self.taskid)
        self.soa.stop_send_ua_event(DOMAIN.CDC)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    # @pytest.mark.V_1_4
    # @pytest.mark.full
    # @allure.title("下载唤醒策略_UA下载速度10min累计0")
    # def test_fota_caseid_1983262(self):
    #     self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90)
    #     self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
    #     self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
    #     self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=30)
    #     self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.DOWNLOAD) 
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"02F8"', timeout=800):
    #         sleep(630) # CDC UA downloadsize 10min 保持不变
    #     # todo: 台架休眠检测
    #     assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=False, up_inactive=False), "下载速度10min累计0时检查条件不满足"
    #     self.io.bgm_diag_line_up()
    #     assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.DOWNLOADING.value, timeout=120)
    #     self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
    #     self.mix.back_fota_to(FOTAMasteSts.IDLE, self.taskid)
    #     self.soa.stop_send_ua_event(DOMAIN.CDC)
    #     self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("FOTA下载超时1h不维持唤醒_0x02_0xF5_WakeUpTimeOut")
    def test_fota_caseid_1986138(self):
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90)
        get_status_args = self.soa.pack_ua_status_args(ua_sts=UA_Sts.DOWNLOAD)
        get_status_args['downloadStatus']['downloadSpeed'] = round(100/300, 2)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=30)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.DOWNLOAD) 
        for i in range(12):
            get_status_args['downloadStatus']['downloadFileSize'] += 100
            self.soa.update_ua_event(domain_name=DOMAIN.CDC, event_args={"status": get_status_args})
            self.soa.update_ua_response(domain_name=DOMAIN.CDC, get_status_args=get_status_args)
            if i == 11:
                with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"02F5"', timeout=800):
                    pass
            else:
                sleep(300) # 等待5分钟
        # todo: 台架休眠检测
        assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=False, up_inactive=False), "下载超时1h时检查条件不满足"
        self.io.bgm_diag_line_up()
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.DOWNLOADING.value, timeout=120)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.mix.back_fota_to(FOTAMasteSts.IDLE, self.taskid)
        self.soa.stop_send_ua_event(DOMAIN.CDC)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("FOTA下载网络状态异常不维持唤醒_0x02_0xF8_WakeUpNetworkError_getstatus失败")
    def test_fota_caseid_1986137(self):
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=30)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.DOWNLOAD) 
        sleep(10) # 等待fota master进下载
        self.soa.stop_send_ua_event(DOMAIN.CDC)
        self.soa.stop_send_ua_response(DOMAIN.CDC)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"02F8"', timeout=800):
            sleep(630) # CDC UA 下线 10min
        # todo: 台架休眠检测
        assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=False, up_inactive=False), "下载速度10min累计0时检查条件不满足"
        self.io.bgm_diag_line_up()
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.DOWNLOADING.value, timeout=120)

if __name__ == "__main__":
    pass

    




