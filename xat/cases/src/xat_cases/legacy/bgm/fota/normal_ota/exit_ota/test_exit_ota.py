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
                         ("UpdateAgentService","client","BGM_UA_Service")])
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
        self.ssh.update_ua_skip(DOMAIN.BGM, False)
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip']) 
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
                    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.ssh.set_airplane_mode(isOn.Off)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.V_2_1
    @pytest.mark.smoke
    @allure.title("退出FOTA流程_写入DID F150&&F151") 
    def test_fota_caseid_1994896(self):
        self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xf150, SESSION.EXTENDED, UnLock.L5, '6100000110204141',#写入F150 6100000110 AA
                                           '62f1506100000110204141', recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xf151, SESSION.EXTENDED, UnLock.L5,
                                           '56322e312e300000000000000000000000000000000000000000000000000000',#写入F151 V1.1.0
                                           '62f15156322e312e300000000000000000000000000000000000000000000000000000',recover=False)
        self.sd_tester.stop_tester_present()
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM]) 
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid) 
        target_soft_id = self.tsp.get_softid_from_taskid(task_id=self.taskid)
        target_baseline,target_dis_baseline,_ = self.tsp.get_target_version_from_softid(soft_id=target_soft_id,ecu_name='CD')
        target_baseline_diag = target_baseline[:-3] + "".join([hex(ord(char))[2:] for char in target_baseline[-3:]])
        target_dis_baseline_diag = ''.join(hex(ord(c))[2:] for c in target_dis_baseline)
        assert self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf150, SESSION.DEFAULT, '62f150', check_in=target_baseline_diag)
        assert self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf151, SESSION.DEFAULT, '62f151', check_in=target_dis_baseline_diag)

    @pytest.mark.V_2_1
    @pytest.mark.smoke
    @allure.title("退出FOTA流程_退出FOTAMODE_正向流程") 
    def test_fota_caseid_1989745(self):
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM]) 
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid) 
        with self.log_manage.check_jetlog_by_keywords(log_type='-E "fota: | diag_client:| EM2:"', keywords=[ 'tx 1fff:10 81',
                                                                                                            'notify door is available',
                                                                                                            'tx 1011:31 01 a1 00 02',
                                                                                                            'rx 1011:71 01 a1 00 10 00',
                                                                                                            'tx 1401:31 01 a1 00 02',
                                                                                                            'tx 1201:31 01 a1 00 02',
                                                                                                            'tx 1630:31 01 42 89 00',
                                                                                                            'tx 1001:31 01 a1 00 02',
                                                                                                            'rx 1001:71 01 a1 00 10 00',
                                                                                                            'tx 1630:31 01 40 00 00',
                                                                                                            'notify current mode: default'
                                                                                                            ], timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.SUCCESSFUL.value, timeout=1400)
        
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("ERROR_CODE重试_03_F7(Update_Failed_CANNOTDRIVING)") 
    def test_fota_caseid_1979762(self):
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM]) 
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate) 
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"03F7"',
                                                                                   '"stateCode":"03F7"',
                                                                                   '"stateCode":"03F7"',
                                                                                   '"stateCode":"03F7"'
                                                                                   ], timeout=600):
            time.sleep(2) #等待log manage启动
            self.ssh.set_airplane_mode(isOn.On)
            self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FAILED_NOT_DRIVING.value, timeout=300)
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("ERROR_CODE重试_03_F7 && 05_05 组合") 
    def test_fota_caseid_1994876(self):
        try:            
            self.mix.update_version_debug(self.taskid,[DOMAIN.BGM]) 
            self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate) 
            assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
            self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"03F7"',timeout=600):
                time.sleep(2) #等待log manage启动
                self.ssh.set_airplane_mode(isOn.On)
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['SaveCodeToCloud:err code:0505,stage:2',
                                                                                       '"stateCode":"0505"',
                                                                                       'cmdEngsendDataAsync error, soa_ret:0, return:2',
                                                                                       'SaveCodeToCloud:err code:03F7,stage:2',
                                                                                       '"stateCode":"03F7"',
                                                                                       'cmdEngsendDataAsync error, soa_ret:0, return:2'
                                                                                        ], timeout=600):
                self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=300)
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"03F7"',
                                                                                       'filterKeyStateCode:state code:03F7, entry_send: 0, success_send:1',
                                                                                       '"stateCode":"0505"',
                                                                                       'filterKeyStateCode:state code:0505, entry_send: 0, success_send:1'
                                                                                        ], timeout=30):
                self.ssh.set_airplane_mode(isOn.Off)
        finally:
            self.ssh.set_airplane_mode(isOn.Off)


    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("升级失败不可开车_重启后Status") 
    def test_fota_caseid_1987979(self):
       self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])  
       self.mix.back_fota_to(FOTAMasteSts.FAILED_NOT_DRIVING,taskid=self.taskid)
       assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value
       time.sleep(120)
       self.sd_tester.reset_bgm()
       assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value, "can not receive Status after reset"
       assert self.bus_comm.check_InfoCan_FOTAStatus(infocanfotastatus=InfoCanFOTAStatus.UpdateFailNotDriving.value)

    # @pytest.mark.ecu_mock
    # @allure.title("有SRS升级_失败不可开车退出）") 
    # def test_fota_caseid_1987601(self):
    #     self.mix.update_version_debug(self.taskid,["SRS"])
    #     self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid) 
    #     assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
    #     self.diag_mock.update_0x10_data(ecu_name="SRS", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x11_data(ecu_name="SRS", reset_type={0x01: [0x01]}) 
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"030A"',#检查上报code 进boot失败
    #                                                                                 'ChangeState:hv_ecu_upgrade => exit_ota',#检查Post Update步骤
    #                                                                                'SendRawData:raw data: :[ 10 81 ]',#检查Post Update步骤
    #                                                                                'FinToSendChangeSessionReqCb:notify door is availabl',#检查Post Update步骤
    #                                                                                'ChangeState:exit_ota => failed',#检查第一轮失败
    #                                                                                'QuitFotaModeCb:quit_fota_mode_ecu_info, ecu_name:TCAM',#检查退出流程第一阶段退FOTAMODE
    #                                                                                'SendRawData:raw data: :[ 2e f1 53 00 ]',#j检查退出流程第一阶段写入F153 00
    #                                                                                'ChangeState:failed => rescue_query_task',#检查进入救援流程
    #                                                                                'ChangeState:rescue_pre_check => failed_not_driving',#检查进入救援失败不可开车
    #                                                                                'IsAllUasInIdleCb:not in idle ua count:0',#检查退出流程第二阶段拉齐UA
    #                                                                                'findEcuFromTaskinfo:has find in task ecu id: 5031, found: 1',#检查到存在SRS升级任务
    #                                                                               ], timeout=600):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
    #     time.sleep(25) #检测到本次任务中存在SRS升级需等待30S进行重启SRS 启动检索需要约3S
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['SendRawData:raw data: :[ 11 01 ]',#检查重启SRS
    #                                                                                 'ResetEcuCb:, data::[ 51 01 ]',#检查 mock SRS 肯定响应
    #                                                                                 'reset srs  waiting 5s to start version collection'#检查重启后等待5S进行下一步
    #                                                                                 ],timeout=60):
    #         pass
    #     time.sleep(2) #重启SRS后需等待5s,进行版本校验 写入F153,启动检索需要约3S
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['SendRawData:raw data: :[ 2e f1 53 06 ]',#检查写入F15306
    #                                                                             #    ', error code:0, serial number:1, task type:1',#检查Flag置位 SOA-25497偏差
    #                                                                                '"stateCode":"03F7"',#检查上报TSP 失败不可开车
    #                                                                                'SendToMonitorServer:Send to monitor'
    #                                                                                ],timeout=60):
    #         pass
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['SetVFCReqDiagnosticCb: VfcType :23',#检查停发唤醒
    #                                                                                         'onTimer:Send 3E 80',#检查停发唤醒
    #                                                                                         ],timeout=60):
    #         pass                                                               
    #     assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value,'当前不在失败不可开车状态'
    #     assert self.bus_comm.check_InfoCan_FOTAStatus(infocanfotastatus=InfoCanFOTAStatus.UpdateFailNotDriving.value),'InfoCan FOTAStatus 非 UpdateFailNotDriving'

    @pytest.mark.ecu_mock
    @allure.title("无SRS升级_失败不可开车退出）") 
    def test_fota_caseid_1987602(self):
        self.mix.update_version_debug(self.taskid,["DDM"])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid) 
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: {"NRC": 0x22}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"030A"',#检查上报code 进boot失败
                                                                                    'ChangeState:hv_ecu_upgrade => exit_ota',#检查Post Update步骤
                                                                                   'SendRawData:raw data: :[ 10 81 ]',#检查Post Update步骤
                                                                                   'FinToSendChangeSessionReqCb:notify door is availabl',#检查Post Update步骤
                                                                                   'ChangeState:exit_ota => failed',#检查第一轮失败
                                                                                   'QuitFotaModeCb:quit_fota_mode_ecu_info, ecu_name:TCAM',#检查退出流程第一阶段退FOTAMODE
                                                                                   'SendRawData:raw data: :[ 2e f1 53 00 ]',#j检查退出流程第一阶段写入F153 00
                                                                                   'ChangeState:failed => rescue_query_task',#检查进入救援流程
                                                                                   'ChangeState:rescue_pre_check => failed_not_driving',#检查进入救援失败不可开车
                                                                                   'IsAllUasInIdleCb:not in idle ua count:0',#检查退出流程第二阶段拉齐UA
                                                                                   'SendRawData:raw data: :[ 2e f1 53 06 ]',#检查写入F15306
                                                                                   #    ', error code:0, serial number:1, task type:1',#检查Flag置位 SOA-25497偏差
                                                                                   '"stateCode":"03F7"',#检查上报TSP 失败不可开车
                                                                                   'SendToMonitorServer:Send to monitor'
                                                                                  ], timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['SetVFCReqDiagnosticCb: VfcType :23',#检查停发唤醒
                                                                                            'onTimer:Send 3E 80',#检查停发唤醒
                                                                                            ],timeout=60):
            pass                                                               
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value,'当前不在失败不可开车状态'
        assert self.bus_comm.check_InfoCan_FOTAStatus(infocanfotastatus=InfoCanFOTAStatus.UpdateFailNotDriving.value),'InfoCan FOTAStatus 非 UpdateFailNotDriving'

    # @pytest.mark.ecu_mock
    # @allure.title("有SRS升级_失败不可开车退出_重启否定响应）") 
    # def test_fota_caseid_1987600(self):
    #     self.mix.update_version_debug(self.taskid,["SRS"])
    #     self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid) 
    #     assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
    #     self.diag_mock.update_0x10_data(ecu_name="SRS", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x11_data(ecu_name="SRS", reset_type={0x01: {"NRC": 0x22}})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"030A"',#检查上报code 进boot失败
    #                                                                                 'ChangeState:hv_ecu_upgrade => exit_ota',#检查Post Update步骤
    #                                                                                'SendRawData:raw data: :[ 10 81 ]',#检查Post Update步骤
    #                                                                                'FinToSendChangeSessionReqCb:notify door is availabl',#检查Post Update步骤
    #                                                                                'ChangeState:exit_ota => failed',#检查第一轮失败
    #                                                                                'QuitFotaModeCb:quit_fota_mode_ecu_info, ecu_name:TCAM',#检查退出流程第一阶段退FOTAMODE
    #                                                                                'SendRawData:raw data: :[ 2e f1 53 00 ]',#j检查退出流程第一阶段写入F153 00
    #                                                                                'ChangeState:failed => rescue_query_task',#检查进入救援流程
    #                                                                                'ChangeState:rescue_pre_check => failed_not_driving',#检查进入救援失败不可开车
    #                                                                                'IsAllUasInIdleCb:not in idle ua count:0',#检查退出流程第二阶段拉齐UA
    #                                                                                'findEcuFromTaskinfo:has find in task ecu id: 5031, found: 1',#检查到存在SRS升级任务
    #                                                                               ], timeout=600):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
    #     time.sleep(25) #检测到本次任务中存在SRS升级需等待30S进行重启SRS 启动检索需要约3S
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['SendRawData:raw data: :[ 11 01 ]',#检查重启SRS
    #                                                                                 'ResetEcuCb:, data::[ 7f 11 22 ]',#检查 mock SRS 否定响应
    #                                                                                 'SendRawData:raw data: :[ 11 01 ]',#检查重启SRS重试第一次
    #                                                                                 'ResetEcuCb:, data::[ 7f 11 22 ]',#检查 mock SRS 否定响应
    #                                                                                 'SendRawData:raw data: :[ 11 01 ]',#检查重启SRS重试第二次
    #                                                                                 'ResetEcuCb:, data::[ 7f 11 22 ]',#检查 mock SRS 否定响应
    #                                                                                 'reset srs  waiting 5s to start version collection'#检查重启后等待5S进行下一步
    #                                                                                 ],timeout=60):
    #         pass
    #     time.sleep(2) #重启SRS后需等待5s,进行版本校验 写入F153,启动检索需要约3S
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['SendRawData:raw data: :[ 2e f1 53 06 ]',#检查写入F15306
    #                                                                             #    ', error code:0, serial number:1, task type:1',#检查Flag置位 SOA-25497偏差
    #                                                                                '"stateCode":"03F7"',#检查上报TSP 失败不可开车
    #                                                                                'SendToMonitorServer:Send to monitor'
    #                                                                                ],timeout=60):
    #         pass
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['SetVFCReqDiagnosticCb: VfcType :23',#检查停发唤醒
    #                                                                                         'onTimer:Send 3E 80',#检查停发唤醒
    #                                                                                         ],timeout=60):
    #         pass                                                               
    #     assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value,'当前不在失败不可开车状态'
    #     assert self.bus_comm.check_InfoCan_FOTAStatus(infocanfotastatus=InfoCanFOTAStatus.UpdateFailNotDriving.value),'InfoCan FOTAStatus 非 UpdateFailNotDriving'

    @pytest.mark.ecu_mock
    @allure.title("有SRS升级_失败不可开车退出_重启不响应）") 
    def test_fota_caseid_1987599(self):
        self.mix.update_version_debug(self.taskid,["SRS"])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid) 
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
        self.diag_mock.update_0x11_data(ecu_name="SRS", reset_type={0x01: {"NRC":"no_reply"}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"030A"',#检查上报code 进boot失败
                                                                                    'ChangeState:hv_ecu_upgrade => exit_ota',#检查Post Update步骤
                                                                                   'SendRawData:raw data: :[ 10 81 ]',#检查Post Update步骤
                                                                                   'FinToSendChangeSessionReqCb:notify door is availabl',#检查Post Update步骤
                                                                                   'ChangeState:exit_ota => failed',#检查第一轮失败
                                                                                   'QuitFotaModeCb:quit_fota_mode_ecu_info, ecu_name:TCAM',#检查退出流程第一阶段退FOTAMODE
                                                                                   'SendRawData:raw data: :[ 2e f1 53 00 ]',#j检查退出流程第一阶段写入F153 00
                                                                                   'ChangeState:failed => rescue_query_task',#检查进入救援流程
                                                                                   'ChangeState:rescue_pre_check => failed_not_driving',#检查进入救援失败不可开车
                                                                                   'IsAllUasInIdleCb:not in idle ua count:0',#检查退出流程第二阶段拉齐UA
                                                                                   'findEcuFromTaskinfo:has find in task ecu id: 5031, found: 1',#检查到存在SRS升级任务
                                                                                  ], timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        time.sleep(25) #检测到本次任务中存在SRS升级需等待30S进行重启SRS 启动检索需要约3S
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['SendRawData:raw data: :[ 11 01 ]',#检查重启SRS
                                                                                    'SendRawData:raw data: :[ 11 01 ]',#检查重启SRS重试第一次
                                                                                    'SendRawData:raw data: :[ 11 01 ]',#检查重启SRS重试第二次
                                                                                    'reset srs  waiting 5s to start version collection'#检查重启后等待5S进行下一步
                                                                                    ],timeout=60):
            pass
        time.sleep(2) #重启SRS后需等待5s,进行版本校验 写入F153,启动检索需要约3S
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['SendRawData:raw data: :[ 2e f1 53 06 ]',#检查写入F15306
                                                                                #    ', error code:0, serial number:1, task type:1',#检查Flag置位 SOA-25497偏差
                                                                                   '"stateCode":"03F7"',#检查上报TSP 失败不可开车
                                                                                   'SendToMonitorServer:Send to monitor'
                                                                                   ],timeout=60):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['SetVFCReqDiagnosticCb: VfcType :23',#检查停发唤醒
                                                                                            'onTimer:Send 3E 80',#检查停发唤醒
                                                                                            ],timeout=60):
            pass                                                               
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value,'当前不在失败不可开车状态'
        assert self.bus_comm.check_InfoCan_FOTAStatus(infocanfotastatus=InfoCanFOTAStatus.UpdateFailNotDriving.value),'InfoCan FOTAStatus 非 UpdateFailNotDriving'

    @pytest.mark.smoke
    @allure.title("无SRS升级成功退出（03F9/03F6）") 
    def test_fota_caseid_1983079(self):
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid) 
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['SendRawData:raw data: :[ 10 81 ]',#检查Post Update步骤
                                                                                   'FinToSendChangeSessionReqCb:notify door is availabl',#检查Post Update步骤
                                                                                   'ChangeState:exit_ota => success',#检查升级成功
                                                                                   '"stateCode":"03F9"',#检查上报code:03F9 Update Finish
                                                                                   'waiting 20s to start version collection'
                                                                                 ], timeout=900):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['CheckDomainsDoIpConnection:addr:',#检查启动doip检测
                                                                                    'CollectECUsVersionCB:next',#检查版本校验结果
                                                                                    'QuitFotaModeCb:quit_fota_mode_ecu_info, ecu_name:TCAM,ecu quit_fota_mode: 1',#检查退fotamode
                                                                                    '2e f1 53 00',#检查写入F153 00
                                                                                    'IsAllUasInIdleCb:not in idle ua count:0',#检查拉齐UA
                                                                                    '14 ff ff ff',#检查清除DTC 3次
                                                                                    '14 ff ff ff',#检查清除DTC 3次
                                                                                    '14 ff ff ff',#检查清除DTC 3次
                                                                                    'writeBaseline:set f150 succeed',#检查写入F150 成功
                                                                                    'writeDisplayBaseLine:set f151 succeed',#检查写入F151 成功
                                                                                    '1 ,progress:100',#检查进度100
                                                                                    '"stateCode":"03F6"'#检查上报code: 03 F6 UpdateComplete
                                                                                    ],timeout=103):
            pass                                                         
        assert self.soa.get_fota_UpdateProcess(MASTER_UpdateProcess_EVENT.progress) == 100 ,'当前获取通知CDC升级进度不是100'
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.SUCCESSFUL.value,'当前不在升级成功状态' 
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['SetVFCReqDiagnosticCb: VfcType :23',#检查停发唤醒
        #                                                                                     'onTimer:Send 3E 80',#检查停发唤醒
        #                                                                                     ],timeout=60):
        #     pass  https://jira.jiduauto.com/browse/SOA-25560 
        time.sleep(20) #20秒后状态机从Suc > Idle, InfoCan Fotastatus == 0
        assert self.ssh.check_file_existence(DeviceName.BGM, path="/update/ua", filename="*.bin") == False, "未删包"
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value,'当前不在Idle状态'
        assert self.bus_comm.check_InfoCan_FOTAStatus(infocanfotastatus=InfoCanFOTAStatus.Idle.value),'InfoCan FOTAStatus 非 Idle'
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['SetVFCReqDiagnosticCb: VfcType :23',#检查停发唤醒
                                                                                            'onTimer:Send 3E 80',#检查停发唤醒
                                                                                            ],timeout=60):
            pass

if __name__ == "__main__":
    pass

    




