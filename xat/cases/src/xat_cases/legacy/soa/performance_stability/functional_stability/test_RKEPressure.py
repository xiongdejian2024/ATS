import allure
import pytest
from time import sleep
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


@allure.feature("性能稳定性")
@allure.story("业务稳定性/启动场景压测--蓝牙控制")
@pytest.mark.soa
class TestRKEPressure(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("CentralLockService", "client"),
                                     ("KeyService", "client")
                                     ])
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
        self.partner.empty_all()

    def after_each_func(self, ecu):
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待10s让环境恢复")
            sleep(10)
        else:
            sleep(3)
        super().after_each_func(ecu, start=False)

    Times=50
    @pytest.mark.repeat(Times)
    @allure.title("重启后RKE解锁成功")
    @pytest.mark.sanity
    def test_caseid_1984243(self):
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all(5)
        self.ipdu.pause_all_bus_send()
        self.bgm_power_off_and_on() # 无需等待服务连接
        self.ipdu.resume_all_bus_send() 
        self.partner.empty_all(1) # 待MCU起来
        self.dk.send_rke_unlock()
        info1 = {"sts": 1, "triggerId": 1, "updateEve": True}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info1}, timeout=6.1) # 重启到服务可用
        info2 = {"sts": 1, "triggerId": 1, "updateEve": False}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info2})



    # @allure.title("重启后RKE车窗控制失败")
    # @pytest.mark.repeat(Times)
    # @pytest.mark.full
    # def test_caseid_dhy2(self): # remoteCtrl
    #     self.dk.send_rke_window_control(0, 0, 0, 0) # 等一次控制结束 新增逻辑：相同报文只响应第一次
    #     sleep(15)
    #     self.dk.empty_dk_data_queue()        
    #     self.dk.set_window_position(0x1A, 0x1A, 0x1A, 0x1A) # 1A=26 是100%开度，不会下降1.5cm
    #     self.dk.send_rke_window_control(0x14, 0x14, 0x14, 0x14)
    #     self.dk.ck_window_opener_req(0x6, 0x6, 0x6, 0x6)
    #     self.dk.ck_rke_resp(2, 0, "PreConditionOK", exec_type=2)
    #     sleep(7)
    #     self.dk.ck_rke_resp(2, 1, "DelayFail", exec_type=3)
        
    # @allure.title("重启后RKE车窗控制成功")
    # @pytest.mark.repeat(Times)
    # @pytest.mark.full
    # def test_caseid_dhy3(self): # remoteCtrl
    #     self.dk.send_rke_window_control(0x1A, 0x1A, 0x1A, 0x1A) # 等一次控制结束 新增逻辑：相同报文只响应第一次
    #     sleep(15)
    #     self.dk.empty_dk_data_queue()  
    #     self.dk.set_window_position(0x1A, 0x1A, 0x1A, 0x1A) # 1A=26 是100%开度，不会下降1.5cm
        
        
    #     self.dk.send_rke_window_control(0, 0, 0, 0)
    #     self.dk.ck_window_opener_req(0x1, 0x1, 0x1, 0x1)
    #     self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
    #     self.dk.ck_rke_resp(2, 0, "PreConditionOK", exec_type=2)
    #     self.dk.ck_rke_resp(2, 0, "Success", exec_type=3, timeout=8)
        
    # @allure.title("重启后RKE车窗控制成功")
    # @pytest.mark.repeat(Times)
    # @pytest.mark.full
    # def test_caseid_dhy3(self): # remoteCtrl
    #     self.dk.send_rke_window_control(0x1A, 0x1A, 0x1A, 0x1A) # 等一次控制结束 新增逻辑：相同报文只响应第一次
    #     sleep(15)
    #     self.dk.empty_dk_data_queue()  
    #     self.dk.set_window_position(0x1A, 0x1A, 0x1A, 0x1A) # 1A=26 是100%开度，不会下降1.5cm
        
    #     sleep(5)     
    #     self.ipdu.pause_all_bus_send()
    #     self.bgm_power_off_and_on() 
    #     self.ipdu.resume_all_bus_send()
    #     self.partner.empty_all(1) 
    #     # self.partner.wait_for_service_reconnect(KeyService_client)
    #     self.dk.send_rke_window_control(0, 0, 0, 0)
    #     self.dk.ck_window_opener_req(0x1, 0x1, 0x1, 0x1)
    #     self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
    #     self.dk.ck_rke_resp(2, 0, "PreConditionOK", exec_type=2)
    #     self.dk.ck_rke_resp(2, 0, "Success", exec_type=3, timeout=8)