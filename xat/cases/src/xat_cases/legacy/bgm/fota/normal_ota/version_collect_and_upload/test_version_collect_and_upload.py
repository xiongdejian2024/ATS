import os
import sys
import pytest
import allure
from time import sleep
import copy
import yaml

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
                         ("V2TRoutingForwarder","client","V2TOTAFotaForwarder"),
                         ("AcuModeManagerService","server")])
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
                                    FOTA_Skip_Debug.update_precondition_check,
                                    # FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check
                                    ], allow_sleep=False) 
        self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.sd_tester.write_ccp({950: 0x01, 962: 0x00})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x00})  # 检查写入的ccp
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("整车软硬件版本收集上传_版本收集条件判断_先插入诊断线，再推送任务")    
    def test_fota_caseid_1994511(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        self.io.bgm_diag_line_up()
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120)
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("整车软硬件版本收集上传_版本收集条件判断_无受诊断仲裁影响的业务执行")    
    def test_fota_caseid_1994510(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.NEW_TASK.value, timeout=600)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("诊断令牌_OTA Cancel_Query")    
    def test_fota_caseid_1985080(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        self.io.bgm_diag_line_up()
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("诊断令牌_OTA Cancel_Idle")    
    def test_fota_caseid_1985081(self):
        self.io.bgm_diag_line_up()
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("整车软硬件版本收集上传_PNC27唤醒")    
    def test_fota_caseid_1985083(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='VfcType :17', timeout=660):
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("整车软硬件版本收集_软硬件号重试")    
    def test_fota_caseid_1985084(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        with self.log_manage.check_jetlog_by_keywords(log_type="obt:", keywords=['result is error, retry send, addr:1201', 'result is error, retry send, addr:1201', 'result is error, retry send, addr:1201'], timeout=600):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"HWPN":"","SWPN":"ff","ecuId":"3011","name":"CDC"', timeout=600):
            pass 

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("整车软硬件版本收集_维持整车唤醒")    
    def test_fota_caseid_1985088(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        self.log_manage.check_jetlog_by_keywords(log_type=" rvsl:", keywords="SetAutoDrivingModeKeepAlive", timeout=90)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.NEW_TASK.value, timeout=600)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("整车软硬件版本收集_状态")    
    def test_fota_caseid_1985089(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='VfcType :23', timeout=30):
            pass
        self.log_manage.check_jetlog_by_keywords(log_type=" rvsl:", keywords=["check_ota_task => collect_version", "SetAutoDrivingModeKeepAlive"])
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.NEW_TASK.value, timeout=600)


    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("整车软硬件版本收集_上传信息成功")    
    def test_fota_caseid_1985091(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"01F2"', timeout=600):
            self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("整车软硬件版本收集_doip 检查")    
    def test_fota_caseid_1985092(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='22 f1 86', timeout=600):
            self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("整车软硬件版本收集_can(小件)")    
    def test_fota_caseid_1985099(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        with self.log_manage.check_jetlog_by_keywords(log_type="obt:", keywords=['result is error, retry send, addr:1601', 'result is error, retry send, addr:1601', 'result is error, retry send, addr:1601'], timeout=600):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"HWPN":"","SWPN":"ff","ecuId":"5011","name":"VDDM"', timeout=600):
            pass

    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("整车软硬件版本收集_版本收集_01F1")    
    def test_fota_caseid_1985100(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"01F1"', timeout=120):
            self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("任务信息获取_软硬件匹配通过")    
    def test_fota_caseid_1985101(self):
        self.mix.update_version_debug(200000,[DOMAIN.BGM])
        self.soa.trigger_fota_type20(200000)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = 200000
            Task_Info_Type50['data']['baseLineVer'] = '6100000200 DZ'
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.NEW_TASK.value, timeout=600)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("任务信息获取_软硬件匹配不通过") 
    def test_fota_caseid_1985102(self):
        self.soa.trigger_fota_type20(20000)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['code'] = 0
            Task_Info_Type50['data']['taskId'] = 20000
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=600)
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("任务信息获取_解析过程唤醒")    
    def test_fota_caseid_1985103(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        with self.log_manage.check_jetlog_by_keywords(log_type="", keywords=["upload_version => wait_task_info", "SetAutoDrivingModeKeepAlive"], timeout=90):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.NEW_TASK.value, timeout=600)

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("任务信息获取_获取任务详情")
    def test_fota_caseid_1985104(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"01F3"', timeout=600):
            self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid) 

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("任务信息获取_任务解析失败")    
    def test_fota_caseid_1985105(self):
        self.soa.trigger_fota_type20(20000)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = 20000
            Task_Info_Type50['data']['ecusInfo'] = []
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0202"', timeout=120):
            sleep(2)
            self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120)

    @pytest.mark.full
    @allure.title("任务信息获取_云端下发任务无ECU升级")    
    def test_fota_caseid_1985106(self):
        # self.soa.trigger_fota_type20(self.taskid)
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
        #     Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
        #     Task_Info_Type50['data']['taskId'] = self.taskid
        #     Task_Info_Type50['data']['ecusInfo'] = []
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0203"', timeout=120):
        #     sleep(2)
        # 	self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        # assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120)
        pass #SOA-21207

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("任务信息获取_taskid不一致")    
    def test_fota_caseid_1985107(self):
        self.soa.trigger_fota_type20(20000)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = 1
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0201"', timeout=120):
            sleep(2)
            self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120)

    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("Release Note获取_支持StartDownload")
    def test_fota_caseid_1985108(self):
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.DOWNLOADING.value, timeout=30)
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("Release Note获取_维持唤醒")
    def test_fota_caseid_1985109(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="KeepAliveCb", timeout=30):
            pass
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("版本收集与上传_baseline不匹配")
    def test_fota_caseid_1985117(self):
        self.soa.trigger_fota_type20(20000)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = 20000
            Task_Info_Type50['data']['baseLineVer'] = "6100000055BL"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0204"', timeout=120):
            sleep(2)
            self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120)

    # V1.4 CCP CASE
    @pytest.mark.V_1_4_ONLY
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_CCP_Mars无挂载低配")
    def test_fota_caseid_1985741(self, ecu):
        self.sd_tester.write_ccp({950: 0x01, 1312: 0x01, 1381: 0x01, 1395: 0x01, 566: 0x17, 1333: 0x01})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 1312: 0x01, 1381: 0x01, 1395: 0x01, 566: 0x17, 1333: 0x01})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid, expect_keywords=["BECM1_75"], unexpect_keywords=["MGM","SUM1","AUD","IPM", "BECM1_102"])

    @pytest.mark.V_1_4_ONLY
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_CCP_Mars其余值")
    def test_fota_caseid_1985098(self, ecu):
        self.sd_tester.write_ccp({950: 0x01, 1312: 0x00, 1381: 0x00, 1395: 0x00, 566: 0x20, 1333: 0x00})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 1312: 0x00, 1381: 0x00, 1395: 0x00, 566: 0x20, 1333: 0x00})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["MGM","SUM1","AUD", "BECM1_102", "BECM1_75"],unexpect_keywords=["IPM"])
    
    @pytest.mark.V_1_4_ONLY
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_CCP_Mars有挂载高配")
    def test_fota_caseid_1985096(self, ecu):
        self.sd_tester.write_ccp({950: 0x01, 1312: 0x02, 1381: 0x02, 1395: 0x02, 566: 0x10, 1333: 0x02})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 1312: 0x02, 1381: 0x02, 1395: 0x02, 566: 0x10, 1333: 0x02})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["MGM","SUM1","AUD","BECM1_102", "IPM"],unexpect_keywords=["BECM1_75"])
    
    @pytest.mark.V_1_4_ONLY
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_CCP_Venus其余值 ")
    def test_fota_caseid_1985095(self, ecu):
        self.sd_tester.write_ccp({950: 0x02, 1312: 0x00, 1381: 0x00, 1395: 0x00, 566: 0x20, 1333: 0x00,1473:0x00})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x02, 1312: 0x00, 1381: 0x00, 1395: 0x00, 566: 0x20, 1333: 0x00,1473:0x00})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid, expect_keywords=["MGM", "SUM1", "AUD", "BECM1_102", "BECM1_75","SMB"], unexpect_keywords=["IPM"])
    
    @pytest.mark.V_1_4_ONLY
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_CCP_Venus无挂载低配")
    def test_fota_caseid_1985094(self, ecu):
        self.sd_tester.write_ccp({950: 0x02, 1312: 0x01, 1381: 0x01, 1395: 0x01, 566: 0x17, 1333: 0x01,1473:0x01})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x02, 1312: 0x01, 1381: 0x01, 1395: 0x01, 566: 0x17, 1333: 0x01,1473:0x01})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid, expect_keywords=["BECM1_75"], unexpect_keywords=["MGM","SUM1","AUD","SMB","IPM", "BECM1_102"])
    
    @pytest.mark.V_1_4_ONLY
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title(" 整车软硬件版本收集_CCP_Venus有挂载高配 ")
    def test_fota_caseid_1985093(self, ecu):
        self.sd_tester.write_ccp({950:0x02,1312:0x02,1381:0x02,1395:0x02,566:0x10,1333:0x02,1473:0x02})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950:0x02,1312:0x02,1381:0x02,1395:0x02,566:0x10,1333:0x02,1473:0x02})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["MGM","SUM1","AUD","BECM1_102","SMB","IPM"], unexpect_keywords=["BECM1_75"])
    
    @pytest.mark.V_1_4_ONLY
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_CCP_车型判断950≠01，02")    
    def test_fota_caseid_1985086(self):
        self.sd_tester.write_ccp({950 : 0x3})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x03})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid, unexpect_keywords=["PSGM"])

    # V2.0 beta2 BP及以前版本 CCP CASE
    @pytest.mark.V_2_1_ONLY
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_Marsone平台CCP_全挂载")
    def test_fota_caseid_1986065(self):
        self.sd_tester.write_ccp({950: 0x01, 962: 0x00, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x00, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "MGM", 5061,"HVCM", 5081,"ECM3", 5091, "IEM", 5071, "SUM1", 5131, "AUD", 3021, "IPM", 6241], unexpect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "VCU", 5092, "IEM2", 5073])

    @pytest.mark.V_2_1_ONLY
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_Marsone平台CCP_全不挂载")
    def test_fota_caseid_1986064(self):
        self.sd_tester.write_ccp({950: 0x01, 962: 0x00, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x00, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "HVCM", 5081, "ECM3", 5091, "IEM", 5071], unexpect_keywords=["BECM2", 5055, "HVCM2", 5082, "VCU", 5092, "MGM", 5061, "MGM2", 5062, "SUM1", 5131, "AUD", 3021, "IPM", 6241, "SMB", "IEM2", 5073])

    @pytest.mark.V_2_1_ONLY
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_Marsone平台CCP_全其余值")
    def test_fota_caseid_1986063(self):
        self.sd_tester.write_ccp({950: 0x03, 962: 0x03, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x03, 962: 0x03, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091,"IEM", 5071, "SUM1", 5131, "AUD", 3021], unexpect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "VCU", 5092, "IEM2", 5073, "IPM", 6241])

    @pytest.mark.V_2_1_ONLY
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_MarsMCA800V平台CCP_全挂载")
    def test_fota_caseid_1986062(self):
        self.sd_tester.write_ccp({950: 0x01, 962: 0x02, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x02, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "MGM2", 5062,"HVCM2", 5082, "IEM2", 5073, "VCU", 5092, "SUM1", 5131, "AUD", 3021, "IPM", 6241], unexpect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091, "IEM", 5071])

    @pytest.mark.V_2_1_ONLY
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_MarsMCA800V平台CCP_全不挂载")
    def test_fota_caseid_1986061(self):
        self.sd_tester.write_ccp({950: 0x01, 962: 0x02, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x02, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "HVCM2", 5082, "IEM2", 5073, "VCU", 5092], unexpect_keywords=["BECM1", 5051, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "MGM", 5061, "MGM2", 5062, "SUM1", 5131, "AUD", 3021, "IPM", 6241, "SMB"])

    @pytest.mark.V_2_1_ONLY
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_MarsMCA800V平台CCP_全其余值")
    def test_fota_caseid_1986060(self):
        self.sd_tester.write_ccp({950: 0x03, 962: 0x02, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x03, 962: 0x02, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "IEM2", 5073, "VCU", 5092, "SUM1", 5131, "AUD", 3021], unexpect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "IPM", 6241])

    # V2.0 beta2 BP以后版本 CCP CASE
    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_Marsone平台CCP_全挂载")
    def test_fota_caseid_1986065(self):
        self.sd_tester.write_ccp({950: 0x01, 962: 0x00, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x00, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "MGM", 5061,"HVCM", 5081,"ECM3", 5091, "IEM", 5071, "SUM1", 5131, "AUD", 3021, "IPM", 6241, "WPC3", 1072], unexpect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "VCU", 5092, "IEM2", 5073])

    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_Marsone平台CCP_全不挂载")
    def test_fota_caseid_1986064(self):
        self.sd_tester.write_ccp({950: 0x01, 962: 0x00, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x00, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "HVCM", 5081, "ECM3", 5091, "IEM", 5071], unexpect_keywords=["BECM2", 5055, "HVCM2", 5082, "VCU", 5092, "MGM", 5061, "MGM2", 5062, "SUM1", 5131, "AUD", 3021, "IPM", 6241, "SMB", "IEM2", 5073, "WPC3", 1072])

    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_Marsone平台CCP_全其余值")
    def test_fota_caseid_1986063(self):
        self.sd_tester.write_ccp({950: 0x03, 962: 0x03, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x03, 962: 0x03, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091,"IEM", 5071, "SUM1", 5131, "AUD", 3021, "WPC3", 1072], unexpect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "VCU", 5092, "IEM2", 5073, "IPM", 6241])

    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_MarsMCA800V平台CCP_全挂载")
    def test_fota_caseid_1986062(self):
        self.sd_tester.write_ccp({950: 0x01, 962: 0x02, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x02, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "MGM2", 5062,"HVCM2", 5082, "IEM2", 5073, "VCU", 5092, "SUM1", 5131, "AUD", 3021, "IPM", 6241, "WPC3", 1072], unexpect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091, "IEM", 5071])

    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_MarsMCA800V平台CCP_全不挂载")
    def test_fota_caseid_1986061(self):
        self.sd_tester.write_ccp({950: 0x01, 962: 0x02, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x02, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "HVCM2", 5082, "IEM2", 5073, "VCU", 5092], unexpect_keywords=["BECM1", 5051, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "MGM", 5061, "MGM2", 5062, "SUM1", 5131, "AUD", 3021, "IPM", 6241, "SMB", "WPC3", 1072])

    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_MarsMCA800V平台CCP_全其余值")
    def test_fota_caseid_1986060(self):
        self.sd_tester.write_ccp({950: 0x03, 962: 0x02, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x03, 962: 0x02, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "IEM2", 5073, "VCU", 5092, "SUM1", 5131, "AUD", 3021, "WPC3", 1072], unexpect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "IPM", 6241])

    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_Venus 400V CCP_全挂载")
    def test_fota_caseid_1986059(self):
        self.sd_tester.write_ccp({950: 0x02, 962: 0x00, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x02, 962: 0x00, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "SUM1", 5132, "AUD", 3021, "IPM", 6242, "WPC3", 1072], unexpect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "VCU", 5092, "IEM2", 5073])

    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_Venus 400V CCP_全不挂载")
    def test_fota_caseid_1986058(self):
        self.sd_tester.write_ccp({950: 0x02, 962: 0x00, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x02, 962: 0x00, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "HVCM", 5081, "ECM3", 5091, "IEM", 5071], unexpect_keywords=["BECM2", 5055, "HVCM2", 5082, "MGM2", 5062, "MGM", 5061, "SUM1", 5132, "AUD", 3021, "IPM", 6242, "SMB", "WPC3", 1072, "VCU", 5092, "IEM2", 5073])

    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_Venus 400V CCP_全其余值")
    def test_fota_caseid_1986057(self):
        self.sd_tester.write_ccp({950: 0x02, 962: 0x03, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x02, 962: 0x03, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "SUM1", 5132, "AUD", 3021, "WPC3", 1072], unexpect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "VCU", 5092, "IPM", 6242, "IEM2", 5073])

    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_Venus 800V CCP_全挂载")
    def test_fota_caseid_1986056(self):
        self.sd_tester.write_ccp({950: 0x02, 962: 0x02, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x02, 962: 0x02, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "IEM2", 5073, "VCU", 5092, "SUM1", 5132, "AUD", 3021, "IPM", 6242, "WPC3", 1072], unexpect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091, "IEM", 5071])

    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_Venus 800V CCP_全不挂载")
    def test_fota_caseid_1986055(self):
        self.sd_tester.write_ccp({950: 0x02, 962: 0x02, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x02, 962: 0x02, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "HVCM2", 5082, "IEM2", 5073, "VCU", 5092], unexpect_keywords=["BECM1", 5051, "MGM", 5061, "MGM2", 5062, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "SUM1", 5132, "AUD", 3021, "IPM", 6242, "SMB", "WPC3", 1072])

    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("整车软硬件版本收集_Venus 800V CCP_全其余值")
    def test_fota_caseid_1986054(self):
        self.sd_tester.write_ccp({950: 0x02, 962: 0x02, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x02, 962: 0x02, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "IEM2", 5073, "VCU", 5092, "SUM1", 5132, "AUD", 3021, "WPC3", 1072], unexpect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "IPM", 6242])

    # @pytest.mark.smoke
    # @allure.title("整车软硬件版本收集_电子架构信息确认Mars")
    # def test_fota_caseid_1986053(self):
    #     json_content = self.ssh.type_commands(DeviceName.BGM, "/app/bin/zstdcat /app/bin/fota/mars1_ecu_info.json")
    #     data = eval(json_content)
    #     all_ecu = data['mars1EcuCfg']
    #     with open('config/ecu_info_v2.0.yaml', 'r') as fn:
    #         all_local_ecu = yaml.safe_load(fn)['mars1']
    #         ck_res = dict.fromkeys(all_local_ecu.keys(), False)
    #         for ecu_name, item in all_local_ecu.items():
    #             ecu_id = item['ecuid']
    #             for ecu in all_ecu:
    #                 if f"'name': '{ecu_name}'" in str(ecu) and f"'ecuid': '{ecu_id}'" in str(ecu):
    #                     ck_res[ecu_name] = True
    #     for k, v in ck_res.items():
    #         assert v , f'mars1-ecu：{k} 与电子架构定义不符'

    # @pytest.mark.smoke
    # @allure.title("整车软硬件版本收集_电子架构信息确认Venus")
    # def test_fota_caseid_1986052(self):
    #     json_content = self.ssh.type_commands(DeviceName.BGM, "/app/bin/zstdcat /app/bin/fota/venus_ecu_info.json")
    #     data = eval(json_content)
    #     all_ecu = data['venusEcuCfg']
    #     with open('config/ecu_info_v2.0.yaml', 'r') as fn:
    #         all_local_ecu = yaml.safe_load(fn)['venus']
    #         ck_res = dict.fromkeys(all_local_ecu.keys(), False)
    #         for ecu_name, item in all_local_ecu.items():
    #             ecu_id = item['ecuid']
    #             for ecu in all_ecu:
    #                 if f"'name': '{ecu_name}'" in str(ecu) and f"'ecuid': '{ecu_id}'" in str(ecu):
    #                     ck_res[ecu_name] = True
    #     for k, v in ck_res.items():
    #         assert v , f'Venus-ecu：{k} 与电子架构定义不符'

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("整车软硬件版本收集_0x01_0x05_DiagnosticToolIn")
    def test_fota_caseid_1986139(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0105"', timeout=600):
            self.sd_tester.diag_cancel()

    @pytest.mark.ecu_mock
    @allure.title("整车软硬件版本收集_软硬件号收集")
    def test_fota_caseid_1985085(self):
        from xat_ecu.api.common.common import set_bench_vlan9_ip
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])
        self.diag_mock.update_0x22_data(ecu_name="ACU", did="F1AA", data_info_update={"NRC": 0x11})
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=['HWPN', ''])

    # V2.2 AD 以后版本 CCP CASE
    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("V2.2_整车软硬件版本收集_Marsone平台CCP_全挂载")
    def test_fota_caseid_1995515(self):
        self.sd_tester.write_ccp({950: 0x01, 962: 0x00, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02, 1335: 0x02})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x00, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02, 1335: 0x02})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "MGM", 5061,"HVCM", 5081,"ECM3", 5091, "IEM", 5071, "SUM1", 5131, "AUD", 3021, "IPM", 6241, "WPC3", 1072], unexpect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "VCU", 5092, "IEM2", 5073, "EVCC", 5201])

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("V2.2_整车软硬件版本收集_Marsone平台CCP_全不挂载")
    def test_fota_caseid_1995514(self):
        self.sd_tester.write_ccp({950: 0x01, 962: 0x00, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01, 1335: 0x01})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x00, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01, 1335: 0x01})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "HVCM", 5081, "ECM3", 5091, "IEM", 5071], unexpect_keywords=["BECM2", 5055, "HVCM2", 5082, "VCU", 5092, "MGM", 5061, "MGM2", 5062, "SUM1", 5131, "AUD", 3021, "IPM", 6241, "SMB", "IEM2", 5073, "WPC3", 1072, "EVCC", 5201])

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("V2.2_整车软硬件版本收集_Marsone平台CCP_全其余值")
    def test_fota_caseid_1995513(self):
        self.sd_tester.write_ccp({950: 0x03, 962: 0x03, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03, 1335: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x03, 962: 0x03, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03, 1335: 0x03})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091,"IEM", 5071, "SUM1", 5131, "AUD", 3021, "WPC3", 1072], unexpect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "VCU", 5092, "IEM2", 5073, "IPM", 6241, "EVCC", 5201])

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("V2.2_整车软硬件版本收集_MarsMCA800V平台CCP_全挂载")
    def test_fota_caseid_1995512(self):
        self.sd_tester.write_ccp({950: 0x01, 962: 0x02, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02, 1335: 0x02})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x02, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02, 1335: 0x02})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "MGM2", 5062,"HVCM2", 5082, "IEM2", 5073, "VCU", 5092, "SUM1", 5131, "AUD", 3021, "IPM", 6241, "WPC3", 1072], unexpect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "EVCC", 5201])

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("V2.2_整车软硬件版本收集_MarsMCA800V平台CCP_全不挂载")
    def test_fota_caseid_1995511(self):
        self.sd_tester.write_ccp({950: 0x01, 962: 0x02, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01, 1335: 0x01})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x02, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01, 1335: 0x01})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "HVCM2", 5082, "IEM2", 5073, "VCU", 5092], unexpect_keywords=["BECM1", 5051, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "MGM", 5061, "MGM2", 5062, "SUM1", 5131, "AUD", 3021, "IPM", 6241, "SMB", "WPC3", 1072, "EVCC", 5201])

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("V2.2_整车软硬件版本收集_MarsMCA800V平台CCP_全其余值")
    def test_fota_caseid_1995510(self):
        self.sd_tester.write_ccp({950: 0x03, 962: 0x02, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03, 1335: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x03, 962: 0x02, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03, 1335: 0x03})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "IEM2", 5073, "VCU", 5092, "SUM1", 5131, "AUD", 3021, "WPC3", 1072], unexpect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "IPM", 6241, "EVCC", 5201])

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("V2.2_整车软硬件版本收集_Venus 400V CCP_全挂载")
    def test_fota_caseid_1995509(self):
        self.sd_tester.write_ccp({950: 0x02, 962: 0x00, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02, 1335: 0x02})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x02, 962: 0x00, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02, 1335: 0x02})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "SUM1", 5132, "AUD", 3021, "IPM", 6242, "WPC3", 1072, "EVCC", 5201], unexpect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "VCU", 5092, "IEM2", 5073])

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("V2.2_整车软硬件版本收集_Venus 400V CCP_全不挂载")
    def test_fota_caseid_1995508(self):
        self.sd_tester.write_ccp({950: 0x02, 962: 0x00, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01, 1335: 0x01})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x02, 962: 0x00, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01, 1335: 0x01})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "HVCM", 5081, "ECM3", 5091, "IEM", 5071], unexpect_keywords=["BECM2", 5055, "HVCM2", 5082, "MGM2", 5062, "MGM", 5061, "SUM1", 5132, "AUD", 3021, "IPM", 6242, "SMB", "WPC3", 1072, "VCU", 5092, "IEM2", 5073, "EVCC", 5201])

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("V2.2_整车软硬件版本收集_Venus 400V CCP_全其余值")
    def test_fota_caseid_1995507(self):
        self.sd_tester.write_ccp({950: 0x02, 962: 0x03, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03, 1335: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x02, 962: 0x03, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03, 1335: 0x03})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "SUM1", 5132, "AUD", 3021, "WPC3", 1072], unexpect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "VCU", 5092, "IPM", 6242, "IEM2", 5073, "EVCC", 5201])

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("V2.2_整车软硬件版本收集_Venus 800V CCP_全挂载")
    def test_fota_caseid_1995506(self):
        self.sd_tester.write_ccp({950: 0x02, 962: 0x02, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1439: 0x02, 1335: 0x02})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x02, 962: 0x02, 1312: 0x02, 1381: 0x02, 1395: 0x02, 1333: 0x02, 1473: 0x02, 1335: 0x02})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "IEM2", 5073, "VCU", 5092, "SUM1", 5132, "AUD", 3021, "IPM", 6242, "WPC3", 1072, "EVCC", 5201], unexpect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091, "IEM", 5071])

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("V2.2_整车软硬件版本收集_Venus 800V CCP_全不挂载")
    def test_fota_caseid_1995505(self):
        self.sd_tester.write_ccp({950: 0x02, 962: 0x02, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01, 1335: 0x01})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x02, 962: 0x02, 1312: 0x01, 1381: 0x01, 1395: 0x01, 1333: 0x01, 1473: 0x01, 1439: 0x01, 1335: 0x01})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "HVCM2", 5082, "IEM2", 5073, "VCU", 5092], unexpect_keywords=["BECM1", 5051, "MGM", 5061, "MGM2", 5062, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "SUM1", 5132, "AUD", 3021, "IPM", 6242, "SMB", "WPC3", 1072, "EVCC", 5201])

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=2, reruns_delay=10)
    @allure.title("V2.2_整车软硬件版本收集_Venus 800V CCP_全其余值")
    def test_fota_caseid_1995504(self):
        self.sd_tester.write_ccp({950: 0x02, 962: 0x02, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03, 1335: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x02, 962: 0x02, 1312: 0x03, 1381: 0x03, 1395: 0x03, 1333: 0x03, 1473: 0x03, 1439: 0x03, 1335: 0x03})  # 检查写入的ccp
        self.mix.check_keywords_in_version_collect_results(taskid=self.taskid,expect_keywords=["BECM2", 5055, "MGM2", 5062, "HVCM2", 5082, "IEM2", 5073, "VCU", 5092, "SUM1", 5132, "AUD", 3021, "WPC3", 1072], unexpect_keywords=["BECM1", 5051, "MGM", 5061, "HVCM", 5081, "ECM3", 5091, "IEM", 5071, "IPM", 6242, "EVCC", 5201])

if __name__ == "__main__":
    pass