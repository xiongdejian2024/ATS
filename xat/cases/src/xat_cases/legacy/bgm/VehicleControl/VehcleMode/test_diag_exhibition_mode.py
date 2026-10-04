import os, time
import sys
import pytest
import allure
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.interface.ecuinterface import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))


@allure.feature("架构基础")
@allure.story("整车模式")
class TestChangeExhibiMode(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.ipdu.start_all_time_control()
        self.busapp.start_all_cyclic_msg()
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.tester_present()
        sleep(0.5)
        self.sd_tester.update_serverdoipid(0x1002)
        self.ipdu.set_vehspd(0.0)
        sleep(1)
        self.sd_tester.change_usage_mode(1, do_assert=1)
        self.s2sbaseclass = S2sBaseClass([("VehicleModeService", "client")])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.change_car_mode_to_unexhibition()
        sleep(1)
        super().after_each_func(ecu)

    def after_class(self, ecu):
        self.ipdu.time_control_stop()  # 停止数据模拟(数据库周期性报文和调度表)
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动,总线开始收发报文
        sleep(0.5)
        self.sd_tester.stop_tester_present()
        sleep(0.5)
        self.sd_tester.diagnostic_client_sim_close()
        sleep(0.5)
        super().after_class(self, ecu)

    def get_exhibition_mode(self):
        '''
        获取展车模式
         返回 True 是展车模式，返回False 则不是
        @return:
        '''
        # doipid = kwargs.get('doipid', 0x1002)
        # self.update_serverdoipid(doipid)
        # 读取 模式
        self.sd_tester.send_data([0x22, 0xD1, 0x35])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
            "向1002发送  0x22, 0xD1,0X35"
        )[3:]
        curr_mode = result[0]
        if curr_mode == 1:
            return True
        else:
            return False

    def set_exhibition_mode(
        self,
        do_assert=True,
    ):
        '''
        进入展车模式
        前置条件
            1.FR:36-0-1:!=13 UsgModSts1_UsgModDriving
            2.FR:55-0-1:EpbStsEpbSts=3_AllAppld

        返回 True 是设置展车模式成功，返回 False 设置失败
        @return:
        '''
        self.sd_tester.update_serverdoipid(0x1002)
        logger.info("设置:FR:55-0-1:EpbStsEpbSts=3_AllAppld")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        time.sleep(0.3)
        # self.ipdu.check(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)

        ret = self.get_exhibition_mode()
        if ret:
            return ret

        # 检查当前会话，判断是否需要重新进入
        self.sd_tester.diagnostic_session_check()
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
            "Send f186 to get result"
        )[3:]
        curr_status = result[-1]
        if curr_status != 0x03:
            # 进入扩展会话
            self.sd_tester.enter_extended_session()
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
                "Send 1003 to get result"
            )
            if do_assert and result[0] != 0x50:
                assert 0, f'enter_extended_session 失败'
            self.sd_tester.security_access_level_l3()
        else:
            # 判断是否需要解锁
            self.sd_tester.client_sim.send_data([0x27, 0x05])
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
                "Send 0x27, 0x05 to get result"
            )
            curr_le = result[2:]
            if curr_le != [0x00, 0x00, 0x00]:
                # 三级 27 解锁
                self.sd_tester.security_access_level_l3()
        # 设置使用模式
        self.sd_tester.client_sim.send_data([0x2E, 0xD1, 0x35, 0x01])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
            "Send d135 to set exhibi mode"
        )
        curr_status = result[0]
        if do_assert and curr_status != 0x6E:
            assert 0, f'设置展车模式失败'
        # sleep(0.5)

        # 接受数据
        ret = self.get_exhibition_mode()
        if do_assert:
            assert ret, f'设置展车模式失败'
        return ret
    
    def set_exhibition_mode_no_appld(
        self,
        do_assert=True,
    ):
        '''
        进入展车模式
        前置条件
            1.FR:36-0-1:!=13 UsgModSts1_UsgModDriving
            2.FR:55-0-1:EpbStsEpbSts=3_AllAppld

        返回 True 是设置展车模式成功，返回 False 设置失败
        @return:
        '''
        self.sd_tester.update_serverdoipid(0x1002)
        # logger.info("设置:FR:55-0-1:EpbStsEpbSts=3_AllAppld")
        # self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        time.sleep(0.3)
        # self.ipdu.check(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)

        ret = self.get_exhibition_mode()
        if ret:
            return ret

        # 检查当前会话，判断是否需要重新进入
        self.sd_tester.diagnostic_session_check()
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
            "Send f186 to get result"
        )[3:]
        curr_status = result[-1]
        if curr_status != 0x03:
            # 进入扩展会话
            self.sd_tester.enter_extended_session()
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
                "Send 1003 to get result"
            )
            if do_assert and result[0] != 0x50:
                assert 0, f'enter_extended_session 失败'
            self.sd_tester.security_access_level_l3()
        else:
            # 判断是否需要解锁
            self.sd_tester.client_sim.send_data([0x27, 0x05])
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
                "Send 0x27, 0x05 to get result"
            )
            curr_le = result[2:]
            if curr_le != [0x00, 0x00, 0x00]:
                # 三级 27 解锁
                self.sd_tester.security_access_level_l3()
        # 设置使用模式
        self.sd_tester.client_sim.send_data([0x2E, 0xD1, 0x35, 0x01])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
            "Send d135 to set exhibi mode"
        )
        curr_status = result[0]
        if do_assert and curr_status != 0x6E:
            assert 0, f'设置展车模式失败'
        # sleep(0.5)

        # 接受数据
        ret = self.get_exhibition_mode()
        if do_assert:
            assert ret, f'设置展车模式失败'
        return ret
    

    def change_car_mode_to_exhibition(self, do_assert=True):
        '''
        诊断切换到 展车模式
        @return: True 切换成功 False 切换失败
        '''
        logger.info("设置:FR:55-0-1:EpbStsEpbSts=3_AllAppld")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        time.sleep(0.3)
        result = self.set_exhibition_mode()

        logger.info(F"切换到 展车模式 {'成功' if result else '失败'}")
        if do_assert:
            assert result, f"切换到展车模式失败 "
        return result

    def change_car_mode_to_unexhibition(self, do_assert=True, **kwargs):
        '''
        诊断切换到 非展车模式  退出展模式
        @return: True 切换成功 False 切换失败
        '''
        logger.info("设置:FR:55-0-1:EpbStsEpbSts=3_AllAppld")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        time.sleep(0.3)
        result = self.set_unexhibition_mode(do_assert=False, ipdu=self.ipdu)

        logger.info(F"退出展车模式 {'成功' if result else '失败'}")
        if do_assert:
            assert result, f"退出展车模式失败 "
        return result

    def set_unexhibition_mode(self, do_assert=True, **kwargs):
        '''
        退出展车模式

        返回 True 是退出展车模式成功，返回 False 退出失败
        @return:
        '''
        self.sd_tester.update_serverdoipid(0x1002)
        logger.info("设置:FR:55-0-1:EpbStsEpbSts=3_AllAppld")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        time.sleep(0.3)
        ret = self.get_exhibition_mode()
        if not ret:
            return not ret

        # 检查当前会话，判断是否需要重新进入
        self.sd_tester.diagnostic_session_check()
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
            "Send f186 to get result"
        )[3:]
        curr_status = result[-1]
        if curr_status != 0x03:
            # 进入扩展会话
            self.sd_tester.enter_extended_session()
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
                "Send 1003 to get result"
            )
            if do_assert and result[0] != 0x50:
                assert 0, f'enter_extended_session 失败'
            self.sd_tester.security_access_level_l3()
        else:
            # 判断是否需要解锁
            self.sd_tester.client_sim.send_data([0x27, 0x05])
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
                "Send 0x27, 0x03 to get result"
            )
            curr_le = result[2:]
            if curr_le != [0x00, 0x00, 0x00]:
                # 三级 27 解锁
                self.sd_tester.security_access_level_l3()
        # 设置使用模式
        self.sd_tester.client_sim.send_data([0x2E, 0xD1, 0x35, 0x00])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
            "Send dd0a to set usage mode"
        )
        curr_status = result[0]
        if do_assert and curr_status != 0x6E:
            assert 0, f'设置展车模式失败'
        # sleep(0.5)

        # 接受数据
        ret = self.get_exhibition_mode()
        if do_assert:
            assert not ret, f'设置展车模式失败'
        return not ret

    def set_lockunlock(self):
        self.ipdu.pause_all_bus_send()
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
        time.sleep(.5)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
        # self.ipdu.backbonefr_vddmbackbonefr03_gearlvrindcn_gearlvrindcn2_parkindcn()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 0)
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
        self.dk.set_drvr_seat_notpresent()
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        time.sleep(.3)
        self.io.set_four_door_close()
        self.io.trunk_door_close()
        self.io.hood_door1_close()
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorDrvrSts_2_CemBodySignalIPdu02', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorPassSts_2_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorLeReSts_1_CemBodySignalIPdu02', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorRiReSts_1_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'TrSts_2_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06,'HoodSts', 2)
        time.sleep(.3)
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        self.dk.set_cenlock_sts(0x1)
        self.ipdu.resume_all_bus_send()

    def change_usage_driving(self):
        '''切driving'''
        self.set_lockunlock()
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 11}
        )
        self.ipdu.backbonefr_vddmbackbonefr00_engst1wdstsengst1wdsts_engst1_runngrunng()
        time.sleep(.5)
        self.ipdu.backbonefr_vddmbackbonefr00_engst1wdstsengst1wdsts_engst1_runngrunng()
        self.check_usage_mode_status(UsageMode.DRIVING)

    @pytest.mark.smoke
    @pytest.mark.verify
    def test_diag_enter_exhibition_caseid_113348(self):
        '''诊断进展车'''
        self.change_car_mode_to_exhibition()
        time.sleep(2)
        self.ipdu.check(
            self.ipdu.propulsioncan.BgmPropulsionFr01,
            'ExhibitionModeStsExhibitionModeSts_1_BgmPropSignalIPdu01',
            'OnOff1_On',
        )

    @pytest.mark.smoke
    def test_diag_exit_exhibition_caseid_113341(self):
        '''诊断退展车'''
        self.change_car_mode_to_unexhibition()
        time.sleep(2)
        self.ipdu.check(
            self.ipdu.propulsioncan.BgmPropulsionFr01,
            'ExhibitionModeStsExhibitionModeSts_1_BgmPropSignalIPdu01',
            'OnOff1_Off',
        )

    @pytest.mark.full
    # @pytest.mark.xfail
    def test_diag_exit_exhibition_caseid_113324(self):
        '''driving下无法进入展车模式_诊断进入'''
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(13)
        # self.change_usage_driving()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        time.sleep(0.3)
        self.set_exhibition_mode(False)
        time.sleep(2)
        self.ipdu.check(
            self.ipdu.propulsioncan.BgmPropulsionFr01,
            'ExhibitionModeStsExhibitionModeSts_1_BgmPropSignalIPdu01',
            'OnOff1_Off',
        )
    
    @pytest.mark.full
    # @pytest.mark.xfail
    def test_diag_exit_exhibition_caseid_113317(self):
        '''非allappld下无法进入展车模式_诊断进入'''
        # self.change_usage_driving()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 1)
        time.sleep(0.3)
        self.set_exhibition_mode_no_appld(False)
        time.sleep(2)
        self.ipdu.check(
            self.ipdu.propulsioncan.BgmPropulsionFr01,
            'ExhibitionModeStsExhibitionModeSts_1_BgmPropSignalIPdu01',
            'OnOff1_Off',
        )

    

