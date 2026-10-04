# -*- coding: utf-8 -*-
"""
@File        : test_FotamasterService.py
@Author      : jingjing.wang
@Time        : 2024/01/16 15:00 PM
@Description : Test s2s interface about bonnet function
"""
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.soa_partner.src.partner_const import *
from xat_cases.legacy.bgm.case_helper.diag_case_helper.DiagTestBase import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from copy import deepcopy
from xat_cases.legacy.soa.case_helper.test_base import TestBase


USAGE_MODE_MAP = {
    0: "ABANDONED",
    1: "INACTIVE",
    2: "CONVENIENCE",
    11: "ACTIVE",
    13: "DRIVING",
}

CAR_MODE_MAP = {
    0: "NORMAL",
    1: "TRANSPORT",
    2: "FACTORY",
    3: "CRASH",
    5: "DYNO",
}

@allure.feature("SOA服务接口")
@allure.story("架构基础/FotaMasterService")
@pytest.mark.wjj
class TestFotamasterService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("FotaMasterService", "client")])
        self.partner.method_default_timeout = 0.1


    def before_each_func(self, ecu, **kwargs):
        super().before_each_func(ecu, start=False)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        super().after_class(self, ecu)

    @allure.title("获取/通知FOTAMaster状态")
    @pytest.mark.sanity
    def test_caseid_1984006(self):
        self.sd_tester.change_car_mode(0)
        self.partner.ck_s2s_event(FOTAMASTER_SERVICE_CLIENT, "Status", {"status":{"taskId":0,"state":0,"errorCode":0,"serialNumber":1,"taskType":0}},timeout=4)
        self.partner.send_request_and_ck_resp(FOTAMASTER_SERVICE_CLIENT, "GetStatus", {}, {"out": {"taskId":0,"state":0,"errorCode":0,"serialNumber":1,"taskType":0}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02,'FOTAStatus',0,timeout=0.5) 
        

    @allure.title("获取FOTA任务信息")
    @pytest.mark.smoke
    def test_caseid_1984007(self):
        self.partner.send_request_and_ck_resp(FOTAMASTER_SERVICE_CLIENT,"GetTaskInfo",{},
                                                  {"out":{"version":"","updateTime":0,"releaseNoteURL":"","updateTitle":"","updatePackageTotalSize":0,"publishTime":"","lvSOC":0,"hvSOC":0}})
        
    @allure.title("取消FOTA升级")
    @pytest.mark.sanity
    def test_caseid_1984008(self):
        self.partner.send_request_and_ck_resp(FOTAMASTER_SERVICE_CLIENT,"CancelFota",{},{"out":0})

    @allure.title("触发检测任务")
    @pytest.mark.sanity
    def test_caseid_1984009(self):
        self.partner.send_request_and_ck_resp(FOTAMASTER_SERVICE_CLIENT,"CheckTask",{"cmd":0},{"out":0})

    @allure.title("开始FOTA下载")
    @pytest.mark.smoke
    def test_caseid_1984010(self):
        self.partner.send_request_and_ck_resp(FOTAMASTER_SERVICE_CLIENT,"StartDownload",{},{"out":0})

    @allure.title("停止FOTA下载")
    @pytest.mark.sanity
    def test_caseid_1984011(self):
        self.partner.send_request_and_ck_resp(FOTAMASTER_SERVICE_CLIENT,"StopDownload",{},{"out":1})

    @allure.title("暂停FOTA下载")
    @pytest.mark.sanity
    def test_caseid_1984012(self):
        self.partner.send_request_and_ck_resp(FOTAMASTER_SERVICE_CLIENT,"SuspendDownload",{},{"out":1})

    @allure.title("恢复FOTA下载")
    @pytest.mark.sanity
    def test_caseid_1984014(self):
        self.partner.send_request_and_ck_resp(FOTAMASTER_SERVICE_CLIENT,"ResumeDownload",{},{"out":1})

    @allure.title("开始FOTA升级")
    @pytest.mark.smoke
    def test_caseid_1984015(self):
        self.partner.send_request_and_ck_resp(FOTAMASTER_SERVICE_CLIENT,"StartUpdate",{},{"out":0})

    @allure.title("停止FOTA升级")
    @pytest.mark.sanity
    def test_caseid_1984016(self):
        self.partner.send_request_and_ck_resp(FOTAMASTER_SERVICE_CLIENT,"StopUpdate",{},{"out":0})

    @allure.title("设置预约升级时间")
    @pytest.mark.sanity
    def test_caseid_1984017(self):
        self.partner.send_request_and_ck_resp(FOTAMASTER_SERVICE_CLIENT,"SetAppointment",{"taskId":0,"time":0},{"out":0})

    @allure.title("获取预约升级时间")
    @pytest.mark.sanity
    def test_caseid_1984018(self):
        self.partner.send_request_and_ck_resp(FOTAMASTER_SERVICE_CLIENT,"GetAppointment",{"taskId":0},{"out":0})

    @allure.title("取消预约升级")
    @pytest.mark.sanity
    def test_caseid_1984019(self):
        self.partner.send_request_and_ck_resp(FOTAMASTER_SERVICE_CLIENT,"CancelAppointment",{"taskId":0},{"out":0})

    @allure.title("设置初次校验检查结果状态")
    @pytest.mark.sanity
    def test_caseid_1984091(self):
        data=self.partner.send_request_and_return_resp(FOTAMASTER_SERVICE_CLIENT,"SetFirstCheckResult",{"sts":{"errorCode":"0x04 0x20"}})
        assert data==None

    # @pytest.mark.sanity
    # @allure.title("通知FOTA预约升级时间") 
    # def test_caseid_1984314(self): 
    #     args={"taskId":self.taskid,"time":self.mix.generate_fota_appointment_time(delay_seconds=300)}  # time固定为当前时间5min后
    #     self.soa.send_fota_request(MASTER_REQUEST.SetAppointment,args=args)
    #     assert self.soa.get_fota_NotifyAppointTime(MASTER_NotifyAppointTime_EVENT.AppointmentTime) == args.get("time") and self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='SetBookEvent:rt:0', timeout=60)

    # @pytest.mark.sanity
    # @allure.title("获取/通知FOTAMaster条件检查结果")
    # def test_caseid_1984315(self):
    #     self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_TASK)
    #     self.mix.set_factory_ota_condition(display_hv_soc=250,low_volt_power=11.5,local_diag_sts=DiagActLineSts.DisActive) 
    #     self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
    #     assert FOTA_ConditionCheck_Code.CR_SUCCESSFUL.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)

    # @pytest.mark.repeat(num)
    # @pytest.mark.sanity
    # @allure.title("通知FOTA查询下载状态进度")    
    # def test_fota_1984316(self):
    #     global cur_num
    #     cur_num = cur_num + 1
    #     self.cur_log_path = f"/root/log/{self.super_file_name}/{self.file_name}/{cur_num}_E2E_Normal_Bench_Base_1984316"
    #     os.makedirs(self.cur_log_path, exist_ok=True)
    #     with allure.step("【Download】New Event: DownloadProcess"):
    #         assert self.soa.get_fota_DownloadProcess(MASTER_DownloadProcess_EVENT.taskId) == self.taskid, "Not Receive DownloadProcess Event"

    # @pytest.mark.repeat(num)
    # @pytest.mark.sanity
    # @allure.title("通知FOTA查询下载状态进度")    
    # def test_fota_1984321(self):
    #     self.partner.ck_s2s_event(FOTAMASTER_SERVICE_CLIENT, "UpdateProcess", {"updateProgress":{"taskId":0,"state":0,"progress":0,"leftTime":0,"errorCode":0}})

    # @pytest.mark.sanity
    # @allure.title("通知FOTA过程中车辆功能状态")
    # def test_caseid_1984324(self):
    #     self.partner.ck_s2s_event(FOTAMASTER_SERVICE_CLIENT,"FunctionStsNofitification",{"funcs":{"name":"0","status":0}})
        
    # @pytest.mark.sanity
    # @allure.title("通知FOTA过程中具体ECU刷写情况")
    # def test_caseid_1984325(self):
    #     self.partner.ck_s2s_event(FOTAMASTER_SERVICE_CLIENT,"UpdateErrorInfo",{"info":{"ecuName":"0","errorCode":0}})
            
    # @pytest.mark.sanity
    # @allure.title("FOTA Master状态机状态新增REMOTE_UPDATE1.4新增需求")
    # def test_fota_caseid_1984541(self):
    #     self.mix.set_fota_Remoteupdate_condition(UsageMode.INACTIVE, LockKCmd.Lock)
    #     self.soa.trigger_fota_type90(self.taskid)
    #     assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status # RENMOTE_UPDATE"
