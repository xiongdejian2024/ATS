#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_KeyService.py
@Time         :2023/04/08 17:20:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import allure
import pytest
import copy
import uuid
from time import sleep
from random import randint
from xat_ecu.legacy.common.data_type_handing import logger, DataTypeHanding
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.digital_key.RVCTSPMessage_pb2 import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *

KEY_MATCH_INFO = {1: [2, 3, 4, 5, 6, 8, 0xA, 0xB],
                  2: [2, 3, 4, 5, 6, 0xA, 0xB],
                  3: [3, 6, 0xA],
                  4: [4, 6, 0xB],
                  6: [8],
                  7: [8],
                  8: [8]
                  }


@allure.feature("SOA服务接口")
@allure.story("整车控制/KeyService")
@pytest.mark.aqx
class TestKeyService(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("KeyService", "client"),
                                     ("CentralLockService", "client"),
                                     ("HornService", "client"),
                                     ("DoorService", "client")
                                     ])
        self.partner.method_default_timeout = 0.1
        self.ipdu.pause_bus_send("chassiscan1")
        self.ipdu.pause_bus_send("chassiscan2")
        self.ipdu.pause_bus_send("passivesafetycan")
        self.ipdu.pause_ecu_send('connectivitycanfd', 'DRMFL')
        self.ipdu.pause_ecu_send('connectivitycanfd', 'DRMFR')
        self.ipdu.pause_ecu_send('connectivitycanfd', 'DRMRL')
        self.ipdu.pause_ecu_send('connectivitycanfd', 'DRMRR')
        self.ipdu.pause_ecu_send('connectivitycanfd', 'TCAM')
        self.ipdu.stop_send_pdu('connectivitycanfd', 0x10)
        self.ipdu.stop_send_pdu('connectivitycanfd', 0x40)
        #抓取tcpdump
        self.bgm_tcpdump = BGM_SSH()
        self.bgm_tcpdump.init_bgm_tcpdump()        

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)   
        self.set_nopeople_incar()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEKeyPrsntStsZone7', 'Validity_NotValid')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1) # MPU侧档位
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)  
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.io.io_obj.set_do_level("horn_switch", False) # 喇叭关闭
        self.dk.empty_dk_data_queue()
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.partner.empty_all(2)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待10s让环境恢复")
            sleep(10)
        else:
            sleep(3)

    def bgm_sleep_and_awake(self):
        pass  # todo

    def ck_pdu(self,file_path,save_name,data_list1,data_list2):
        # todo 停止抓包
        self.bgm_tcpdump.stop_bgm_tcpdump()
        # todo 拉取日志 单个日志 不打包
        file_path=self.bgm_tcpdump.scp_bgm_log_to_local(bgm_log_name=save_name)
        # todo 删除所有 pcap 文件
        self.bgm_tcpdump.delete_bgm_tcpdump_file(bgm_log_name='*.pcap')
        
        #停止和删除 也在aftercase中增加进去
        # 列表里面为元祖（pdu的id，数据长度，信号起始bit位，信号长度，信号值），可以 是多个元祖
        # data_list = [list1]
        ret, res_dict = check_pdu(data_list1, file_path)
        if ret==False :
             assert False, f"对应信号不存在"             
        
        # data_list 格式 为列表，列表里面为元祖（pdu的id，数据长度，信号起始bit未，信号长度），可以 是多个元祖
        # data_list = [list2]  
        res_dict=get_pdu_value_and_time(data_list2, file_path)

    @allure.title("SetCarLocalTraceRequest_无请求")
    @pytest.mark.full
    def test_caseid_105181(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 0})
        # todo: 校验pdu6361，其中ProxyCarFindrHornLiReq=0
        try:
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
                            'ActvnOfIndcrIndcrOut', 'IndcrSts1_LeAndRiOn', 0.8)
        except Exception:
            pass
        else:
            assert False, "信号异常"
        try:
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, "ActvOfHorn", "OnOff1_On", 0.8)
        except Exception:
            pass
        else:
            assert False, "信号异常"
        sleep(3)

    @allure.title("SetCarLocalTraceRequest_喇叭请求")
    @pytest.mark.full
    def test_caseid_105164(self):
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 1})
        for _ in range(2):  # todo: 内部信号320ms周期，总线400ms周期，故存在错位情况，此处只校验2个周期
            # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, "ActvOfHorn", "OnOff1_On", 1)
            # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, "ActvOfHorn", "OnOff1_Off", 1)
            self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 1})
            self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 0})

    @allure.title("SetCarLocalTraceRequest_灯光请求")
    @pytest.mark.full
    def test_caseid_105177(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 2})
        for _ in range(3):
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
                            'ActvnOfIndcrIndcrOut', 'IndcrSts1_LeAndRiOn', 0.5)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, "ActvOfHorn", "OnOff1_Off", 0.1)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
                            'ActvnOfIndcrIndcrOut', 'IndcrSts1_Off', 0.5)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, "ActvOfHorn", "OnOff1_Off", 0.1)
        sleep(3)

    @allure.title("SetCarLocalTraceRequest_喇叭和灯光同时请求")
    @pytest.mark.full
    def test_caseid_1913299(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 3})
        for _ in range(3):
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
                            'ActvnOfIndcrIndcrOut', 'IndcrSts1_LeAndRiOn')
            # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, "ActvOfHorn", "OnOff1_On") 
            self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 0}) 
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
                            'ActvnOfIndcrIndcrOut', 'IndcrSts1_Off')
            # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, "ActvOfHorn", "OnOff1_Off")
            self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 1})
        sleep(3)

    @allure.title("GetCarLocalTraceActiveStatus_无请求_返回未寻车")
    @pytest.mark.full
    def test_caseid_105195(self):
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, 'GetCarLocalTraceActiveStatus',
                                              {}, {"out": 0})
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr05, 'CarLoctrActvnSts', 0)
        sleep(3)

    @allure.title("GetCarLocalTraceActiveStatus_喇叭请求_返回寻车成功")
    @pytest.mark.sanity
    def test_caseid_105180(self):
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 1})
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr05, 'CarLoctrActvnSts', 1)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, 'GetCarLocalTraceActiveStatus',
                                              {}, {"out": 1})
        sleep(3)

    @allure.title("GetCarLocalTraceActiveStatus_喇叭请求_返回寻车失败")
    @pytest.mark.full
    def test_caseid_105172(self):
        self.sd_tester.change_usage_mode(0)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 3})
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr05, 'CarLoctrActvnSts', 2)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, 'GetCarLocalTraceActiveStatus',
                                              {}, {"out": 2})
        sleep(3)

    @allure.title("NotifyCarLocalTraceActiveStatus_喇叭请求_返回寻车成功")
    @pytest.mark.sanity
    def test_caseid_1913300(self):
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 1})
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "NotifyCarLocalTraceActiveStatus", {"sts": 1})
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr05, 'CarLoctrActvnSts', 1)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "NotifyCarLocalTraceActiveStatus", {"sts": 0})
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr05, 'CarLoctrActvnSts', 0)

    @allure.title("NotifyCarLocalTraceActiveStatus_喇叭请求_返回寻车失败")
    @pytest.mark.full
    def test_caseid_105149(self):
        self.sd_tester.change_usage_mode(0)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 1})
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "NotifyCarLocalTraceActiveStatus", {"sts": 2})
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr05, 'CarLoctrActvnSts', 2)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "NotifyCarLocalTraceActiveStatus", {"sts": 0})
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr05, 'CarLoctrActvnSts', 0)

    @allure.title("SetDigitalKeyUnlockEvent_Trigger=0+Type=0+Info=0_保持last_value")
    @pytest.mark.full
    def test_caseid_105176(self):
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        digital_key_info = {"type": 0,
                            "trigger": 0,
                            "keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetDigitalKeyUnlockEvent",
                                         {'info': digital_key_info})
        sleep(2)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {},
                                              {"out": [{"type": 1,
                                                        "trigger": 3,
                                                        "keyId": key_id1}]})
        try:
            self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId", digital_key_info)
        except Exception:
            pass
        else:
            assert False, "不应该上报"

    @allure.title("SetDigitalKeyUnlockEvent_Trigger=1+Type=1+Info=0_保持last_value")
    @pytest.mark.full
    def test_caseid_105167(self):
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        digital_key_info = {"type": 1,
                            "trigger": 1,
                            "keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetDigitalKeyUnlockEvent",
                                         {'info': digital_key_info})
        sleep(2)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {},
                                              {"out": [{"type": 1,
                                                        "trigger": 3,
                                                        "keyId": key_id1}]})
        try:
            self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId", digital_key_info)
        except Exception:
            pass
        else:
            assert False, "不应该上报"

    @allure.title("SetDigitalKeyUnlockEvent_Trigger=0+Type=1+Info=1_保持last_value")
    @pytest.mark.full
    def test_caseid_105162(self):
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        digital_key_info = {"type": 1,
                            "trigger": 0,
                            "keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetDigitalKeyUnlockEvent",
                                         {'info': digital_key_info})
        sleep(2)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {},
                                              {"out": [{"type": 1,
                                                        "trigger": 3,
                                                        "keyId": key_id1}]})
        try:
            self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId", digital_key_info)
        except Exception:
            pass
        else:
            assert False, "不应该上报"

    @allure.title("SetDigitalKeyUnlockEvent_Trigger=1+Type=0+Info=1_保持last_value")
    @pytest.mark.full
    def test_caseid_105153(self):
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(2)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetDigitalKeyUnlockEvent",
                                         {'info': {"type": 0,
                                                   "trigger": 1,
                                                   "keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}})
        self.partner.ck_no_event_and_ck_resp(KEY_SERVICE_CLIENT, "DigitalKeyId", 
                                             {"out": [{"type": 1,
                                                        "trigger": 3,
                                                        "keyId": key_id1}]}, timeout=3)

    @allure.title("SetDigitalKeyUnlockEvent_Trigger=1+Type从1到9遍历+Info=16byte随机数_更新new_value")
    @pytest.mark.full
    def test_caseid_105196(self):
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        for i in range(1, 10):
            digital_key_info = {"type": i,
                                "trigger": 1,
                                "keyId": [randint(0x0, 0xF) for i in range(16)]}
            self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetDigitalKeyUnlockEvent", {'info': digital_key_info})
            self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId", {"info": digital_key_info})
            self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {},
                                                  {"out": [digital_key_info]})
        
    @allure.title("数字钥匙触发事件信息_PDUID校验")
    @pytest.mark.smoke
    def test_caseid_1980822(self):
        file_path, save_name = self.bgmcli.start_bgm_tcpdump()        
        self.dk.set_cenlock_sts(3)
        sleep(2)
        #靠近迎宾 "type":3,"trigger":1,"
        self.dk.send_approach_light_cmd(key_type=3, key_id=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3])
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId",
                                  {'info': {"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                                            "trigger": 1,
                                            "type": 3}})
        # NFC刷卡解锁 "type":1,"trigger":3
        self.partner.empty_all()
        self.dk.send_nfc_cmd()
        self.dk.ck_cenlock_sts(1)
        sleep(5)
        data_list = [(15011, 18, 130, 3), (15011, 18, 139, 4)]
        res_dict = self.stop_tcpdump_and_copy_and_calculate(save_name, data_list)
        
    @allure.title("JBS-21261数字钥匙触发事件信息_靠近车辆触发迎宾后NFC闭锁")
    @pytest.mark.full
    def test_caseid_1912544(self):     
        self.dk.set_cenlock_sts(3)
        sleep(2)
        #靠近迎宾 "type":3,"trigger":1,"
        self.dk.send_approach_light_cmd(key_type=3, key_id=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3])
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId",
                                  {'info': {"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                                            "trigger": 1,
                                            "type": 3}})
        # NFC刷卡解锁 "type":1,"trigger":3
        self.partner.empty_all()
        self.dk.send_nfc_cmd()
        self.dk.ck_cenlock_sts(1)
        sleep(10)
        logger.info(f"获取partner的所有event")
        for event in list(self.partner.partner_infos[KEY_SERVICE_CLIENT].event_queue.queue):
            logger.info(f"event={event}")
            if event['function'] == "UpdateDigitalKeyIdEvent":
                raw_data = eval(event['args'])['info']
                logger.info(f"raw={raw_data}，type={raw_data['type']},trigger={raw_data['trigger']}")
                if raw_data['keyId'] != key_id1 or raw_data['type'] != 1 or raw_data['trigger'] != 3:
                    logger.info(f"raw={raw_data}，type={raw_data['type']},trigger={raw_data['trigger']}")
                    assert False, f"报文发送不同时"  
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {},
                                                  {"out": [{'keyId': key_id1, 'type': 1, 'trigger': 3}]})    
        
    @allure.title("SetDigitalKeyUnlockEvent_Trigger=2+Type从1到9遍历+Info=16byte随机数_更新new_value")
    @pytest.mark.sanity
    def test_caseid_105165(self):
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        for i in range(1, 10):
            digital_key_info = {"type": i,
                                "trigger": 2,
                                "keyId": [randint(0x0, 0xF) for i in range(16)]}
            self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetDigitalKeyUnlockEvent", {'info': digital_key_info})
            self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId", {"info": digital_key_info})
            self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {},
                                                  {"out": [digital_key_info]})

    @allure.title("SetDigitalKeyUnlockEvent_Trigger=3+Type从1到9遍历+Info=16byte随机数_更新new_value")
    @pytest.mark.full
    def test_caseid_105203(self):
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        for i in range(1, 10):
            digital_key_info = {"type": i,
                                "trigger": 3,
                                "keyId": [randint(0x0, 0xF) for i in range(16)]}
            self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetDigitalKeyUnlockEvent", {'info': digital_key_info})
            self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId", {"info": digital_key_info})
            self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {},
                                                  {"out": [digital_key_info]})

    @allure.title("SetDigitalKeyUnlockEvent_上下电_更新invalid值")
    @pytest.mark.full
    def test_caseid_105159(self):
        self.dk.set_cenlock_sts(3)
        self.dk.set_cenlock_sts(1)
        self.nucapp.bgm_power_off()
        sleep(2)
        self.nucapp.bgm_power_on()
        sleep(15)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {},
                                              {"out": [{"type": 0,
                                                        "trigger": 0,
                                                        "keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}]})

    @allure.title("GetDigitalKeyId_Invalid变为非Invalid值_Trigger=1+Type=3+Info=1")
    @pytest.mark.full
    def test_caseid_105166(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {'infos': [{"key": 2, "value": 1}]})
        sleep(1)
        self.nucapp.bgm_power_off()
        sleep(2)
        self.nucapp.bgm_power_on()
        sleep(10)
        self.dk.send_approach_light_cmd(key_type=3, key_id=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        sleep(2)
        digital_key_info = {"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            "trigger": 1,
                            "type": 3}
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId", {"info": digital_key_info})
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {}, {"out": [digital_key_info]})

    @allure.title("GetDigitalKeyId_非Invalid变为其他非Invalid值")
    @pytest.mark.full
    def test_caseid_105193(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {'infos': [{"key": 2, "value": 1}]})
        self.dk.set_cenlock_sts(3)
        sleep(2)
        self.dk.send_approach_light_cmd(key_type=3, key_id=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3])
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId",
                                  {'info': {"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                                            "trigger": 1,
                                            "type": 3}})
        self.dk.send_approach_unlock_cmd(key_type=2, key_id=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                                                             0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        digital_key_info = {"keyId": [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                                      0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
                            "trigger": 3,
                            "type": 2}
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId", {"info": digital_key_info})
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {}, {"out": [digital_key_info]})

    @allure.title("GetDigitalKeyId_非Invalid变为Invalid值")
    @pytest.mark.smoke
    def test_caseid_105152(self):
        self.dk.set_cenlock_sts(3)
        sleep(2)
        self.dk.send_approach_unlock_cmd(key_type=4, key_id=[0xFF, 0xFF, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.dk.ck_cenlock_sts(1)
        sleep(6)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {},
                                              {"out": [{"type": 4,
                                                        "trigger": 3,
                                                        "keyId": [0xFF, 0xFF, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                  0]}]})

    @allure.title("GetDigitalKeyId_发送通信故障")
    @pytest.mark.full
    def test_caseid_105188(self):
        self.sd_tester.tester_present()
        self.dk.set_cenlock_sts(3)
        sleep(2)
        self.dk.send_approach_unlock_cmd(key_type=2, key_id=[0xFF, 0xFF, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.dk.ck_cenlock_sts(1)
        sleep(6)
        digital_key_info = {"type": 2,
                            "trigger": 3,
                            "keyId": [0xFF, 0xFF, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                      0]}
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {}, {"out": [digital_key_info]})
        self.sd_tester.stop_tester_present()
        # self.sd_tester.reset_ecu()
        # sleep(1)
        # self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {}, {"out": [digital_key_info]})

    @allure.title("DigitalKeyId_MCU上行_Trigger=1+Type=3+Info=1")
    @pytest.mark.smoke
    def test_caseid_105183(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {'infos': [{"key": 2, "value": 1}]})
        self.dk.send_approach_light_cmd(key_type=3, key_id=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        sleep(1)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId",
                                  {"info": {"type": 3, "trigger": 1,
                                            "keyId": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}})
        
    @allure.title("DigitalKeyId_keyType不变_trigger和KeyId变化")
    @pytest.mark.full
    def test_caseid_1983997(self): # 防止出现：keyid和发的对不上 如果第二次和第一次的Key ID有相同的，第二次对应位置就收不到
        self.dk.set_cenlock_sts(3)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {'infos': [{"key": 2, "value": 1}]})
        self.dk.send_approach_light_cmd(key_type=3, key_id=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        sleep(1)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId",
                                  {"info": {"type": 3, "trigger": 1,
                                            "keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}})
        self.dk.send_approach_unlock_cmd(key_type=3, key_id=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
        sleep(2)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId",
                                  {"info": {"type": 3, "trigger": 3,
                                            "keyId": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]}})
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {}, 
                                              {"out": [{"type": 3, "trigger": 3, "keyId": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]}]})
                
    @allure.title("DigitalKeyId_keyType和KeyId不变_trigger变化")
    @pytest.mark.full
    def test_caseid_1983992(self): # KeyID没变过
        self.dk.set_cenlock_sts(3)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {'infos': [{"key": 2, "value": 1}]})
        self.dk.send_approach_light_cmd(key_type=3, key_id=key_id1)
        sleep(1)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId",
                                  {"info": {"type": 3, "trigger": 1,
                                            "keyId": key_id1}})
        self.dk.send_approach_unlock_cmd(key_type=3, key_id=key_id1)
        sleep(2)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId",
                                  {"info": {"type": 3, "trigger": 3,
                                            "keyId": key_id1}})

    @allure.title("DigitalKeyId_NFC重复解锁")
    @pytest.mark.full
    def test_caseid_1984355(self): # 140AN
        self.dk.set_cenlock_sts(3)
        sleep(3)
        self.dk.send_nfc_cmd()
        self.dk.ck_cenlock_sts(1)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId",
                                  {'info': {"keyId": key_id1,
                                            "trigger": 3,
                                            "type": 1}})
        self.dk.set_cenlock_sts(3)
        sleep(2)
        self.dk.ck_cenlock_sts(3)
        sleep(2)
        self.dk.send_nfc_cmd()
        self.dk.ck_cenlock_sts(1)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId",
                                  {'info': {"keyId": key_id1,
                                            "trigger": 3,
                                            "type": 1}})   
        
    @allure.title("DigitalKeyId_收到SetDigitalKeyUnlockEvent调用_参数不为0")
    @pytest.mark.full
    def test_caseid_1984001(self):
        digital_key_info = {"type": 1,
                            "trigger": 2,
                            "keyId": key_id1}
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetDigitalKeyUnlockEvent",
                                         {'info': digital_key_info})
        sleep(2)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId", {"info": digital_key_info})
        
        digital_key_info = {"type": 1,
                            "trigger": 3,
                            "keyId": key_id1}
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetDigitalKeyUnlockEvent",
                                         {'info': digital_key_info})
        sleep(2)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId", {"info": digital_key_info})
        
        digital_key_info = {"type": 1,
                            "trigger": 3,
                            "keyId": key_id1}
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetDigitalKeyUnlockEvent",
                                         {'info': digital_key_info})
        sleep(2)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId", {"info": digital_key_info})        
                
    @allure.title("DigitalKeyId_MCU上行_Trigger=3+Type=3+Info=1")
    @pytest.mark.sanity
    def test_caseid_105200(self):
        self.dk.set_cenlock_sts(3)
        self.dk.send_approach_unlock_cmd(key_type=3, key_id=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        sleep(1)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId",
                                  {"info": {"type": 3, "trigger": 3,
                                            "keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}})

    @allure.title("GetFindKeyResult_zone0-10遍历_未调用寻钥匙")
    @pytest.mark.sanity
    def test_caseid_105158(self):
        for i in range(11):
            self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetFindKeyResult", {"zone": i},
                                                  {"out": {"zone": i, "result": 0}})
            sleep(0.5)

    @allure.title("SetFindKeyZone_zone(10)_BGM不发寻钥匙")
    @pytest.mark.full
    def test_caseid_105198(self):
        self.dk.empty_dk_data_queue()
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetFindKeyZone", {"zone": 10})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("KeyReadReqFromSrv", [0])
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'KeyReadReqFromSrv', 0, timeout=0.5)
        self.dk.ck_bgm_not_send_cmd("请求Idle=0无效", self.dk.dk_data_queue_key_search)

    @allure.title("SetFindKeyZone_zone(i)_找到单个钥匙_遍历zone0-9_遍历钥匙区域0-12_钥匙类型0-9随机")
    @pytest.mark.sanity
    @pytest.mark.failed
    def test_caseid_1913298(self):
        for zone in range(10):
            if zone == 9:
                continue
            for status in range(13):
                key_type = randint(2, 9)
                find_car_location = zone + 1
                self.dk.update_keyinfos(find_car_location, [KeyInfo(key_type, [randint(0x0, 0xF) for i in range(16)],
                                                                    status)])
                if find_car_location not in KEY_MATCH_INFO:
                    res = 2
                else:
                    if status in KEY_MATCH_INFO[find_car_location]:
                        res = 3 
                    else:
                        res = 2
                self.partner.empty_all()
                logger.info(f"zone: {zone}, status: {status}, res: {res}")
                self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetFindKeyZone", {"zone": zone})
                self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "FindResults", {"results": [{"zone": zone, "result": 1}]})
                self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetFindKeyResult", {"zone": zone},
                                                      {"out": {"zone": zone, "result": 1}})
                self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "FindResults",
                                          {"results": [{"zone": zone, "result": res}]})
                # todo 性能问题，会导致批量跑时，这次get不到
                self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetFindKeyResult", {"zone": zone},
                                                      {"out": {"zone": zone, "result": res}})
                self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "FindResults", {"results": [{"zone": zone, "result": 0}]})
                self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetFindKeyResult", {"zone": zone},
                                                      {"out": {"zone": zone, "result": 0}})
                self.dk.ck_search_key_req(find_car_location, 6)

    @allure.title("GetIsConnectedZoneHasKey_所有区域无钥匙")
    @pytest.mark.full
    def test_caseid_105179(self):
        zone_status = {x: 0 for x in range(16)}
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetIsConnectedZoneHasKey", {}, {
            "out": [{"zone": key, "hasKey": False} for key, value in zone_status.items()]})

    @allure.title("GetIsConnectedZoneHasKey_单个钥匙_区域0-15遍历")
    @pytest.mark.sanity
    def test_caseid_105170(self):
        zone_status = {x: 0 for x in range(16)}
        for i in range(16):
            zone_status[i] = 1
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                          f'BLEKeyPrsntStsZone{i}', 1)
            if i > 0:
                zone_status[i - 1] = 0
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                              f'BLEKeyPrsntStsZone{i - 1}', 0)
            sleep(1)
            zones = [{"zone": key, "hasKey": True if value else False} for key, value in zone_status.items()]
            self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "ConnectedZones", {"zones": zones})
            self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetIsConnectedZoneHasKey", {}, {
                "out": zones})
            sleep(1)

    @allure.title("GetIsConnectedZoneHasKey_所有区域均有钥匙")
    @pytest.mark.full
    def test_caseid_105174(self):
        zone_status = {x: 1 for x in range(16)}
        for i in range(16):
            zone_status[i] = 1
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                          f'BLEKeyPrsntStsZone{i}', 1)
        sleep(1)
        zones = [{"zone": key, "hasKey": True if value else False} for key, value in zone_status.items()]
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "ConnectedZones", {"zones": zones})
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetIsConnectedZoneHasKey", {}, {"out": zones})

    @allure.title("GetIsConnectedZoneHasKey_所有区域均有钥匙_钥匙依次断开")
    @pytest.mark.smoke
    def test_caseid_105202(self):
        zone_status = {x: 1 for x in range(16)}
        for i in range(16):
            zone_status[i] = 1
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                          f'BLEKeyPrsntStsZone{i}', 1)
        sleep(1)
        zones = [{"zone": key, "hasKey": True if value else False} for key, value in zone_status.items()]
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "ConnectedZones", {"zones": zones})
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetIsConnectedZoneHasKey", {}, {"out": zones})
        for i in range(15, -1, -1):
            zone_status[i] = 0
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                          f'BLEKeyPrsntStsZone{i}', 0)
            sleep(1)
            zones = [{"zone": key, "hasKey": True if value else False} for key, value in zone_status.items()]
            self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "ConnectedZones", {"zones": zones})
            self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetIsConnectedZoneHasKey", {}, {
                "out": zones})
            sleep(1)

    @allure.title("单个配置SetConfigInfo_信号变化触发上报_下电记忆_休眠唤醒记忆_can信号映射")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_105191(self): 
        config_infos = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        config_all = {0: [0, 1, 2, 3], 1: [0, 1], 2: [0, 1], 3: [0, 1], 4: [0, 1], 5: [0, 1]}
        ApproachUnlockHmi_map = {1: 0, 0: 1}
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {
            "infos": [{"key": key, "value": value} for key, value in config_infos.items()]})
        sleep(1)

        for i in range(6):
            if i == 2:
                continue
            for value in config_all[i]:
                curr_config = {"key": i, "value": value}
                for _ in range(2):  # Set两次，第一次信号变化触发event，第二次无信号变化不会触发event
                    last_infos = copy.deepcopy(config_infos)
                    config_infos[i] = value
                    self.partner.empty_all()
                    self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [curr_config]})
                    logger.info(f"{last_infos}-->{config_infos}")
                    if last_infos == config_infos:
                        self.partner.ck_no_event(KEY_SERVICE_CLIENT, "ConfigInfo")
                    else:
                        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "ConfigInfo", {"infos": [curr_config]})
                    self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetConfigInfo", {},
                                                          {"out": [curr_config]})

                    self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr18, 'ApproachUnlockHmi',
                                    ApproachUnlockHmi_map[config_infos[1]], timeout=0.5)
                    self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr18, 'WalkAwayLockHmi', config_infos[0], timeout=0.5)
                sleep(2)
                self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT)  # 测试下电记忆
                sleep(5)
                self.partner.empty_all()
                self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetConfigInfo", {},
                                                      {"out": [curr_config]})

                self.bgm_sleep_and_awake()  # 测试休眠唤醒记忆
                self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetConfigInfo", {},
                                                      {"out": [curr_config]})

    @allure.title("SetConfigInfo_下行PDU数据验证")
    @pytest.mark.sanity
    def test_caseid_1987915(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        for value in range(2):              
            self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 3, "value": value},
                                                                                             {"key": 1, "value": value},
                                                                                             {"key": 5, "value": value},
                                                                                             {"key": 4, "value": value}]})
            sleep(1.5)
        for value in range(4):
            self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": value}]})
            sleep(1.5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('ApproachUnlockHmi', [1, 0]) # key=1
        self.bgm_eth_inter.ck_ordered_array('WalkAwayLockHmi', [0, 1, 2, 3]) # key=0
        self.bgm_eth_inter.ck_ordered_array('PEKeySearchZoneSet', [0, 1]) # key=5                         
        self.bgm_eth_inter.ck_ordered_array('ClsAutEna', [0, 1]) # key=4
        self.bgm_eth_inter.ck_ordered_array('DrvrDoorOpenWhenUnlockHmi', [1, 0]) # key=3
        
    @allure.title("全部配置SetConfigInfo_GetConfigInfo")
    @pytest.mark.sanity
    def test_caseid_105178(self):
        curr_config = [{"key": key, "value": 0} for key in range(6)]
        ApproachUnlockHmi_map = {1: 0, 0: 1}

        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": curr_config})
        sleep(1)
        self.partner.empty_all()

        for _ in range(30):
            last_config = curr_config
            curr_config = [{"key": 0, "value": randint(0, 3)},
                           {"key": 1, "value": randint(0, 1)},
                           {"key": 2, "value": randint(0, 1)},
                           {"key": 3, "value": randint(0, 1)},
                           {"key": 4, "value": randint(0, 1)},
                           {"key": 5, "value": randint(0, 1)}
                           ]

            self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": curr_config})
            if last_config == curr_config:
                self.partner.ck_no_event(KEY_SERVICE_CLIENT, "ConfigInfo")
            else:
                self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "ConfigInfo",
                                          {"infos": [config for config in curr_config if config not in last_config]})
            self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetConfigInfo", {},
                                                  {"out": curr_config})
            #存在通信丢帧问题，此处timeout需要大一点
            self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr18, 'ApproachUnlockHmi',
                            ApproachUnlockHmi_map[curr_config[1]["value"]], timeout=3)
            self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr18, 'WalkAwayLockHmi', curr_config[0]["value"], timeout=3)

    @allure.title("SetConfigInfo_AutoLockOnLeaveOff")
    @pytest.mark.sanity
    def test_caseid_105155(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 0}]})
        sleep(1)
        self.dk.set_cenlock_sts(0x1)
        sleep(1)
        self.dk.send_walk_away_lock_cmd()
        sleep(1)
        self.dk.ck_cenlock_sts(1)

    @allure.title("SetConfigInfo_OnWithoutAnyDoorClose")
    @pytest.mark.full
    def test_caseid_105184(self):
        # 当前mcu SWRS无该场景，故按Off处理 140AS 新合入该场景，见2.0SWRS
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 1}]})
        sleep(1)
        self.dk.set_cenlock_sts(0x1)
        sleep(1)
        self.dk.send_walk_away_lock_cmd()
        sleep(1)
        self.dk.ck_cenlock_sts(3)

    @allure.title("SetConfigInfo_OnWithDriverDoorClose_主驾门开")
    @pytest.mark.full
    def test_caseid_105157(self):
        #关闭诊断，防止诊断优先级高，门开无法切usagemode = 2
        self.sd_tester.quit_usage_mode()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 8) # SWSR：507156 防止不下发关门
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        sleep(1)
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenCloseStatus", {"doors": [0]},
                                                                                                  {"out": [{"id": 0, "isOpen": True}]})
        sleep(1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecMai',0)
        self.dk.send_walk_away_lock_cmd()
        self.dk.ck_door_opener_cmd(1, 2, timeout=6) # 离车闭锁5s后下发关
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_cenlock_sts(3, 9)

    @allure.title("SetConfigInfo_OnWithDriverDoorClose_副驾门开")
    @pytest.mark.full
    def test_caseid_105151(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        sleep(1)
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        sleep(1)
        self.dk.send_walk_away_lock_cmd()
        try:
            self.dk.ck_door_opener_cmd(2, 2, 1)
        except Exception:
            pass
        else:
            assert False, "不应该发送关副驾门信号"
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_cenlock_sts(1)

    @allure.title("SetConfigInfo_OnWithAllDoorClose_主驾门开")
    @pytest.mark.sanity
    def test_caseid_105154(self):
        #关闭诊断，防止诊断优先级高，门开无法切usagemode = 2
        self.sd_tester.quit_usage_mode()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 8) # SWSR：507156 防止不下发关门
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(1)
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        sleep(2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts',2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecMai',0)
        self.dk.send_walk_away_lock_cmd()
        self.dk.ck_door_opener_cmd(1, 2, 0, timeout=6) 
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_cenlock_sts(3)

    @allure.title("SetConfigInfo_AutoLockOnApproach_Off")
    @pytest.mark.full
    def test_caseid_105197(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 1, "value": 0}]})
        sleep(1)
        self.dk.set_cenlock_sts(0x3)
        sleep(2)
        self.dk.send_approach_unlock_cmd()
        sleep(1)
        self.dk.ck_cenlock_sts(1, 9)

    @allure.title("SetConfigInfo_AutoLockOnApproach_On")
    @pytest.mark.smoke
    def test_caseid_105163(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 1, "value": 1}]})
        sleep(1)
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        self.dk.send_approach_unlock_cmd()
        sleep(1)
        self.dk.ck_cenlock_sts(1, 9)

    @allure.title("SetConfigInfo_DoorAutoOpenOnUnlock_Off")
    @pytest.mark.full
    def test_caseid_105182(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 3, "value": 0}]})
        sleep(1)
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        self.dk.send_approach_unlock_cmd()
        sleep(1)
        self.dk.ck_cenlock_sts(1, 9)

        sleep(1)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEKeyPrsntStsZone7', 'Validity_Valid')
        try:
            self.dk.ck_door_opener_cmd(1, 1, timeout=3)
        except Exception:
            pass
        else:
            assert False, "不应该发送主驾开门"

    @allure.title("SetConfigInfo_DoorAutoOpenOnUnlock_On")
    @pytest.mark.sanity
    def test_caseid_105161(self):
        self.sd_tester.change_usage_mode(0)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 3, "value": 1}]})
        sleep(1)
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        self.dk.send_approach_unlock_cmd() # 140AS新增解锁后800ms计时器策略 见SOA-21415 
        self.dk.ck_cenlock_sts(1, 9, timeout=2)
        self.dk.ck_door_opener_cmd(1, 4, 1)
        # 800ms内，zone7有钥匙，则下发关门；800ms外，硬线门开&zone7有钥匙，则下发关门
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        sleep(2)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEKeyPrsntStsZone7', 'Validity_Valid')
        self.dk.ck_door_opener_cmd(1, 1, 1)

    @allure.title("SetConfigInfo_WindowAutoCloseOnLock_Off")
    @pytest.mark.full
    def test_caseid_105160(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 4, "value": 0}]})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_window_position(0x1A, 0x1A, 0x1A, 0x1A)
        sleep(1)
        self.dk.send_nfc_cmd()
        try:
            self.dk.ck_window_opener_req(0x1, 0x1, 0x1, 0x1, 3)
        except Exception:
            pass
        else:
            assert False, "配置关闭，锁车不应关窗"
        sleep(1)
        self.dk.ck_cenlock_sts(3)
        self.dk.set_digital_key_connect_info()

    @allure.title("SetConfigInfo_WindowAutoCloseOnLock_On")
    @pytest.mark.sanity
    def test_caseid_105189(self): # WinGlbCmd1 信号触发不稳定 SWRS：461783
        # self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 4, "value": 1}]})
        # sleep(0.5) 
        # self.sd_tester.change_usage_mode(2)
        # self.dk.set_cenlock_sts(0x1)
        # self.dk.set_window_position(0x1A, 0x1A, 0x1A, 0x1A)
        # sleep(1)
        # self.sd_tester.change_usage_mode(1)
        # self.dk.send_walk_away_lock_cmd()
        # self.dk.ck_window_opener_req(0x1, 0x1, 0x1, 0x1, 3)
        # sleep(1)
        # self.dk.ck_cenlock_sts(3)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 4, "value": 1}]})
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()        
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("ClsAutEna", [1])
        self.bgm_eth_inter.ck_period_time("ClsAutEna", 1)

        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 4, "value": 0}]})
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()        
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("ClsAutEna", [0])
        self.bgm_eth_inter.ck_period_time("ClsAutEna", 1)

    @allure.title("SetConfigInfo_SetPEKeySearchDedicateZone_Off")
    @pytest.mark.full
    def test_caseid_1983608(self): # V140
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 5, "value": 0}]})
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(1, 0.5)
        self.dk.ck_search_key_req(1, 2)
        
    @allure.title("SetConfigInfo_SetPEKeySearchDedicateZone_On")
    @pytest.mark.sanity
    def test_caseid_1983609(self):
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 5, "value": 1}]})
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        self.dk.empty_dk_data_queue()
        self.dk.press_door_outswitch(1, 0.5)
        self.dk.ck_search_key_req(1, 2)
        self.dk.press_door_outswitch(2, 0.5)
        self.dk.ck_search_key_req(1, 2)
        self.dk.press_door_outswitch(3, 0.5)
        self.dk.ck_search_key_req(1, 2)
        self.dk.press_door_outswitch(4, 0.5)
        self.dk.ck_search_key_req(1, 2)

    @allure.title("GetDigitalKeyConnectedStatus_上电通信故障")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_105168(self):
        self.ipdu.pause_all_bus_send()
        self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT)
        try:
            self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {},
                                                  {"out": [{"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                            "type": 0, "isConnected": False, "zone": 0,
                                                            "battWarnSts": False},
                                                           {"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                            "type": 0, "isConnected": False, "zone": 0,
                                                            "battWarnSts": False},
                                                           {"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                            "type": 0, "isConnected": False, "zone": 0,
                                                            "battWarnSts": False},
                                                           {"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                            "type": 0, "isConnected": False, "zone": 0,
                                                            "battWarnSts": False}]})
        except Exception as e:
            self.ipdu.resume_all_bus_send()
            assert False, e
        else:
            self.ipdu.resume_all_bus_send()

    @allure.title("GetDigitalKeyConnectedStatus_信号遍历")
    @pytest.mark.sanity
    def test_caseid_105185(self):
        curr_status = [{"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        "type": 0, "isConnected": False, "zone": 0,
                        "battWarnSts": False},
                       {"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        "type": 0, "isConnected": False, "zone": 0,
                        "battWarnSts": False},
                       {"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        "type": 0, "isConnected": False, "zone": 0,
                        "battWarnSts": False},
                       {"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        "type": 0, "isConnected": False, "zone": 0,
                        "battWarnSts": False}]
        keyids = [key_id1, key_id2, key_id3, key_id4]
        pdu_map = {0: self.ipdu.connectivitycanfd.BncmConnectivityFr18,
                   1: self.ipdu.connectivitycanfd.BncmConnectivityFr18,
                   2: self.ipdu.connectivitycanfd.BncmConnectivityFr19,
                   3: self.ipdu.connectivitycanfd.BncmConnectivityFr19}

        for i in range(4):
            key_id = keyids[i]
            for j in range(16):
                self.ipdu.set(pdu_map[i], f'DigKeyConnectInfo{i + 1}KeyIdByte{j}', key_id[j])
            curr_status[i]["keyId"] = key_id
            self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyConnectedStatus", {"status": curr_status})
            self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {},
                                                  {"out": curr_status})

            for isConnected in [1, 0]:
                curr_status[i]["isConnected"] = True if isConnected else False
                self.ipdu.set(pdu_map[i], f'DigKeyConnectInfo{i + 1}KeyConnectSts', isConnected)
                self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyConnectedStatus", {"status": curr_status})
                self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {},
                                                      {"out": curr_status})

            for zone in range(1, 16):
                curr_status[i]["zone"] = zone
                self.ipdu.set(pdu_map[i], f'DigKeyConnectInfo{i + 1}KeyPrsntZone', zone)
                self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyConnectedStatus", {"status": curr_status})
                self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {},
                                                      {"out": curr_status})

            for key_type in range(1, 10):
                curr_status[i]["type"] = key_type
                self.ipdu.set(pdu_map[i], f'DigKeyConnectInfo{i + 1}KeyTyp', key_type)
                self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyConnectedStatus", {"status": curr_status})
                self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {},
                                                      {"out": curr_status})

            for battWarnSts in [1, 0]:
                curr_status[i]["battWarnSts"] = True if battWarnSts else False
                self.ipdu.set(pdu_map[i], f'DigKeyConnectInfo{i + 1}BattWarn', battWarnSts)
                self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyConnectedStatus", {"status": curr_status})
                self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {},
                                                      {"out": curr_status})

    # @allure.title("GetDigitalKeyDataUp_DigitalKeyDataUp_RKE闭锁")
    # @pytest.mark.smoke
    # def test_caseid_105186(self): # 200AC删除
    #     execid = str(uuid.uuid1()).replace("-", "")
    #     self.dk.send_rke_lock(exec_id=execid)
    #     real_cmd = RealtimeCmdReq()
    #     real_cmd.execId = execid
    #     real_cmd.vid = f'{1:032}'
    #     real_cmd.vehicleModel = 61
    #     real_cmd.cmdCode = 1
    #     real_cmd.timestamp = 1000000012345678

    #     cd = CmdDetail()
    #     lc = LockControl()
    #     lc.op = 2
    #     lc.keyId = f'{1:032}'
    #     lc.userId = ''
    #     cd.lock_control.MergeFrom(lc)
    #     real_cmd.cmdDetail.MergeFrom(cd)
    #     ble_payload = real_cmd.SerializeToString().hex()
    #     ck_data = DataTypeHanding.hexstr_to_inlist(f'21{1 + len(ble_payload) // 2:04X}{1:02X}{ble_payload}')
    #     self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyDataUp", {"data": ck_data}, fuzz_match=False)  # case写死
    #     self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyDataUp", {}, {"out": ck_data})
    #     self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
    #     self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("KeyWhiteListVersion_GetKeyWhiteListVersion")
    @pytest.mark.sanity
    def test_caseid_105194(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', 0x0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', 0x0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', 0x1)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', 0x1)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "KeyWhiteListVersion",
                                  {"ver": [{'type': 0, 'version': 1}, {'type': 1, 'version': 1}]})
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetKeyWhiteListVersion", {"type": 0},
                                              {"out": [{'type': 0, 'version': 1}]})
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetKeyWhiteListVersion", {"type": 1},
                                              {"out": [{'type': 1, 'version': 1}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', 0xFFFFFFFFFFFFFFFF)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "KeyWhiteListVersion",
                                  {"ver": [{'type': 1, 'version': 0xFFFFFFFFFFFFFFFF}]})
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetKeyWhiteListVersion", {"type": 0},
                                              {"out": [{'type': 0, 'version': 1}]})
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetKeyWhiteListVersion", {"type": 1},
                                              {"out": [{'type': 1, 'version': 0xFFFFFFFFFFFFFFFF}]})

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', 0xFFFFFFFF)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', 0x2)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "KeyWhiteListVersion",
                                  {"ver": [{'type': 0, 'version': 0xFFFFFFFF}, {'type': 1, 'version': 2}]})
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetKeyWhiteListVersion", {"type": 0},
                                              {"out": [{'type': 0, 'version': 0xFFFFFFFF}]})
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetKeyWhiteListVersion", {"type": 1},
                                              {"out": [{'type': 1, 'version': 2}]})

    @allure.title("GetKeyWhiteListVersion_服务启动默认值")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_105150(self):
        self.ipdu.pause_all_bus_send()
        self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT, resume_all_bus=False)
        try:
            self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetKeyWhiteListVersion", {"type": 0},
                                                  {"out": [{'type': 0, 'version': 0}]})
            self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetKeyWhiteListVersion", {"type": 1},
                                                  {"out": [{'type': 1, 'version': 0}]})
        except Exception:
            self.ipdu.resume_all_bus_send()
            assert False, "默认值异常"
        else:
            self.ipdu.resume_all_bus_send()

    @allure.title("GetDigitalKeyConnectedStatus_通信故障")
    @pytest.mark.sanity
    def test_caseid_105175(self):
        self.dk.set_digital_key_connect_info(connect_sts1=1)
        sleep(5)
        self.ipdu.resume_all_bus_send()
        sleep(2)
        try:
            self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {},
                                                  {"out": [{"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                            "type": 0, "isConnected": False, "zone": 0,
                                                            "battWarnSts": False},
                                                           {"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                            "type": 0, "isConnected": False, "zone": 0,
                                                            "battWarnSts": False},
                                                           {"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                            "type": 0, "isConnected": False, "zone": 0,
                                                            "battWarnSts": False},
                                                           {"keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                            "type": 0, "isConnected": False, "zone": 0,
                                                            "battWarnSts": False}]})
        except Exception as e:
            self.ipdu.resume_all_bus_send()
            assert False, e
        else:
            self.ipdu.resume_all_bus_send()

    @allure.title("SetConfigInfo_下行PDU周期验证")
    @pytest.mark.sanity
    def test_caseid_1912577(self): 
        self.bgm_eth_inter.start_bgm_tcpdump()         
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {'infos': [{"key": 0, "value": 3},
                                                                                         {"key": 1, "value": 0},
                                                                                         {"key": 3, "value": 1},
                                                                                         {"key": 4, "value": 1},
                                                                                         {"key": 5, "value": 0}]})  
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time('WalkAwayLockHmi', 1)
        self.bgm_eth_inter.ck_period_time('ApproachUnlockHmi', 1)
        self.bgm_eth_inter.ck_period_time('DrvrDoorOpenWhenUnlockHmi', 1)
        self.bgm_eth_inter.ck_period_time('ClsAutEna', 1)
        self.bgm_eth_inter.ck_period_time('PEKeySearchZoneSet', 1)                      
        
    @allure.title("SetDigitalKeyUnlockEvent增加时间戳机制")
    @pytest.mark.full
    def test_caseid_1913648(self):
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)           
        seqId=[0,1,2]
        seqId[0]=self.partner.send_request_and_return_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {})["out"][0]["seqId"]
        for i in range(1,3):
            digital_key_info = {"type": randint(1,10),
                                "trigger": 1,
                                "keyId": [randint(0x0, 0xF) for i in range(16)]}   
            self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetDigitalKeyUnlockEvent", {'info': digital_key_info})
            self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId", {"info": digital_key_info})
            seqId[i]=self.partner.send_request_and_return_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {})["out"][0]["seqId"]   
            if seqId[i] != seqId[i-1]:   
                pass
            else:
                assert False, f"时间戳有误"   

    @allure.title("设置寻车请求_下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_1943233(self):
        file_path, save_name = self.bgm_tcpdump.start_bgm_tcpdump() 
        for i in range(4):
            self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": i})
            sleep(3)
        data_list=[(6361,1,1,2)]
        res_dict = self.stop_tcpdump_and_copy_and_calculate(save_name, data_list)
        logger.info(f"打印当前值： res_dict={res_dict}")
        for key in data_list:
            assert len(res_dict[key]) == 4
            for index, data in enumerate(res_dict[key]):
                logger.info(f"打印当前值： data={data} {res_dict[data_list[0]].index(data)} ")
                assert data[1] == index
                
    @allure.title("远程寻车功能执行状态_无总线数据输入默认值")
    @pytest.mark.full
    def test_caseid_1943236(self): 
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 1})
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr05, 'CarLoctrActvnSts', 1)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, 'GetCarLocalTraceActiveStatus', {}, {"out": 1})
        self.ipdu.pause_all_bus_send()
        self.bgm_power_off_and_on()
        self.partner.wait_for_service_reconnect(KEY_SERVICE_CLIENT)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "NotifyCarLocalTraceActiveStatus", {"sts": 0})
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, 'GetCarLocalTraceActiveStatus', {}, {"out": 0})
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr05, 'CarLoctrActvnSts', 0)
 
    @allure.title("SetFindKeyZone寻钥匙请求_下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_1943237(self):
        def return_info(value):
            return value+1 if value != 10 else 0

        self.bgm_eth_inter.start_bgm_tcpdump()
        for i in range(11):
            self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetFindKeyZone", {"zone": i})
            sleep(3)
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'KeyReadReqFromSrv', return_info(i), timeout=0.5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("KeyReadReqFromSrv",[1,2,3,4,5,6,7,8,9,10,0])

    @allure.title("BGM首次下线默认配置")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_105169(self):
        # 删除数据库
        bgmssh = BGM_SSH()
        bgmssh.type_commands("sudo rm -rf /data/s2s_service/s2s_service.db3", root_permission=True)
        sleep(1)
        bgmssh.type_commands("ls -l /data/s2s_service")
        sleep(5)
        self.ipdu.pause_all_bus_send()  # 停掉总线
        self.nucapp.bgm_power_off()
        self.partner.empty_all(7)
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(KEY_SERVICE_CLIENT)   
        curr_config=[{"key": 0, "value": 0},
                     {"key": 1, "value": 0}, 
                     {"key": 3, "value": 0}, 
                     {"key": 4, "value": 0},
                     {"key": 5, "value": 0}]
        # GetConfigInfo_未配置时默认值
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetConfigInfo", {}, {"out": curr_config})
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "ConfigInfo", {"infos": curr_config})   
        self.partner.empty_all(2)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo",  {'infos': curr_config})     
        # 通知配置信息
        self.partner.ck_no_event(KEY_SERVICE_CLIENT, "ConfigInfo")  
        self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT)
        # 通知配置信息
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "ConfigInfo", {"infos": curr_config})   

    @allure.title("启动场景event")
    @pytest.mark.full
    def test_caseid_1984754(self):
        self.dk.set_cenlock_sts(3)
        sleep(2)
        self.dk.send_nfc_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId",
                                  {'info': {"keyId": key_id1,
                                            "trigger": 3,
                                            "type": 1}})  
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetFindKeyZone", {"zone": 10})  
        curr_config=[{"key": 0, "value": 1},
                     {"key": 1, "value": 0}, 
                     {"key": 3, "value": 1}, 
                     {"key": 4, "value": 0},
                     {"key": 5, "value": 1}]
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo",  {'infos': curr_config})        
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetConfigInfo", {}, {"out": curr_config})
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', 0x0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', 0x0)
        zone_status = {x: 0 for x in range(16)}
        for i in range(16):
            zone_status[i] = 1
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, f'BLEKeyPrsntStsZone{i}', 0)
        self.partner.empty_all(10)
        self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT)
        # 通知远程寻车功能执行状态 
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "NotifyCarLocalTraceActiveStatus", {"sts": 0})
        # 通知数字钥匙触发事件信息 0为无效值 不上报
        digital_key_info = {"type": 0, "trigger": 0, "keyId": key_id0}
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {}, {"out": [digital_key_info]})
        self.partner.ck_no_event(KEY_SERVICE_CLIENT, "DigitalKeyId")  
        # 通知寻钥匙结果
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "FindResults", {"results": [{"zone": 10, "result": 0}]})
        # # 通知数字钥匙应用处理数据能力状态  200AC删除
        # self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "NotifyDigitalKeyServiceStatus", {"isEnable": True})
        # 通知区域钥匙状态
        zone_status = {x: 0 for x in range(16)}
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetIsConnectedZoneHasKey", {}, {
            "out": [{"zone": key, "hasKey": False} for key, value in zone_status.items()]})
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "ConnectedZones", 
                                  {"zones": [{"zone": key, "hasKey": False} for key, value in zone_status.items()]})
        # 通知配置信息
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "ConfigInfo", {"infos": curr_config})
        # 通知数字钥匙连接信息
        curr_status = [{"keyId": key_id0,
                        "type": 0, "isConnected": False, "zone": 0,
                        "battWarnSts": False}]
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {},
                                                  {"out": curr_status})
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyConnectedStatus", {"status": curr_status})
        # 通知钥匙白名单版本号
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "KeyWhiteListVersion",
                                  {"ver": [{'type': 0, 'version': 0}, {'type': 1, 'version': 0}]}) 
        
    @allure.title("启动场景_通知钥匙白名单版本号_默认值")
    @pytest.mark.full
    def test_caseid_1988706(self): 
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', 0x0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', 0x0)
        self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "KeyWhiteListVersion",
                                  {"ver": [{'type': 0, 'version': 0}, {'type': 1, 'version': 0}]})
        
    @allure.title("启动场景_通知钥匙白名单版本号_默认值")
    @pytest.mark.full
    def test_caseid_1988707(self): 
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', 0x1)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', 0x1)
        self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "KeyWhiteListVersion",
                                  {"ver": [{'type': 0, 'version': 1}, {'type': 1, 'version': 1}]})
        
        
@allure.feature("SOA服务接口")
@allure.story("整车控制/KeyService")
@pytest.mark.lg                          
class TestKeyServiceMockMCU(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("KeyService", "client")])

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)        
        
    @allure.title("启动场景_通知远程寻车功能执行状态_默认值")
    @pytest.mark.full
    def test_caseid_1988702(self): 
       self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr05, 'CarLoctrActvnSts', 0) 
       self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT)
       self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "NotifyCarLocalTraceActiveStatus", {"sts": 0}, timeout = 10)
    
    @allure.title("启动场景_通知远程寻车功能执行状态_非默认值")
    @pytest.mark.full
    def test_caseid_1988703(self): 
       self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr05, 'CarLoctrActvnSts', 1) 
       self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT)
       self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "NotifyCarLocalTraceActiveStatus", {"sts": 1}, timeout = 10)
       
    @allure.title("启动场景_通知数字钥匙连接信息_默认值")
    @pytest.mark.full
    def test_caseid_1988704(self):
        key_id0 = "0000000000000000" 
        curr_status = [{"keyId": key_id0,
                        "type": 0, "isConnected": False, "zone": 0,
                        "battWarnSts": False}]
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1KeyConnectSts', 0)
        zone_status = {x: 0 for x in range(16)}
        for i in range(16):
            zone_status[i] = 1
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, f'DigKeyConnectInfo1KeyIdByte{i}', 0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1KeyPrsntZone', 0)  
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1KeyTyp', 0) 
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1BattWarn', 0)   
            
        self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyConnectedStatus", {"status": curr_status}, timeout = 10)
        
    @allure.title("启动场景_通知数字钥匙连接信息_默认值")
    @pytest.mark.full
    def test_caseid_1988705(self):
        key_id0 = "1111111111111111" 
        curr_status = [{"keyId": key_id0,
                        "type": 1, "isConnected": True, "zone": 1,
                        "battWarnSts": True}]
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1KeyConnectSts', 1)
        zone_status = {x: 0 for x in range(16)}
        for i in range(16):
            zone_status[i] = 1
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, f'DigKeyConnectInfo1KeyIdByte{i}', 1)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1KeyPrsntZone', 1)  
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1KeyTyp', 1) 
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1BattWarn', 1)   
            
        self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyConnectedStatus", {"status": curr_status}, timeout = 10)
        
    @allure.title("获取&通知数字钥匙无感请求信息_信号遍历")
    @pytest.mark.sanity
    def test_caseid_1989231(self):    
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdDevFr01, 'DigKeyApproachReqDigKeyApproaReq', 2)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyApproachRequestInfo", {}, {"out": {"approachRequestSts": 2}}, timeout = 5)
        last_value=2
        self.partner.empty_all(2)
        for req in range(8):
            self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdDevFr01, 'DigKeyApproachReqDigKeyApproaReq', req)
            value = req if req in [0, 2, 3] else last_value
            if value != last_value:
                self.partner.ck_event_and_resp(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": value}}, timeout = 5)
            else:
                self.partner.ck_no_event_and_ck_resp(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo", {"out": {"approachRequestSts": value}}, timeout = 3)   
            last_value = value
    
    @allure.title("获取&通知数字钥匙无感请求信息_启动默认值")
    @pytest.mark.full
    def test_caseid_1989232(self):    
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdDevFr01, 'DigKeyApproachReqDigKeyApproaReq', 2)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyApproachRequestInfo", {}, {"out": {"approachRequestSts": 2}}, timeout = 5)
        self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        sleep(10)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyApproachRequestInfo", {}, {"out": {"approachRequestSts": 255}}, timeout = 5)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_event_and_resp(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 2}}, timeout = 5)