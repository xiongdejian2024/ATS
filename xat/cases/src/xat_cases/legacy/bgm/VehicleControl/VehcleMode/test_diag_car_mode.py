import os,time
import sys
import allure
import pytest
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.interface.ecuinterface import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

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

@allure.feature("车身网关测试/基础架构")
@allure.story("整车模式/车辆模式")
class TestChangeCarMode(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.nucapp.bgm_diag_line_up()
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        time.sleep(.5)
        self.sd_tester.diagnostic_client_sim_start()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        # Code Location
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(0x3)
        time.sleep(1)
        self.dk.set_cenlock_sts(0x1)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        time.sleep(.5)
        # self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)


    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        self.sd_tester.change_car_mode(0)
        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        self.nucapp.bgm_diag_line_down()
        self.sd_tester.diagnostic_client_sim_close()
        super().after_class(self, ecu)

    def usage_mode_change_driving(self):
        self.dk.set_cenlock_sts(0x3)
        time.sleep(1)
        self.dk.set_cenlock_sts(0x1)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 11}
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        expectedvalue = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts')
        assert expectedvalue == 5, "动力未置成功"
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModDrvg',
        )

    def check_car_mode_status(self, expectedmode, do_assert=True, **kwargs):
        '''
        校验 car 状态
        @param expectedmode:
        @param do_assert:
        @param timeout:
        @param kwargs:
        @return:
        '''
        timeout = kwargs.get('timeout', 5)
        msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.bodycan.CEMBodyFr12)
        signal_name = kwargs.get('signal_name', 'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12')

        result, realvalue, expectedvalue = self.ipdu.check(msg_signals_obj=msg_signals_obj,
                                                           signal_name=signal_name,
                                                           sig_value_name=expectedmode,
                                                           do_assert=do_assert, timeout=timeout, )
        return result, realvalue, expectedvalue

    def not_change_car_mode(self, mode_type: int, do_assert=True, **kwargs):
        '''
        切换 car mode
        @param mode_type: 切换的 模式
                    0 : NORMAL
                    1 : TRANSPORT
                    2 : FACTORY
                    3 : CRASH
                    5 : DYNO
        @param do_assert: 若为True 则表示切换失败则会报错，否则返回切换后的模式
        @return:
        '''
        # 读取did
        self.sd_tester.information_check_d134()
        # 接受数据
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send d134 to get result")[3:]
        curr_mode = result[0]
        if curr_mode == mode_type:
            return curr_mode
        # 检查当前会话，判断是否需要重新进入
        self.sd_tester.diagnostic_session_check()
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send f186 to get result")[3:]
        curr_status = result[-1]
        if curr_status != 0x03:
            # 进入扩展会话
            self.sd_tester.enter_extended_session()
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 1003 to get result")
            if do_assert and result[0] != 0x50:
                assert 0, f'enter_extended_session 失败'
            self.sd_tester.security_access_level_l2()
        else:
            # 判断是否需要解锁
            self.sd_tester.client_sim.send_data([0x27, 0x03])
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 0x27, 0x03 to get result")
            curr_le = result[2:]
            if curr_le != [0x00, 0x00, 0x00]:
                # 三级 27 解锁
                self.sd_tester.security_access_level_l2()
        # 设置 car 模式
        self.sd_tester.io_control_car_mode_control(mode_type)
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send d134 to set car mode")
        assert result[0] != 0x6F, '不应切换成功'

    @pytest.mark.smoke
    @pytest.mark.verify
    @pytest.mark.full
    def test_car_mode_caseid_110036(self, **kwargs):
        '''
        crash to normal
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==3 CarModSts1_CarModCrash
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(3)
        self.check_car_mode_status(3)
        time.sleep(.3)                                  
        self.sd_tester.change_car_mode(0)
        self.check_car_mode_status(0)

    @pytest.mark.full
    def test_car_mode_caseid_110153(self, **kwargs):
        '''
        normal to crash
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  == 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(13)
        # self.usage_mode_change_driving()
        time.sleep(.3)
        self.not_change_car_mode(3)
        self.check_car_mode_status(0)
        self.sd_tester.change_usage_mode(1)

    @pytest.mark.full
    def test_car_mode_caseid_110076(self, **kwargs):
        '''
        factory to dyno
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==2 CarModSts1_CarModFactory
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd

        '''
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)
        time.sleep(.3)                                  
        self.sd_tester.change_car_mode(5)
        self.check_car_mode_status(5)


    @pytest.mark.full
    def test_car_mode_caseid_110106(self, **kwargs):
        '''
        transport to dyno
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==1 CarModSts1_CarModTransport
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd

        '''
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)
        time.sleep(.3)    
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)                              
        self.sd_tester.change_car_mode(5)
        self.check_car_mode_status(5)

    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_110154(self, **kwargs):
        '''
        crash to normal
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==3 CarModSts1_CarModCrash
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd

        '''
        self.sd_tester.change_car_mode(3)
        self.check_car_mode_status(3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)
        self.sd_tester.change_car_mode(0)
        self.check_car_mode_status(0)

    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_110124(self, **kwargs):
        '''
        factory to normal
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==3 CarModSts1_CarModFactory
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd

        '''
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)
        time.sleep(.3)    
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)                              
        self.sd_tester.change_car_mode(0)
        self.check_car_mode_status(0)



    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_110083(self, **kwargs):
        '''
        normal to crash
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd

        '''   
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)                         
        self.not_change_car_mode(3)
        self.check_car_mode_status(0)


    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_110081(self, **kwargs):
        '''
        normal to factory
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd

        '''  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)                                
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)


    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_110161(self, **kwargs):
        '''
        transport to normal
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==1 CarModSts1_CarModTransport
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)
        time.sleep(.3)      
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)                         
        self.sd_tester.change_car_mode(0)
        self.check_car_mode_status(0)

    @pytest.mark.full
    def test_car_mode_caseid_110055(self, **kwargs):
        '''
        factory to transport
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==2 CarModSts1_CarModFactory
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)
        time.sleep(.3)                                  
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)


    @pytest.mark.full
    def test_car_mode_caseid_109997(self, **kwargs):
        '''
        transport to factory
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==1 CarModSts1_CarModTransport
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)
        time.sleep(.3)   
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)                               
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)


    @pytest.mark.full
    def test_car_mode_caseid_109900(self, **kwargs):
        '''
        factory to crash
                1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
                2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==2 CarModSts1_CarModFactory
                3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
                4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)
        time.sleep(.3)               
        self.sd_tester.change_car_mode(3)
        self.check_car_mode_status(3)

    @pytest.mark.full
    def test_car_mode_caseid_110090(self, **kwargs):
        '''
        crash to transport
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==3 CarModSts1_CarModCrash
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(3)
        self.check_car_mode_status(3)
        time.sleep(.3)                                  
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)

    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_109984(self, **kwargs):
        '''
        normal to factory
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''                                 
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)

    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_1959736(self, **kwargs):
        '''
        109963
        normal to crash
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''                                 
        self.sd_tester.change_car_mode(3)
        self.check_car_mode_status(3)

    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_109951(self, **kwargs):
        '''
        factory to normal
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==2 CarModSts1_CarModFactory
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)
        time.sleep(.3)                                  
        self.sd_tester.change_car_mode(0)
        self.check_car_mode_status(0)

    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_109914(self, **kwargs):
        '''
        normal to transport
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''                      
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)

    @pytest.mark.full
    def test_car_mode_caseid_109941(self, **kwargs):
        '''
        transport to crash
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==1 CarModSts1_CarModTransport
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)
        time.sleep(.3)                 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)                 
        self.not_change_car_mode(3)
        self.check_car_mode_status(1)

    @pytest.mark.full
    def test_car_mode_caseid_109925(self, **kwargs):
        '''
        transport to crash
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==1 CarModSts1_CarModTransport
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)
        time.sleep(.3)                                  
        self.sd_tester.change_car_mode(3)
        self.check_car_mode_status(3)

    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_109949(self, **kwargs):
        '''
        normal to transport
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''     
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)                         
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)

    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_109899(self, **kwargs):
        '''
        normal to dyno
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''  
        self.sd_tester.change_car_mode(0) 
        self.check_car_mode_status(0)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        time.sleep(1)
        self.sd_tester.change_car_mode(5)
        self.check_car_mode_status(5)

    @pytest.mark.full
    def test_car_mode_caseid_110159(self, **kwargs):
        '''
        crash to factory
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==3 CarModSts1_CarModCrash
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(3)
        self.check_car_mode_status(3)
        time.sleep(.3)                                  
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)

    @pytest.mark.full
    def test_car_mode_caseid_110115(self, **kwargs):
        '''
        crash to dyno
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==3 CarModSts1_CarModCrash
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(3)
        self.check_car_mode_status(3)
        time.sleep(.3)                                  
        self.sd_tester.change_car_mode(5)
        self.check_car_mode_status(5)

    @pytest.mark.full
    def test_car_mode_caseid_110110(self, **kwargs):
        '''
        dyno to factory
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==5 CarModSts1_CarModDyno
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(5)
        self.check_car_mode_status(5)
        time.sleep(.3)                                  
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)


    @pytest.mark.full
    def test_car_mode_caseid_109999(self, **kwargs):
        '''
        crash to transport
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==3 CarModSts1_CarModCrash
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(3)
        self.check_car_mode_status(3)
        time.sleep(.3)            
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)
    
    @pytest.mark.full
    def test_car_mode_caseid_110017(self, **kwargs):
        '''
        dyno to crash
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==5 CarModSts1_CarModDyno
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(5)
        self.check_car_mode_status(5)
        time.sleep(.3)        
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)                          
        self.not_change_car_mode(3)
        self.check_car_mode_status(5)

    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_110007(self, **kwargs):
        '''
        dyno to normal
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==5 CarModSts1_CarModDyno
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(5)
        self.check_car_mode_status(5)
        time.sleep(.3)                                  
        self.sd_tester.change_car_mode(0)
        self.check_car_mode_status(0)

    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_1959742(self, **kwargs):
        '''
        110035
        dyno to normal
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==5 CarModSts1_CarModDyno
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(5)
        self.check_car_mode_status(5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)
        self.sd_tester.change_car_mode(0)
        self.check_car_mode_status(0)

    @pytest.mark.full
    def test_car_mode_caseid_110118(self, **kwargs):
        '''
        dyno to transport
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==5 CarModSts1_CarModDyno
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(5)
        self.check_car_mode_status(5)
        time.sleep(.3)                                  
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)

    @pytest.mark.full
    def test_car_mode_caseid_110038(self, **kwargs):
        '''
        crash to factory
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==3 CarModSts1_CarModCrash
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(3)
        self.check_car_mode_status(3)
        time.sleep(.3)                    
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)              
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)

    @pytest.mark.full
    def test_car_mode_caseid_109893(self, **kwargs):
        '''
        dyno to crash
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==5 CarModSts1_CarModDyno
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''

        self.sd_tester.change_car_mode(5)
        self.check_car_mode_status(5)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        time.sleep(.3)                                  
        self.sd_tester.change_car_mode(3)
        self.check_car_mode_status(3)

    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_1959734(self, **kwargs):
        '''
        transport to normal110069
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==5 CarModSts1_CarModTrans
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)
        time.sleep(.3)                                  
        self.sd_tester.change_car_mode(0)
        self.check_car_mode_status(0)


    @pytest.mark.smoke
    @pytest.mark.full
    def test_car_mode_caseid_110056(self, **kwargs):
        '''
        normal to dyno
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==5 CarModSts1_CarModDyno
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''        
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)
        self.not_change_car_mode(5)
        self.check_car_mode_status(0)


#######################################full用例######################################################################
    # @pytest.mark.xfail(condition=lambda: True, reason='这是一个预期失败的用例')
    @pytest.mark.full
    def test_car_mode_caseid_109928(self, **kwargs):
        '''
        crash to dyno
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==5 CarModSts1_CarModDyno
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(3)
        self.check_car_mode_status(3)    
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)                             
        time.sleep(.3)
        self.not_change_car_mode(5)
        self.check_car_mode_status(3)

    # @pytest.mark.xfail(condition=lambda: True, reason='这是一个预期失败的用例')
    @pytest.mark.full
    def test_car_mode_caseid_110117(self, **kwargs):
        '''
        dyno to factory
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==5 CarModSts1_CarModDyno
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(5)
        self.check_car_mode_status(5)
        time.sleep(.3)        
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)                          
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)

    @pytest.mark.full
    def test_car_mode_caseid_110004(self, **kwargs):
        '''
        factory to crash
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==5 CarModSts1_CarModCrash
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)                             
        time.sleep(.3) 
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'VehMtnStVehMtnSt_1_CemBodySignalIPdu02', 0)
        self.not_change_car_mode(3)
        self.check_car_mode_status(2)

    @pytest.mark.full
    def test_car_mode_caseid_110002(self, **kwargs):
        '''
        dyno to transport
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==5 CarModSts1_CarModDYNO
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.sd_tester.change_car_mode(5)
        self.check_car_mode_status(5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)
        time.sleep(1)       
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)

    @pytest.mark.full
    def test_car_mode_caseid_109927(self, **kwargs):
        '''
        factory to dyno
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==2 CarModSts1_CarModFactory
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd

        Carmode_Factory诊断切换车辆模式为Dyno_Unkown无法切换
        '''
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)
        time.sleep(.3)
        self.not_change_car_mode(5)
        self.check_car_mode_status(2)

    @pytest.mark.full
    def test_car_mode_caseid_110001(self, **kwargs):
        '''
        factory to transport
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==1 CarModSts1_CarModTransport
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd

        '''
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)                                 
        time.sleep(.3) 
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)

    @pytest.mark.full
    def test_car_mode_caseid_110023(self, **kwargs):
        '''
        transport to factory
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==1 CarModSts1_CarModTransport
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd

        '''
        self.sd_tester.change_car_mode(1)
        self.check_car_mode_status(1)    
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)                             
        time.sleep(.3) 
        self.sd_tester.change_car_mode(2)
        self.check_car_mode_status(2)

    @pytest.mark.full
    # @pytest.mark.xfail(condition=lambda: True, reason='这是一个预期失败的用例')
    def test_car_mode_caseid_110067(self, **kwargs):
        '''
        normal to dyno
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==1 CarModSts1_CarModTransport
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd

        '''
        self.sd_tester.change_car_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 0)
        time.sleep(.3) 
        self.not_change_car_mode(5)
        self.check_car_mode_status(1)
##################################非standstill无法切#######################################################
    @pytest.mark.full
    # @pytest.mark.xfail(condition=lambda: True, reason='这是一个预期失败的用例')
    def test_car_mode_caseid_110116(self, **kwargs):
        '''
        normal to factory
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 != 0 || 1 || 2 ||  3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_rollgfwdval1()
        time.sleep(.3) 
        self.not_change_car_mode(2)
        self.check_car_mode_status(0)

    @pytest.mark.full
    # @pytest.mark.xfail(condition=lambda: True, reason='这是一个预期失败的用例')
    def test_car_mode_caseid_110134(self, **kwargs):
        '''
        normal to crash
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 != 0 || 1 || 2 ||  3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_rollgfwdval1()
        time.sleep(.3) 
        self.not_change_car_mode(3)
        self.check_car_mode_status(0)

    @pytest.mark.full
    # @pytest.mark.xfail(condition=lambda: True, reason='这是一个预期失败的用例')
    def test_car_mode_caseid_109988(self, **kwargs):
        '''
        normal to dyno
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 != 0 || 1 || 2 ||  3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_rollgfwdval1()
        time.sleep(.3) 
        self.not_change_car_mode(5)
        self.check_car_mode_status(0)

    @pytest.mark.full
    # @pytest.mark.xfail(condition=lambda: True, reason='这是一个预期失败的用例')
    def test_car_mode_caseid_109892(self, **kwargs):
        '''
        normal to transport
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 != 0 || 1 || 2 ||  3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_rollgfwdval1()
        time.sleep(.3)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'VehMtnStVehMtnSt_1_CemBodySignalIPdu02', 4)
        self.not_change_car_mode(1)
        self.check_car_mode_status(0)
