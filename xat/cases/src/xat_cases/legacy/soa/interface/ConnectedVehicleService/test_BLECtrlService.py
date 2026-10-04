import allure
import pytest
import uuid
from time import sleep
from xat_ecu.legacy.common.data_type_handing import logger, DataTypeHanding
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.digital_key.RVCTSPMessage_pb2 import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *


@allure.feature("SOA服务接口")
@allure.story("互联服务/BLECtrlService")
@pytest.mark.aqx
class TestBLECtrlService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu, enable_inter_service=True)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("RKECtrlService", "client")])
        
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
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0) 
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.partner.empty_all(10)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)    
        
    # @allure.title("通知数字钥匙处理数据能力的状态_诊断重启")
    # @pytest.mark.smoke
    # @pytest.mark.restart
    # def test_caseid_dhy1(self): # SOA-21923
    #     logger.info("重启前--------------------------------------")
    #     sleep(10)
    #     # self.partner.ck_s2s_event("BLECtrlService_client", "DigitalKeyServiceSts", {"state": True})    
    #     self.sd_tester.reset_ecu() # 我们接口默认 1001 BGM的ECU 
    #     logger.info("重启后--------------------------------------")
    #     # sleep(10)
    #     # self.partner.ck_s2s_event("BLECtrlService_client", "DigitalKeyServiceSts", {"state": True}) 
    #     self.partner.ck_s2s_event("BLECtrlService_client", "DigitalKeyServiceSts", {"state": False})         
        
    @allure.title("设置数字钥匙RKE的请求指令信息_RKE不具有处理数据能力时返回False")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1984733(self):
        self.bgm_power_off_and_on(timeout=3)
        self.partner.wait_for_service_reconnect(RKECTRL_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(RKECTRL_SERVICE_CLIENT, "SetDigitalKeyDataUp", {"data": [1,1,11]}, {"out": 1})  
        self.partner.ck_s2s_event(RKECTRL_SERVICE_CLIENT, "DigitalKeyServiceSts", {"state": True}, timeout=20)  # 冷启动，时间往后延    
        self.partner.send_request_and_ck_resp(RKECTRL_SERVICE_CLIENT, "SetDigitalKeyDataUp", {"data": [1,1,11]}, {"out": 0})  
          
    @allure.title("设置数字钥匙RKE的请求指令信息_RKE闭锁")
    @pytest.mark.smoke
    def test_caseid_1984732(self): 
        execid = str(uuid.uuid1()).replace("-", "")
        self.dk.send_rke_lock(exec_id=execid)
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = execid
        real_cmd.vid = f'{1:032}'
        real_cmd.vehicleModel = 61
        real_cmd.cmdCode = 1
        real_cmd.timestamp = 1000000012345678

        cd = CmdDetail()
        lc = LockControl()
        lc.op = 2
        lc.keyId = f'{1:032}'
        lc.userId = ''
        cd.lock_control.MergeFrom(lc)
        real_cmd.cmdDetail.MergeFrom(cd)
        ble_payload = real_cmd.SerializeToString().hex()
        ck_data = DataTypeHanding.hexstr_to_inlist(f'21{1 + len(ble_payload) // 2:04X}{1:02X}{ble_payload}')
        self.partner.send_method_request(RKECTRL_SERVICE_CLIENT, 'SetDigitalKeyDataUp', {"data": ck_data})
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)           
        
    @allure.title("通知数字钥匙处理数据能力的状态_kill RKE进程")
    @pytest.mark.sanity
    def test_caseid_1984736(self):        
        self.kill_bgm_process("rke")
        self.partner.wait_for_service_reconnect(RKECTRL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(RKECTRL_SERVICE_CLIENT, "DigitalKeyServiceSts", {"state": True})  
       
    @allure.title("数字钥匙提示信息接口")
    @pytest.mark.sanity
    def test_caseid_1987929(self):        
        self.sd_tester.change_usage_mode(2)
        self.set_nopeople_incar()
        self.dk.send_rke_apa_close_door()
       
        self.partner.ck_s2s_event(RKECTRL_SERVICE_CLIENT, "DigitalKeyReminderInfo", {"info":{"closeDoorOutsideReminder":True}})
        self.partner.ck_s2s_event(RKECTRL_SERVICE_CLIENT, "DigitalKeyReminderInfo", {"info":{"closeDoorOutsideReminder":False}}) 
        self.partner.send_request_and_ck_resp(RKECTRL_SERVICE_CLIENT, "GetDigitalKeyReminderInfo",
                                                {},{"out": {"closeDoorOutsideReminder":False}})