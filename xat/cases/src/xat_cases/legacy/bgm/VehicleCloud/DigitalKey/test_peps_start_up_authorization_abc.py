#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_peps_walk_away_abc.py
@Time         :2024/03/28 11:50:00
@Author       :hui.zhao@jiduauto.com
@Description  :数字钥匙NFC相关功能
"""
import copy
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *
from xat_ecu.api.abc_interface import *

handle_ti = 0.5  # PE按下后寻钥匙

@allure.feature("互联服务")
@allure.story("数字钥匙和账号/PEPS/离车侧门尾门自动关闭落锁")
class TestDigitalKeyStartUp(TestDigitalKeyBase):
    def before_each_func(self, ecu):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.bus_comm.set_dtc_pre()
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        pass

    def after_each_func(self, ecu):
        self.soa.set_hv_off_sts(is_off=False)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.set_strt_msg_to_mod_mngt(StrtMsgToModMngt=StrtMsgToModMngt.NoInhb)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.trigger_gear_by_auto(gear_status=False)
        self.bus_comm.trigger_gear_by_manual(gear_status=False)
        self.bus_comm.trigger_gear_by_cdc(gear_status=False)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        self.io.hazard_light_close()
        self.io.bgm_diag_line_up()
        pass
    """
    自动化不稳定
    """
    # @allure.title("启动授权_原KeyPresent=0_找到NFC钥匙_授权成功")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112278?projectId=46')
    # @pytest.mark.smoke
    # def test_caseid_112278(self): 
    #     self.mix.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
    #     self.io.set_door(Drvr=Door.open)
    #     self.bus_comm.set_door_lock_sts(drv_lock=Locksts.Unlckd)
    #     sleep(2)
    #     self.io.set_door(Drvr=Door.close)
    #     self.io.brake_light_close()
    #     sleep(2)
    #     pre_sts = self.bus_comm.get_key_nfc_vmm_prsnt()  
    #     if pre_sts == 1 or pre_sts == 3:
    #         logger.info("NFC钥匙已授权,等待120秒使钥匙失效")
    #         sleep(125)
    #         self.bus_comm.get_key_nfc_vmm_prsnt()
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.NFC_Card, key_id1, 8)])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     self.mix.set_PtActvnReq(up_type=UpType.SetUsageModeUp)
    #     self.bus_comm.dk.ck_search_key_req(1, 1)
    #     self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
    #     self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)



    # @allure.title("启动授权_原KeyPresent=1(BLE)_授权成功")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112256?projectId=46')
    # @pytest.mark.smoke
    # def test_caseid_112256(self):
    #     sleep(125)
    #     self.mix.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
    #     self.io.set_door(Drvr=Door.open)
    #     self.bus_comm.set_door_lock_sts(drv_lock=Locksts.Unlckd)
    #     sleep(2)
    #     self.io.set_door(Drvr=Door.close)
    #     self.io.brake_light_close()
    #     sleep(2)
    #     pre_sts = self.bus_comm.get_key_nfc_vmm_prsnt()  
    #     if pre_sts == 1 or pre_sts == 3:
    #         logger.info("NFC钥匙已授权,等待120秒使钥匙失效")
    #         sleep(125)
    #         self.bus_comm.get_key_nfc_vmm_prsnt()
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 8)])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     self.mix.set_PtActvnReq(up_type=UpType.SetUsageModeUp)
    #     self.bus_comm.dk.ck_search_key_req(1, 1)
    #     self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
    #     self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)

    
    # @allure.title("启动授权_原KeyPresent=0_未找到钥匙_授权失败")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112211?projectId=46')
    # @pytest.mark.full
    # def test_caseid_112211(self):
    #     sleep(125)
    #     self.mix.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
    #     self.io.set_door(Drvr=Door.open)
    #     self.bus_comm.set_door_lock_sts(drv_lock=Locksts.Unlckd)
    #     sleep(2)
    #     self.io.set_door(Drvr=Door.close)
    #     self.io.brake_light_close()
    #     sleep(2)
    #     pre_sts = self.bus_comm.get_key_nfc_vmm_prsnt()  
    #     if pre_sts == 1 or pre_sts == 3:
    #         logger.info("NFC钥匙已授权,等待120秒使钥匙失效")
    #         sleep(125)
    #         self.bus_comm.get_key_nfc_vmm_prsnt()
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     self.mix.set_PtActvnReq(up_type=UpType.SetUsageModeUp)
    #     self.bus_comm.dk.ck_search_key_req(1, 1)
    #     # self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
    #     self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)


    
    # @allure.title("启动授权_原KeyPresent=0_寻钥匙结果(0x1)与目标区域(0x6)不匹配_授权失败")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112249?projectId=46')
    # @pytest.mark.full1
    # def test_caseid_112249(self):
    #     self.mix.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
    #     self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)
    #     self.bus_comm.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 1)])
    #     self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
    #     time.sleep(6)
    #     self.io.bgm_diag_line_down()
    #     time.sleep(10)
    #     self.bus_comm.dk.ck_search_key_req(6, 1)
    #     self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)