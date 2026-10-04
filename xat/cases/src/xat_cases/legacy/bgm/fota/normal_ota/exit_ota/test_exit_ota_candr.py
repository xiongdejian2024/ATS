import os
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
from xat_ecu.api.common.common import set_bench_vlan9_ip
from xat_ecu.legacy.common.data_handle import *
from xat_ecu.legacy.protocol.ProtocolServerKeywords import ProtocolServerKeywords

@pytest.mark.ecu_mock
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota_CANDR(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("V2TRoutingForwarder","client","V2TOTAFotaForwarder")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    'baseline:6100000210AHO',
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ])
        self.mix.update_version_debug(self.taskid,["SRS"], baseline='6100000210AHO') 
        set_bench_vlan9_ip("172.16.9.21")
        self.server_mock = ProtocolServerKeywords('doip', '172.16.9.21', 13400)
        self.server_mock.init_middleware()
        self.ssh.type_commands(DeviceName.BGM,"cp /data/debug_bak.sh /data/debug.sh;sync")
        self.ssh.type_commands(DeviceName.BGM,"cd /data;chmod 777 debug.sh;sync")
        self.ssh.type_commands(DeviceName.BGM,"cd /data;chmod -R 777 sl;sync")
        self.ssh.type_commands(DeviceName.BGM,"cd /data;/app/bin/swdl -nw 10 1;sync") 
        self.io.bgm_power_off()
        sleep(3)
        self.io.bgm_power_on()
        sleep(20)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.mix.fota_back_to_idle()

    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.server_mock.doip_sock_obj.tcp_server_sock.stop()
        self.ssh.type_commands(DeviceName.BGM,"cd /data;/app/bin/swdl -nw 10 0;sync")
        self.ssh.type_commands(DeviceName.BGM,"cd /data;rm debug_script_executed_count;rm -rf debug.sh;sync")

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_status_Failed_Can_Driving") 
    def test_fota_caseid_1984878(self):
        self.mix.update_version_debug(self.taskid,["OtherEcu"], baseline='6100000210AHO')
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1201: {
                0x22: {
                    0xf186: ['62f18601']
                }, 
                0x31: {
                    0x01a100: ['7101a1001000']
                }
            },
            0x1202: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1402: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1401: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000'],
                }
            },
            0x1630: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x014289: ['710142891001'],
                    0x014000: ['710140001001']
                }
            }
        })
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.ssh.type_commands(DeviceName.BGM,"rm -rf /update/fota/61503*.bin")
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.FAILED_DRIVING.value, timeout=600)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_REMOTE_UPDATE discarded', timeout=10):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.trigger_fota_type90(self.taskid)

    @pytest.mark.V2_1_0
    @pytest.mark.full
    @allure.title("立即升级-BGM在FAILED_DRIVING状态下收到StartUpdate请求，忽略处理") 
    def test_fota_caseid_1994260(self):
        self.mix.update_version_debug(self.taskid,["OtherEcu"], baseline='6100000210AHO')
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1201: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000']
                }
            },
            0x1202: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1402: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1401: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000'],
                }
            },
            0x1630: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x014289: ['710142891001'],
                    0x014000: ['710140001001']
                }
            }
        })
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.ssh.type_commands(DeviceName.BGM,"rm -rf /update/fota/61503*.bin")
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.FAILED_DRIVING.value, timeout=600)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_START_UPDATE discarded', timeout=30):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @pytest.mark.ecu_mock
    @allure.title("有SRS升级_失败不可开车退出_重启否定响应）") 
    def test_fota_caseid_1987600(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1201: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000']
                }
            },
            0x1202: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1402: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1401: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000'],
                }
            },
            0x1630: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x014289: ['710142891001'],
                    0x014000: ['710140001001']
                }
            },
            0x1c01: {
                0x11: {
                    0x01: ['7F1122']
                }
            }
        })
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
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
        with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='" fota:"', keywords=['11 01',#检查重启SRS
                                                                                                    '7f 11 22',#检查 mock SRS 否定响应
                                                                                                    '11 01',#检查重启SRS重试第一次
                                                                                                    '7f 11 22',#检查 mock SRS 否定响应
                                                                                                    '11 01',#检查重启SRS重试第二次
                                                                                                    '7f 11 22',#检查 mock SRS 否定响应
                                                                                                    'reset srs  waiting 5s to start version collection',#检查重启后等待5S进行下一步
                                                                                                    '2e f1 53 06',#检查写入F15306
                                                                                                    #    ', error code:0, serial number:1, task type:1',#检查Flag置位 SOA-25497偏差
                                                                                                    '"stateCode":"03F7"'#检查上报TSP 失败不可开车
                                                                                                    ],timeout=20):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['SetVFCReqDiagnosticCb: VfcType :23',#检查停发唤醒
                                                                                            'onTimer:Send 3E 80',#检查停发唤醒
                                                                                            ],timeout=60):
            pass                                                               
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value,'当前不在失败不可开车状态'
        assert self.bus_comm.check_InfoCan_FOTAStatus(infocanfotastatus=InfoCanFOTAStatus.UpdateFailNotDriving.value),'InfoCan FOTAStatus 非 UpdateFailNotDriving'

    @pytest.mark.ecu_mock
    @allure.title("有SRS升级_失败不可开车退出）") 
    def test_fota_caseid_1987601(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1201: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000']
                }
            },
            0x1202: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1402: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1401: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000'],
                }
            },
            0x1630: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x014289: ['710142891001'],
                    0x014000: ['710140001001']
                }
            },
            0x1c01: {
                0x11: {
                    0x01: ['5101']
                }
            }
        })
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
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
                                                                                  ], timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        time.sleep(25) #检测到本次任务中存在SRS升级需等待30S进行重启SRS 启动检索需要约3S
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['SendRawData:raw data: :[ 11 01 ]',#检查重启SRS
                                                                                    'ResetEcu1101Cb:, data::[ 51 01 ]',#检查 mock SRS 肯定响应
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

    @pytest.mark.V2_1_0
    @pytest.mark.full
    @allure.title("有SRS升级成功退出流程_重启无响应") 
    def test_fota_caseid_1987589(self):
        target_soft_id = self.tsp.get_softid_from_taskid(task_id=self.taskid)
        _,_,target_SRS_version = self.tsp.get_target_version_from_softid(soft_id=target_soft_id,ecu_name='SRS')
        target_SRS_app_ver = target_SRS_version['app_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['app_version'][-3:]])
        target_SRS_sbl_ver = target_SRS_version['SBL_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['SBL_version'][-3:]])
        target_SRS_data_ver = target_SRS_version['DATA_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['DATA_version'][-3:]])
        target_SRS_data1_ver = target_SRS_version['DATA2_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['DATA2_version'][-3:]])
        target_SRS_data2_ver = target_SRS_version['DATA3_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['DATA3_version'][-3:]])
        logger.info(f"app_ver:{target_SRS_app_ver},sbl_ver:{target_SRS_sbl_ver},data_ver:{target_SRS_data_ver},data1_ver:{target_SRS_data1_ver},data2_ver:{target_SRS_data2_ver}")
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1201: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000']
                }
            },
            0x1202: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1402: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1401: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000'],
                }
            },
            0x1630: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x014289: ['710142891001'],
                    0x014000: ['710140001001']
                }
            },
            0x1c01: {
                0x22: {
                    0xf1aa: ['62f1aa8894521092202041'],
                    0xf1ae: ['62f1ae04' + target_SRS_app_ver + target_SRS_data_ver + target_SRS_data1_ver + target_SRS_data2_ver],
                    0xf186: ['62f18602'],
                    0xd01c: ['7f2222']
                },
                0x31: {
                    0x010206: ['710102061001'],
                    0x01ff00: ['7101ff0010'],
                    0x010205: ['710102051000000000'],
                    0x01a100: ['7101a1001000'],
                    0x010212: ['710102121000'],
                    0x010301: ['7101030110']
                },
                0x34: {
                    0x10: ['74200400']
                },
                0x10: {
                    0x02: ['5002001901f4']
                },
                0x27:{
                    0x01: ['6701be6769'],
                    0x02: ['6702']
                }
            }
        })
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['=> exit_ota',#检查Post Update步骤
                                                                                   'SendRawData:raw data: :[ 10 81 ]',#检查Post Update步骤
                                                                                   'FinToSendChangeSessionReqCb:notify door is availabl',#检查Post Update步骤
                                                                                   'ChangeState:exit_ota => success',#流程第二阶段拉齐UA
                                                                                   'findEcuFromTaskinfo:has find in task ecu id: 5031, found: 1',#检查到存在SRS升级任务
                                                                                  ], timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        time.sleep(25) #检测到本次任务中存在SRS升级需等待30S进行重启SRS 启动检索需要约3S
        with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='" fota:"', keywords=['11 01',#检查重启SRS
                                                                                                    '11 01',#检查重启SRS重试第一次
                                                                                                    '11 01',#检查重启SRS重试第二次
                                                                                                    'reset srs  waiting 5s to start version collection',#检查重启后等待5S进行下一步
                                                                                                    'GetVehicleECUVersion:',#开始版本收集
                                                                                                    'CollectECUsVersionCB:next state is checkOtaTask',#版本校验完成
                                                                                                    'QuitFotaModeCb:is_all_ecus_quit_fotamode:',#退出FOTAMODE
                                                                                                    '31 01 40 00 00',#恢复高压
                                                                                                    '2e f1 53 00',#写入F153 00
                                                                                                    '14 ff ff ff',#检查清除DTC 3次
                                                                                                    '14 ff ff ff',#检查清除DTC 3次
                                                                                                    '14 ff ff ff',#检查清除DTC 3次
                                                                                                    'writeBaseline:set f150 succeed',#写入F150
                                                                                                    'writeDisplayBaseLine:set f151 succeed',#写入F151
                                                                                                    '"stateCode":"03F6"'#上报升级失败code 03F6
                                                                                                    ],timeout=40):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.SUCCESSFUL.value, 100)
        assert self.soa.get_fota_UpdateProcess(MASTER_UpdateProcess_EVENT.progress) == 100 ,'当前获取通知CDC升级进度不是100' 
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


    @pytest.mark.V2_1_0
    @pytest.mark.full
    @allure.title("有SRS升级成功退出流程_重启否定响应") 
    def test_fota_caseid_1987590(self):
        target_soft_id = self.tsp.get_softid_from_taskid(task_id=self.taskid)
        _,_,target_SRS_version = self.tsp.get_target_version_from_softid(soft_id=target_soft_id,ecu_name='SRS')
        target_SRS_app_ver = target_SRS_version['app_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['app_version'][-3:]])
        target_SRS_sbl_ver = target_SRS_version['SBL_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['SBL_version'][-3:]])
        target_SRS_data_ver = target_SRS_version['DATA_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['DATA_version'][-3:]])
        target_SRS_data1_ver = target_SRS_version['DATA2_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['DATA2_version'][-3:]])
        target_SRS_data2_ver = target_SRS_version['DATA3_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['DATA3_version'][-3:]])
        logger.info(f"app_ver:{target_SRS_app_ver},sbl_ver:{target_SRS_sbl_ver},data_ver:{target_SRS_data_ver},data1_ver:{target_SRS_data1_ver},data2_ver:{target_SRS_data2_ver}")
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1201: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000']
                }
            },
            0x1202: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1402: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1401: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000'],
                }
            },
            0x1630: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x014289: ['710142891001'],
                    0x014000: ['710140001001']
                }
            },
            0x1c01: {
                0x22: {
                    0xf1aa: ['62f1aa8894521092202041'],
                    0xf1ae: ['62f1ae04' + target_SRS_app_ver + target_SRS_data_ver + target_SRS_data1_ver + target_SRS_data2_ver],
                    0xf186: ['62f18602'],
                    0xd01c: ['7f2222'],
                },
                0x31: {
                    0x010206: ['710102061001'],
                    0x01ff00: ['7101ff0010'],
                    0x010205: ['710102051000000000'],
                    0x01a100: ['7101a1001000'],
                    0x010212: ['710102121000'],
                    0x010301: ['7101030110']
                },
                0x34: {
                    0x10: ['74200400']
                },
                0x10: {
                    0x02: ['5002001901f4']
                },
                0x11: {
                    0x01: ['7F1122']
                    },
                0x27:{
                    0x01: ['6701be6769'],
                    0x02: ['6702']
                }
            }
        })
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['=> exit_ota',#检查Post Update步骤
                                                                                   'SendRawData:raw data: :[ 10 81 ]',#检查Post Update步骤
                                                                                   'FinToSendChangeSessionReqCb:notify door is availabl',#检查Post Update步骤
                                                                                   'ChangeState:exit_ota => success',#流程第二阶段拉齐UA
                                                                                   'findEcuFromTaskinfo:has find in task ecu id: 5031, found: 1',#检查到存在SRS升级任务
                                                                                  ], timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        time.sleep(25) #检测到本次任务中存在SRS升级需等待30S进行重启SRS 启动检索需要约3S
        with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='" fota:"', keywords=['11 01',#检查重启SRS
                                                                                                    '7f 11 22',#检查 mock SRS 否定响应
                                                                                                    '11 01',#检查重启SRS重试第一次
                                                                                                    '7f 11 22',#检查 mock SRS 否定响应
                                                                                                    '11 01',#检查重启SRS重试第二次
                                                                                                    '7f 11 22',#检查 mock SRS 否定响应
                                                                                                    'reset srs  waiting 5s to start version collection',#检查重启后等待5S进行下一步
                                                                                                    'GetVehicleECUVersion:',#开始版本收集
                                                                                                    'CollectECUsVersionCB:next state is checkOtaTask',#版本校验完成
                                                                                                    'QuitFotaModeCb:is_all_ecus_quit_fotamode:',#退出FOTAMODE
                                                                                                    '31 01 40 00 00',#恢复高压
                                                                                                    '2e f1 53 00',#写入F153 00
                                                                                                    '14 ff ff ff',#检查清除DTC 3次
                                                                                                    '14 ff ff ff',#检查清除DTC 3次
                                                                                                    '14 ff ff ff',#检查清除DTC 3次
                                                                                                    'writeBaseline:set f150 succeed',#写入F150
                                                                                                    'writeDisplayBaseLine:set f151 succeed',#写入F151
                                                                                                    '"stateCode":"03F6"'#上报升级失败code 03F6
                                                                                                    ],timeout=40):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.SUCCESSFUL.value, 100)
        assert self.soa.get_fota_UpdateProcess(MASTER_UpdateProcess_EVENT.progress) == 100 ,'当前获取通知CDC升级进度不是100' 
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

    @pytest.mark.V2_1_0
    @pytest.mark.smoke
    @allure.title("有SRS升级成功退出（03F9/03F6）") 
    def test_fota_caseid_1987591(self):
        target_soft_id = self.tsp.get_softid_from_taskid(task_id=self.taskid)
        _,_,target_SRS_version = self.tsp.get_target_version_from_softid(soft_id=target_soft_id,ecu_name='SRS')
        target_SRS_app_ver = target_SRS_version['app_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['app_version'][-3:]])
        target_SRS_sbl_ver = target_SRS_version['SBL_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['SBL_version'][-3:]])
        target_SRS_data_ver = target_SRS_version['DATA_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['DATA_version'][-3:]])
        target_SRS_data1_ver = target_SRS_version['DATA2_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['DATA2_version'][-3:]])
        target_SRS_data2_ver = target_SRS_version['DATA3_version'][:-3] + "".join([hex(ord(char))[2:] for char in target_SRS_version['DATA3_version'][-3:]])
        logger.info(f"app_ver:{target_SRS_app_ver},sbl_ver:{target_SRS_sbl_ver},data_ver:{target_SRS_data_ver},data1_ver:{target_SRS_data1_ver},data2_ver:{target_SRS_data2_ver}")
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1201: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000']
                }
            },
            0x1202: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1402: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1401: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000'],
                }
            },
            0x1630: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x014289: ['710142891001'],
                    0x014000: ['710140001001']
                }
            },
            0x1c01: {
                0x22: {
                    0xf1aa: ['62f1aa8894521092202041'],
                    0xf1ae: ['62f1ae04' + target_SRS_app_ver + target_SRS_data_ver + target_SRS_data1_ver + target_SRS_data2_ver],
                    0xf186: ['62f18602'],
                    0xd01c: ['7f2222'],
                },
                0x31: {
                    0x010206: ['710102061001'],
                    0x01ff00: ['7101ff0010'],
                    0x010205: ['710102051000000000'],
                    0x01a100: ['7101a1001000'],
                    0x010212: ['710102121000'],
                    0x010301: ['7101030110']
                },
                0x34: {
                    0x10: ['74200400']
                },
                0x10: {
                    0x02: ['5002001901f4']
                },
                0x11: {
                    0x01: ['5101']
                    },
                0x27:{
                    0x01: ['6701be6769'],
                    0x02: ['6702']
                }
            }
        })
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['=> exit_ota',#检查Post Update步骤
                                                                                   'SendRawData:raw data: :[ 10 81 ]',#检查Post Update步骤
                                                                                   'FinToSendChangeSessionReqCb:notify door is availabl',#检查Post Update步骤
                                                                                   'ChangeState:exit_ota => success',#流程第二阶段拉齐UA
                                                                                   'findEcuFromTaskinfo:has find in task ecu id: 5031, found: 1',#检查到存在SRS升级任务
                                                                                  ], timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        time.sleep(25) #检测到本次任务中存在SRS升级需等待30S进行重启SRS 启动检索需要约3S
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['SendRawData:raw data: :[ 11 01 ]',#检查重启SRS
                                                                                    'ResetEcu1101Cb:, data::[ 51 01 ]'],timeout=60):
            pass
        time.sleep(2) #重启SRS后需等待5s,进行版本校验 写入F153,启动检索需要约3S
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['GetVehicleECUVersion:',#开始版本收集
                                                                                   'CollectECUsVersionCB:',#版本校验
                                                                                   'QuitFotaModeCb:is_all_ecus_quit_fotamode:',#退出FOTAMODE
                                                                                   'SendRawData:raw data: :[ 31 01 40 00 00 ]',#恢复高压
                                                                                   '2e f1 53 00',#写入F153 00 
                                                                                   'ClearAllEcuDTC:count:3',#清除DTC
                                                                                   'writeBaseline:set f150 succeed',#写入F150
                                                                                   'writeDisplayBaseLine:set f151 succeed',#写入F151
                                                                                   '"stateCode":"03F6"'#上报升级成功code 03方
                                                                                   ],timeout=60):
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

    @pytest.mark.V2_1_0
    @pytest.mark.smoke
    @allure.title("诊断_OTA Cancel_UpdateFailedCanDriving_succeed") 
    def test_fota_caseid_1982921(self):
        self.mix.update_version_debug(self.taskid,["OtherEcu"], baseline='6100000210AHO')
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1201: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000']
                }
            },
            0x1202: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1402: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1401: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000'],
                }
            },
            0x1630: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x014289: ['710142891001'],
                    0x014000: ['710140001001']
                }
            }
        })
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.ssh.type_commands(DeviceName.BGM,"rm -rf /update/fota/61503*.bin")
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.FAILED_DRIVING.value, timeout=600)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"05F1"', timeout=120):
            self.sd_tester.diag_cancel() #SOA-29717
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120)
        assert self.ssh.check_file_existence(DeviceName.BGM, path="/update/fota", filename="*.bin") == False, "/update/fota下存在小ecu bin包"

    @pytest.mark.V2_1_0
    @pytest.mark.full
    @allure.title("云端取消FOTA_当前处于UpdateFailedCanDriving状态_取消成功") 
    def test_fota_caseid_1993262(self):
        self.mix.update_version_debug(self.taskid,["OtherEcu"], baseline='6100000210AHO')
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1201: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000']
                }
            },
            0x1202: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1402: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1401: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000'],
                }
            },
            0x1630: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x014289: ['710142891001'],
                    0x014000: ['710140001001']
                }
            }
        })
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.ssh.type_commands(DeviceName.BGM,"rm -rf /update/fota/61503*.bin")
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.FAILED_DRIVING.value, timeout=600)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"05F1"', timeout=120):
            self.soa.trigger_fota_type70(self.taskid) #SOA-29717
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120)
        assert self.ssh.check_file_existence(DeviceName.BGM, path="/update/fota", filename="*.bin") == False, "/update/fota下存在小ecu bin包"


    @pytest.mark.sanity
    @allure.title("自动救援_type40上报无ECU需要更新_writeDIDTask=1_第一轮退FOTAMODE成功_正向流程")    
    def test_fota_caseid_1989749(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1201: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000']
                }
            },
            0x1202: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1402: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1401: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000'],
                }
            },
            0x1630: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x014289: ['710142891001'],
                    0x014000: ['710140001001']
                }
            }
        })
        self.mix.update_version_debug(self.taskid,['rescueErrorHWPN_BGM'], baseline='6100000210AHO') #输入与实际不一致的HWPN，以制造升级完成版本匹配不一致场景
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.mix.back_fota_to(FOTAMasteSts.UPDATE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => success', timeout=1000):#上报版本校验不一致
            pass
        self.ssh.type_commands(DeviceName.BGM,"cp /data/debug_bak.sh /data/debug.sh;sync")
        self.ssh.type_commands(DeviceName.BGM,"cd /data;chmod 777 debug.sh;sync")
        self.ssh.type_commands(DeviceName.BGM,"cd /data;chmod -R 777 sl;sync")
        self.ssh.type_commands(DeviceName.BGM,"cd /data;/app/bin/swdl -nw 10 1;sync") 
        self.io.bgm_power_off()
        sleep(3)
        self.io.bgm_power_on()
        sleep(20)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"032A",', timeout=1000):#上报版本校验不一致
            pass
        self.mix.update_version_debug(self.taskid,['rescue_BGM'], baseline='6100000210AHO')#恢复version_debug 软硬件版本号与实际一致
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"type":50,"writeDidTask":1',
                                                                                   'ChangeState:wait_task_info => success_write_baseline',
                                                                                   '2e f1 53 00',
                                                                                   'ClearAllEcuDTC:count:3',
                                                                                   'writeBaseline:set f150 succeed',
                                                                                   'writeDisplayBaseLine:set f151 succeed',
                                                                                   '"stateCode":"03F6"',
                                                                                   'ChangeState:success_write_baseline => update_status_sync'], timeout=600):
            pass
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value 

    @pytest.mark.V2_1_0
    @pytest.mark.full
    @allure.title("有SRS升级_失败可开车退出") 
    def test_fota_caseid_1987598(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1201: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000']
                }
            },
            0x1202: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1402: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1401: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000'],
                }
            },
            0x1630: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x014289: ['710142891001'],
                    0x014000: ['710140001001']
                }
            },
            0x1c01: {
                0x11: {
                    0x01: ['5101']
                    }
            }
        })
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.ssh.type_commands(DeviceName.BGM,"rm -rf /update/fota/*")
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=["ChangeState:exit_ota =>",
                                                                                   'findEcuFromTaskinfo:has find in task ecu id: 5031, found: 1'
                                                                                   ], timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        start_time = time.time()    
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="ResetEcu1101", timeout=60): 
            pass
        end_time = time.time()
        reset_time = end_time - start_time
        assert 29 < reset_time < 31 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['2e f1 53 00',
                                                                                   '14 ff ff ff',
                                                                                   '"stateCode":"03F8"'], timeout=300): 
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 20)

    @pytest.mark.V2_1_0
    @pytest.mark.full
    @allure.title("无SRS升级_失败可开车退出（03F8）") 
    def test_fota_caseid_1987597(self):
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM], baseline='6100000210AHO') 
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1201: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000']
                }
            },
            0x1202: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1402: {
                0x22: {
                    0xf186: ['62f18601']
                }
            },
            0x1401: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x01a100: ['7101a1001000'],
                }
            },
            0x1630: {
                0x22: {
                    0xf186: ['62f18601']
                },
                0x31: {
                    0x014289: ['710142891001'],
                    0x014000: ['710140001001']
                }
            }
        })
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.ssh.type_commands(DeviceName.BGM,"rm -rf /update/ua/*")
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:exit_ota =>',
                                                                                   '2e f1 53 00',
                                                                                   '14 ff ff ff',
                                                                                   '"stateCode":"03F8"'], timeout=900): 
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 10)

    @pytest.mark.V2_1_0
    @pytest.mark.full
    @allure.title("ERROR_CODE重试_03_F8（Update_Failed_CANDRIVING）") 
    def test_fota_caseid_1979761(self):
        try:
            self.mix.update_version_debug(self.taskid,["CD"], baseline='6100000210AHO') 
            self.server_mock.clear_mock_data_0x8001()
            self.server_mock.doip_update_service_data_0x8001({
                0x1201: {
                    0x22: {
                        0xf186: ['62f18601']
                    },
                    0x31: {
                        0x01a100: ['7101a1001000']
                    }
                },
                0x1202: {
                    0x22: {
                        0xf186: ['62f18601']
                    }
                },
                0x1402: {
                    0x22: {
                        0xf186: ['62f18601']
                    }
                },
                0x1401: {
                    0x22: {
                        0xf186: ['62f18601']
                    },
                    0x31: {
                        0x01a100: ['7101a1001000'],
                    }
                },
                0x1630: {
                    0x22: {
                        0xf186: ['62f18601']
                    },
                    0x31: {
                        0x014289: ['710142891001'],
                        0x014000: ['710140001001']
                    }
                }
            })
            self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
            self.ssh.type_commands(DeviceName.BGM,"rm -rf /update/fota/*")
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            self.ssh.set_airplane_mode(isOn.On)
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='QuitFotaModeCb:', timeout=900): 
                pass
            with self.log_manage.check_jetlog_by_same_keywords(log_type='" fota:"', keywords=['"stateCode":"03F8"',
                                                                                            '"stateCode":"03F8"',
                                                                                            '"stateCode":"03F8"',
                                                                                            '"stateCode":"03F8"'], timeout=60): 
                pass
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='filterKeyStateCode:state code:03F8, entry_send: 0, success_send:1', timeout=30):
                self.ssh.set_airplane_mode(isOn.Off)
        finally:
            self.ssh.set_airplane_mode(isOn.Off)

if __name__ == "__main__":
    pass

