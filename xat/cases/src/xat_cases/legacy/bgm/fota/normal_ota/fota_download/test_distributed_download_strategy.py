import os
import sys
import pytest
import allure
from time import sleep
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
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("V2TRoutingForwarder","client","V2TOTAFotaForwarder")])
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
                                    ], allow_sleep=False) 
        self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False, allow_sleep=False)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])    
        sleep(20)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.ssh.set_airplane_mode(isOn.Off)
        self.soa.ua_back_to_idle(DOMAIN.BGM)
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.ssh.set_airplane_mode(isOn.Off)
        self.ssh.set_network_mode(Network_Mode.Fifth_Generation)
        self.soa.ua_back_to_idle(DOMAIN.BGM)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ssh.set_airplane_mode(isOn.Off)
        self.ssh.set_network_mode(Network_Mode.Fifth_Generation)
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("分布式下载基本策略_ipa重试")    
    def test_fota_caseid_1983260(self):
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.DOWNLOAD, self.BGM_Download_Req)
        with self.log_manage.check_jetlog_by_keywords(log_type=" UAS", keywords='enter DownloadState::retryDownload', timeout=120):
            self.ssh.set_airplane_mode(isOn.On)
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("分布式下载基本策略_进度上传云端")    
    def test_fota_caseid_1983259(self):
        self.mix.back_fota_to(FOTAMasteSts.DOWNLOADING, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value
        start_time = time.time()
        while self.soa.get_fota_DownloadProcess(MASTER_DownloadProcess_EVENT.progress) != 100 and time.time() - start_time < 1800:
            pass
        assert self.soa.get_fota_DownloadProcess(MASTER_DownloadProcess_EVENT.progress) == 100

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("分布式下载基本策略_BGM_UA_5G")    
    def test_fota_caseid_1983257(self):
        self.mix.back_fota_to(FOTAMasteSts.DOWNLOADING, taskid=self.taskid)
        self.ssh.set_network_mode(Network_Mode.Fifth_Generation)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.ACTIVE.value, timeout=1800)

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("分布式下载基本策略_BGM_UA_4G")    
    def test_fota_caseid_1983256(self):
        self.mix.back_fota_to(FOTAMasteSts.DOWNLOADING, taskid=self.taskid)
        self.ssh.set_network_mode(Network_Mode.Fourth_Generation)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.ACTIVE.value, timeout=1800)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @pytest.mark.flaky(reruns=3, reruns_delay=10)
    @allure.title("分布式下载基本策略_BGM_UA_验包错误")    
    def test_fota_caseid_1983254(self):
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value
        BGM_Download_Req = copy.deepcopy(self.BGM_Download_Req)
        BGM_Download_Req["downloadReq"]["fileInformations"][0]["signature"] = "123456"
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.DOWNLOAD, BGM_Download_Req)
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.ErrorCode, target_status=UA_ErrorCode.FileSecurityCheck_Error_0x02_0x22.value, timeout=600)

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("分布式下载基本策略_小件下载_5G")    
    def test_fota_caseid_1983253(self):
        self.mix.update_version_debug(self.taskid,[])
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.ssh.set_network_mode(Network_Mode.Fifth_Generation)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.ACTIVE.value, timeout=120)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
 
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("分布式下载基本策略_小件下载_4G")    
    def test_fota_caseid_1983252(self):
        self.mix.update_version_debug(self.taskid,[])
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.ssh.set_network_mode(Network_Mode.Fourth_Generation)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.ACTIVE.value, timeout=120)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("分布式下载基本策略_5G断点续传")    
    def test_fota_caseid_1985163(self):
        self.ssh.set_network_mode(Network_Mode.Fifth_Generation)
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.ssh.set_airplane_mode(isOn.On)#开启飞行模式
        sleep(10)#等待10S
        self.ssh.set_airplane_mode(isOn.Off)#关闭飞行模式
        sleep(10)#等待10S
        self.sd_tester.reset_bgm()#重启BGM
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.ACTIVE.value, timeout=300)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("分布式下载基本策略_小件验包错误")    
    def test_fota_caseid_1983250(self):
        self.taskid_tmp = 999999
        self.mix.fota_back_to_idle()
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50_NKR = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50_NKR['data']['ecusInfo'][0]['orderList'][0][0]['signature'] = "=========================================="
            Task_Info_Type50_NKR['data']['ecusInfo'][0]['appPkg'][0]['signature'] = "++++++++++++++++++++++++++++++++++++++++++"
            Task_Info_Type50_NKR['data']['taskId'] = self.taskid_tmp
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_NKR)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.NEW_TASK.value, 20), "type50 not take effect"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0222"', timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)

if __name__ == "__main__":
    pass

    




