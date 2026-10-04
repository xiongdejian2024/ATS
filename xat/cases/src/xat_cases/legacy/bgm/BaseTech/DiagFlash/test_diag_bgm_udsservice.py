import time
import pytest
from xat_cases.legacy.bgm.BaseTech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
import json

@allure.feature('BGM BaseTech/诊断功能/基础诊断')
class TestUdsServiceApp(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("before_class")
        self.vin = self.sd_tester.get_vehicle_identification_number()
        self.f1aa = self.sd_tester.get_ecu_core_assembly_part_number()
        self.f1ab = self.sd_tester.get_ecu_delivery_assembly_part_number()
        with allure.step("初始化环境"):
            self.mix.init_boot_per()

    def before_each_func(self, ecu):
        data1 = self.sd_tester.send_data_and_check(TA.BGM_SOC,'22f186','62f186')
        if data1[6:] == '02':
            self.sd_tester.send_data_and_check(TA.BGM_SOC,'1001','5001')
            time.sleep(1)
            self.sd_tester.send_data_and_check(TA.BGM_SOC,'22f186','62f18601')
        data2 = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22f186','62f186')
        if data2[6:] == '02':
            self.sd_tester.exit_muc_boot()
        super().before_each_func(ecu)
        # self.sd_tester.update_serverdoipid(0x1002)
        # err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86])
        # if recv_data_list[3] == 0x2:
        #     self.sd_tester.quit_boot()
        # self.sd_tester.update_serverdoipid(0x1001)
        # self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        logger.info("after_class")
        with allure.step("恢复环境"):
            self.mix.init_boot_per()
        super().after_class(self, ecu)

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x10_NRC12测试')
    def test_caseid_1981442(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.DEFAULT, ['62f18601', '62f18601'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x10, 0x11], ['7f1012', '7f1012'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x10, 0x22], ['7f1012', '7f1012'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x10, 0x33], ['7f1012', '7f1012'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x22, 0xf1, 0x86], ['62f18601', '62f18601', ])

    # BGM_SOC,BGM_MCU 发10010203040506，1001回正响应，没有做超出诊断请求长度的判定，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x10_NRC13测试')
    def test_caseid_1981439(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.DEFAULT, ['62f18601', '62f18601'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x10], ['7f1013', '7f1013'])
        # self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x10,0x01,0x02,0x03,0x04,0x05,0x06],['7f1013','7f1013'])

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x10_NRC22测试')  # 切换会话，usagmode会恢复状态，所以01会话下永远满足不是driving的状态
    def test_caseid_1981436(self):
        pass

    #BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下进入ProgrammingSession的条件检查_Pre-condition_Speed>3Km/h')
    def test_caseid_1981306(self):
        with allure.step("初始化环境成功进boot"):
            self.mix.init_boot_per()
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x0206,0x01,SESSION.DEFAULT,UnLock.L0,'','710102061001')
        # self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU,0x0206,0x01,SESSION.EXTENDED,UnLock.L0,'','710102061001')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.exit_muc_boot()
        with allure.step("车速设为39.1km/h"):
            self.bus_comm.set_vehspd_and_qf(10000,VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
            time.sleep(1)
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x0206,0x01,SESSION.DEFAULT,UnLock.L0,'','710102061002')
        # self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'7f1022',check_method=Check_Method.response)
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU,0x0206,0x01,SESSION.EXTENDED,UnLock.L0,'','710102061002')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'1002','7f1022')
        self.bus_comm.set_vehspd_and_qf(0,VehSpdQf(2))

        # BGM_SOC BGM_MCU 少写MCU

    # BGM_SOC,BGM_MCU  成功回负响应，但是BGM会异常断联，导致DOIP连不上,已解决
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x11_NRC12测试')
    def test_caseid_1981427(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.DEFAULT, ['62f18601', '62f18601'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x11, 0x11], '7f1112')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x11, 0x11], '7f1112')
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x11, 0x51], ['7f1112', '7f1112'])
        # self.sd_tester.sd_tester.stop_tester_present()
        # self.sd_tester.wait_vehicle_announcement()
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x11, 0xff], ['7f1112', '7f1112'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x22, 0xf1, 0x86], ['62f18601', '62f18601'])
        # pass

    # BGM_SOC,BGM_MCU    110101,1001回5001,提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x11_NRC13测试')
    def test_caseid_1981424(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.DEFAULT, ['62f18601', '62f18601'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x11], ['7f1113', '7f1113'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x11, 0x01, 0x01], '7f1113')
        # self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x11,0x01,0x01],['7f1113','7f1113'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x22, 0xf1, 0x86], ['62f18601', '62f18601'])

    #     #pass

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x11_NRC22测试')
    def test_caseid_1981421(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa040, 0x01, SESSION.EXTENDED, UnLock.L7, '0100', '7101a040')
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb165, SESSION.EMPTY, '62b16501')
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.DEFAULT, ['62f18601', '62f18601'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x11, 0x01], ['7f1122', '7f1122'])
        self.sd_tester.close_fireware()

    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x14功能测试')
    def test_caseid_1981344(self):
        self.mix.set_dtc_precontion()
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x02, 0x08])
        self.sd_tester.clear_all_dtc_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L0, '54')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x02, 0x08])
        # # self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EXTENDED,UnLock.L0,'0080','62429e00')
        # # time.sleep(8)
        # # self.sd_tester.write_ccp({1:0x01})
        # # self.sd_tester.send_dtc_request_and_return_check_status()
        # # self.sd_tester.write_ccp({1:0xa3})
        # # self.sd_tester.send_dtc_request_and_return_check_status()
        # self.mix.init_boot_per()
        # # self.sd_tester.clear_dtc_and_check(TA.BGM_MCU,SESSION.EMPTY,UnLock.L0,'54')
        # # self.sd_tester.clear_dtc_and_check(TA.BGM_MCU,SESSION.EMPTY,UnLock.L0,'54')
        # self.sd_tester.reset_0x1181()
        # self.bus_comm.set_batter_sensor_hw_failure(BattSnsrHwFltRaw.DevErrSts2_Flt)
        # self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        # self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.EXTENDED,UnLock.L0,'0080','62429e00',recover=False)
        # time.sleep(20)
        # #self.sd_tester.write_ccp({1:0x02})
        # #self.sd_tester.read_did_and_check(TA.BGM_MCU,0xe103,SESSION.EMPTY,'62e103',check_length=68)
        # self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xA1,0xDB,0x96,0x20])
        # self.sd_tester.clear_all_dtc_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0,'54')
        # self.sd_tester.read_dtc_and_check(TA.BGM_MCU,0x04,0xA1DB9620,'5904A1DB96')
        # pass

    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x14测试')
    def test_caseid_1981347(self):
        self.sd_tester.clear_all_dtc_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L0, '54')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x14测试_NRC13')
    def test_caseid_1981342(self):
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14], '7f1413')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff], '7f1413')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff, 0xff], '7f1413')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff, 0xff, 0xff, 0xff, 0xff], '7f1413')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x14测试_NRC31')
    def test_caseid_1981339(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0x00, 0x00, 0x00], '7f1431')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff, 0xff, 0x00], '7f1431')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff, 0xff, 0x33], '7f1431')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff, 0xff, 0xd0], '7f1431')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x14测试_NRC31')
    def test_caseid_1981340(self):
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0x00, 0x00, 0x00], '7f1431')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff, 0xff, 0x00], '7f1431')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff, 0xff, 0x33], '7f1431')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff, 0xff, 0xd0], '7f1431')

    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x19_0x02测试')
    def test_caseid_1981338(self):
        self.mix.set_dtc_precontion()
        self.sd_tester.send_dtc_request_and_return_check_status()
        # pass

    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x19_0x04测试')
    def test_caseid_1981337(self):
        self.mix.set_dtc_precontion()
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x04, 0xa0, 0x1d, 0x23, 0x20], '5904a01d23')

    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x19_0x0A测试')
    def test_caseid_1981336(self):
        dtc_json = open('./config/DTC.json')
        dtc_data = json.load(dtc_json).get('DTC')
        self.mix.set_dtc_precontion()
        dtc_read_data = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x0a], '590a7f')
        dtc_num = int(len(dtc_read_data[6:]) / 8)
        for dtc in dtc_data:
            if dtc.lower() not in dtc_read_data:
                logger.info(f'{dtc}不在读取的dtc中')
        if dtc_num != len(dtc_data):
            assert False, f'DTC数量不一致,json中的数据量为{len(dtc_data)},读取的数量为：{dtc_num}'

            # BGM_MCU

    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x19_NRC12测试')
    def test_caseid_1981329(self):
        for sv in range(0x00, 0xFF):
            if (sv == 0x02 or sv == 0x04 or sv == 0x0a or sv == 0x82 or sv == 0x84 or sv == 0x8a):
                continue
            else:
                self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, sv], '7f1912')

        # pass

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x19_NRC13测试')
    def test_caseid_1981327(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.DEFAULT, '62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19], '7f1913')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x02], '7f1913')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x02, 0x7f, 0x00], '7f1913')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x04], '7f1913')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x04, 0xf1], '7f1913')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x04, 0xf1, 0x17, 0x88, 0x20, 0x00], '7f1913')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x0a, 0x00], '7f1913')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x19_NRC31测试')
    def test_caseid_1981325(self):
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x04, 0xf1, 0x17, 0x88, 0x01], '7f1931')

    # BGM_SOC,BGM_MCU 1001在22f18601下回正响应，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x22_NRC13测试')
    def test_caseid_1981366(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.DEFAULT, ['62f18601', '62f18601'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x22], ['7f2213', '7f2213'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x22, 0xf1, 0x86, 0x01], '7f2213')
        # self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x22,0xf1,0x86,0x01],['7f2213','7f2213'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x22, 0xf1, 0x86], ['62f18601', '62f18601'])

    #     pass

    # BGM_SOC,BGM_MCU NRC14测试不出来
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x22_NRC14测试')
    def test_caseid_1981358(self):
        # self.sd_tester.read_did_and_check([TA.BGM_MCU,TA.BGM_SOC],0xf190f1aaf1abed20f1a0ed20ed20ed20,SESSION.EMPTY,['7f2214','7f2214'])
        pass

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x22_NRC31测试')
    def test_caseid_1981363(self):
        self.sd_tester.read_did_and_check([TA.BGM_MCU, TA.BGM_SOC], 0xffff, SESSION.EMPTY, ['7f2231', '7f2231'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x22, 0x00, 0x00], ['7f2231', '7f2231'])

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x27服务测试')
    def test_caseid_1981418(self):
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x27, 0x01], check_data=['7f277f', '7f277f'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x03], check_data='7f277f')
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x27, 0x05], check_data=['7f277f', '7f277f'])
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x07], check_data='7f277f')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x11], check_data='7f277f')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x28测试')
    def test_caseid_1981399(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.DEFAULT, '62f18601')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x00, 0x01, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x00, 0x02, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x00, 0x03, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x01, 0x01, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x01, 0x02, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x01, 0x03, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x02, 0x01, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x02, 0x02, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x02, 0x03, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x03, 0x01, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x03, 0x02, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x03, 0x03, SESSION.EMPTY, UnLock.L0, '7f287f')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x28测试-带正响应抑制')
    def test_caseid_1981398(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.DEFAULT, '62f18601')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x80, 0x01, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x80, 0x02, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x80, 0x03, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x81, 0x01, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x81, 0x02, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x81, 0x03, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x82, 0x01, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x82, 0x02, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x82, 0x03, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x83, 0x01, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x83, 0x02, SESSION.EMPTY, UnLock.L0, '7f287f')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x83, 0x03, SESSION.EMPTY, UnLock.L0, '7f287f')

    # #BGM_MCU 诊断调度表上会话都可以写，无法测出7F MS已删除
    # @pytest.mark.full
    # @allure.story('基础诊断服务-New')
    # @allure.title('01会话下0x2E_NRC7F测试')
    # def test_caseid_1981348(self):
    #     # self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.DEFAULT,'62f18601')
    #     # self.sd_tester.write_did_and_check(TA.BGM_MCU,'dd01',SESSION.EMPTY,UnLock.L0,'ffffff','7f2e7f')
    #     # self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x22,0xf1,0x86],'62f18601')
    #     pass

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x31_NRC12测试')
    def test_caseid_1981280(self):
        self.sd_tester.routine_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], 0x0206, 0x10, SESSION.EMPTY, UnLock.L0, '',
                                              ['7f3112', '7f3112'])
        # pass

    # BGM_SOC,BGM_MCU 1001没有做出超出长度的判定，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x31_NRC13测试')
    def test_caseid_1981276(self):
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x31], ['7f3113', '7f3113'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x31, 0x01], ['7f3113', '7f3113'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x31, 0x01, 0x02], ['7f3113', '7f3113'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x31, 0x01, 0x02, 0x06, 0x06], '7f3113')
        # self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x31,0x01,0x02,0x06,0x06],['7f3113','7f3113'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x31, 0x01, 0x20], '7f3113')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x31, 0x01, 0x20, 0xf2, 0xf2, 0xf2, 0xf2], '7f3113')
        # self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x31,0x01,0x20,0xf2,0xf2,0xf2],['7f3113','7f3113'])
        # pass

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x31_NRC31测试')
    def test_caseid_1981271(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.DEFAULT, ['62f18601', '62f18601'])
        self.sd_tester.routine_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], 0xffff, 0x01, SESSION.EMPTY, UnLock.L0, '',
                                              ['7f3131', '7f3131'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x31, 0x01, 0x00, 0x00], ['7f3131', '7f3131'])
        # pass

    # BGM_SOC,BGM_MCU SOC下默认会话34回正响应，需求是在02、L1下，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x34 0x00测试')
    def test_caseid_1981300(self):
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC],
                                           [0x34, 0x00, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                           ['7f3411', '7f347f'])
        # pass

    # BGM_SOC,BGM_MCU  SOC下默认会话34回正响应，需求是在02、L1下，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x34 0x10测试')
    def test_caseid_1981297(self):
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC],
                                           [0x34, 0x10, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                           ['7f3411', '7f347f'])

    #     #pass

    # BGM_SOC,BGM_MCU SOC下默认会话34回正响应，需求是在02、L1下，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x34 0x80测试')
    def test_caseid_1981294(self):
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC],
                                           [0x34, 0x80, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                           ['7f3411', '7f347f'])

    #     #pass

    # BGM_SOC,BGM_MCU  SOC下默认会话34回正响应，需求是在02、L1下，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x36测试')
    def test_caseid_1981291(self):
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x36, 0x01], ['7f3611', '7f3611'])

    #     #pass

    # BGM_SOC,BGM_MCU  SOC下默认会话34回正响应，需求是在02、L1下，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x37测试')
    def test_caseid_1981287(self):
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x37], ['7f3711', '7f3711'])

    #     #pass
    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x36重复传输数据块')
    def test_caseid_1981288(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L1, check_data='2702')
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EMPTY, UnLock.L1, check_data='2702')
        # self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x34,0x00,0x44,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],'743007d000')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,
                                           [0x34, 0x00, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                           '743007d000')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x36, 0x01], '7601')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x36, 0x01], '7601')
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1181')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下0x85测试')
    def test_caseid_1981385(self):
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU, 0x01, SESSION.EMPTY, UnLock.L0, '7f857f')
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU, 0x02, SESSION.EMPTY, UnLock.L0, '7f857f')
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU, 0x81, SESSION.EMPTY, UnLock.L0, '7f857f')
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU, 0x82, SESSION.EMPTY, UnLock.L0, '7f857f')
        # pass

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下11 01复位测试')
    def test_caseid_1981433(self):
        self.sd_tester.hard_reset(TA.BGM_MCU)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        # pass

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下11 81复位测试')
    def test_caseid_1981431(self):
        self.sd_tester.reset_0x1181()

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下3E 00测试')
    def test_caseid_1981405(self):
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x3e, 0x00], ['7e00', '7e00'])
        # pass

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下3E 80测试')
    def test_caseid_1981403(self):
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x3e, 0x80], ['', ''])
        # pass

    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下DTC掩码测试')
    def test_caseid_1981323(self):
        # self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
        # self.sd_tester.change_usage_mode(ACTIVE)
        self.mix.set_dtc_precontion()
        self.sd_tester.send_dtc_request_and_return_check_status()
        # self.sd_tester.change_usage_mode(INACTIVE)
        # self.sd_tester.send_dtc_request_and_check_dtc_status([0xf1,0x17,0x88],'08')
        # pass

    # BGM_SOC,BGM_MCU  接口不适配
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下功能寻址请求长度测试')
    def test_caseid_1981469(self):
        self.sd_tester.send_data_and_check(TA.FUNCTION, '22f1aa',
                                           {'10 01': f'62f1aa{self.f1aa}', '10 02': f'62f1aa{self.f1aa}'})
        self.sd_tester.send_data_and_check(TA.FUNCTION, '22f1aaf1ab', {'10 01': f'62f1aa{self.f1aa}f1ab{self.f1ab}',
                                                                       '10 02': f'62f1aa{self.f1aa}f1ab{self.f1ab}'})
        self.sd_tester.send_data_and_check(TA.FUNCTION, '22f1aaf1abf18cf186', {'10 01': '62', '10 02': '62'})
        self.sd_tester.send_data_and_check(TA.BGM_MCU, '22f1aaf1abf18cf186f1aaf1abf18cf186f1aaf1ab', '62')

    #     #pass

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下执行10 01')
    def test_caseid_1981460(self):
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x10, 0x01], '5001')
        second_time = time.time()
        assert (second_time - current_time) <= 0.2 or (second_time - current_time) <= 5
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x01], '5001')
        second_time = time.time()
        assert (second_time - current_time) <= 0.2 or (second_time - current_time) <= 5

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下执行10 02')
    def test_caseid_1981448(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.exit_muc_boot()
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下执行10 03')
    def test_caseid_1981454(self):
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x10, 0x03], '5003')
        second_time = time.time()
        assert (second_time - current_time) <= 0.2 or (second_time - current_time) <= 5
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x03], '5003')
        second_time = time.time()
        assert (second_time - current_time) <= 0.2 or (second_time - current_time) <= 5

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下执行10 81')
    def test_caseid_1981457(self):
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x10, 0x81])
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x22, 0xf1,0x86],'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x81])
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x22, 0xf1,0x86],'62f18601')

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下执行10 82')
    def test_caseid_1981445(self):
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x10, 0x82])
        time.sleep(20)
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x22, 0xf1,0x86],'62f18602')
        self.sd_tester.exit_muc_boot()
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x82])
        time.sleep(2)
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x22, 0xf1,0x86],'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x01])
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x22, 0xf1,0x86],'62f18601')

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下执行10 83')
    def test_caseid_1981451(self):
        current_time = time.time()
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x10, 0x83])
        if data == '7f1078':
            second_time = time.time()
            assert (second_time - current_time) <= 5
        else:
            assert True
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x83])
        if data == '7f1078':
            second_time = time.time()
            assert (second_time - current_time) <= 5
        else:
            assert True

    # 判断结果参照UDS
    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下诊断服务遍历测试')
    def test_caseid_1981463(self):
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x29, 0x00], ['7f2911', '7f2911'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x83, 0x00], ['7f8311', '7f8311'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x84, 0x00], ['7f8411', '7f8411'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x86, 0x00], ['7f8611', '7f8613'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x87, 0x00], ['7f8711', '7f8711'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x23, 0x00], ['7f2313', '7f2311'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x24, 0x00], ['7f2411', '7f2411'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x2c, 0x00], ['7f2c11', '7f2c11'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x2a, 0x00], ['7f2a11', '7f2a11'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x3d, 0x00], ['7f3d13', '7f3d11'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x35, 0x00], ['7f3511', '7f3513'])

    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下进入ProgrammingSession的条件检查_Pre-condition_ECU电压＜9V')  # 手动测试
    def test_caseid_1981310(self):
        pass

    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下进入ProgrammingSession的条件检查_Pre-condition_ECU电压＞16V')  # 手动测试
    def test_caseid_1981311(self):
        pass

    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')  # 切换会话，USAGMODE状态恢复，无法测试01会话下进BOOT
    @allure.title('01会话下进入ProgrammingSession的条件检查_Pre-condition_usgmod=Driving')
    def test_caseid_1981312(self):
        # try:
        #     with allure.step("切换usagmod=Driving"):
        #     #self.mix.init_boot_per()
        #     #self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','EpbStsEpbSts','EpbSts_AllAppld')
        # #self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU,0x0206,0x01,SESSION.DEFAULT,UnLock.L0,'','710102061001')
        # #with allure.step("车速设为100km/h"):
        #         self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
        #         self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #         self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','EpbStsEpbSts','EpbSts_AllAppld')
        #     #self.bus_comm.set_vehspd(100)# 车速>3km/h     # VehSpdLgtQf=2或3"
        #     #time.sleep(3)
        #     #self.check("bodycan", "CEMBodyFr13", 'PassExtrMirrAdjHmiReq', req, timeout=timeout)
        #     self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU,0x0206,0x01,SESSION.DEFAULT,UnLock.L0,'','710102061002')
        #     #self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'7f1022',check_method=Check_Method.response)
        # except Exception as e:
        #     logger.info(f'ERROR:{e}')
        #     assert False
        # finally:
        #     with allure.step("切换usgmod=ABANDONED"):
        #         self.sd_tester.change_usage_mode(UsageMode.ABANDONED)
        # #     self.bus_comm.set_vehspd(0)
        #     self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU,0x0206,0x01,SESSION.DEFAULT,UnLock.L0,'','710102061001')
        #     self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        pass

    # BGM_MPU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下进入ProgrammingSession的条件检查_Pre-condition_开启防火墙')
    def test_caseid_1981309(self):
        try:
            with allure.step("打开防火墙"):
                self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa040, 0x01, SESSION.EXTENDED, UnLock.L7, '0100',
                                                      '7101a040')
                self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb165, SESSION.EMPTY, '62b16501')
            self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0206, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3122')
            self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0206, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3122')
            # self.sd_tester.send_data_and_check(TA.BGM_SOC,'1002','7f1022')
        except Exception as e:
            logger.info(f'ERROR:{e}')
            assert False
        finally:
            self.sd_tester.close_fireware()
            self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0206, 0x01, SESSION.DEFAULT, UnLock.L0, '',
                                                  '710102061001')
            self.sd_tester.session_ctrl_and_check(TA.BGM_SOC, SESSION.PROGRAMMING, '62f18602')

    # #v1.1取消该判断条件 MS已删除
    # #BGM_MCU
    # @pytest.mark.smoke
    # @allure.story('基础诊断服务-New')
    # @allure.title('01会话下进入ProgrammingSession的条件检查_Pre-condition_防盗开启')#如何开启防盗
    # def test_caseid_1981308(self):
    #     # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,SESSION.PROGRAMMING,UnLock.L7,'0100','7101a04001',check_in=[0x01,0x02,0x03,0x11,0x12,0x13,0x21,0x22,0x23])
    #     # self.sd_tester.read_did_and_check(TA.BGM_MCU,0x42e5,SESSION.DEFAULT,'6242e5',check_in=[0x01,0x02])
    #     # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x0206,0x01,SESSION.DEFAULT,UnLock.L0,'','7101020602')
    #     # self.send_data_and_check(TA.BGM_MCU, [0x10, 0x02],'7f1022')
    #     # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,SESSION.PROGRAMMING,UnLock.L7,'0201','7101a04002',check_in=[0x01,0x02,0x03,0x11,0x12,0x13,0x21,0x22,0x23])
    #     # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x0206,0x01,SESSION.DEFAULT,UnLock.L0,'','7101020601')
    #     # self.send_data_and_check(TA.BGM_MCU, [0x10, 0x02],'5002')

    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下进入ProgrammingSession的条件检查_Pre-condition_Speed>3Km/h')
    def test_caseid_1981313(self):
        with allure.step("初始化环境成功进boot"):
            self.mix.init_boot_per()
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x0206,0x01,SESSION.DEFAULT,UnLock.L0,'','710102061001')
        # self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0206, 0x01, SESSION.DEFAULT, UnLock.L0, '', '710102061001')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.PROGRAMMING, '62f18602')
        self.sd_tester.exit_muc_boot()
        with allure.step("车速设为39.1km/h"):
            self.bus_comm.set_vehspd_and_qf(10000, VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
            time.sleep(1)
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x0206,0x01,SESSION.DEFAULT,UnLock.L0,'','710102061002')
        # self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'7f1022',check_method=Check_Method.response)
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0206, 0x01, SESSION.EMPTY, UnLock.L0, '', '710102061002')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, '1002', '7f1022')
        # with allure.step("初始化环境成功进boot"):
        #     self.mix.init_boot_per()
        # # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x0206,0x01,SESSION.DEFAULT,UnLock.L0,'','710102061001')
        # # self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU,0x0206,0x01,SESSION.DEFAULT,UnLock.L0,'','710102061001')
        # self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')


    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('01会话下进入ProgrammingSession的条件检查_无Pre-condition')
    def test_caseid_1981314(self):
        self.mix.init_boot_per()
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0206, 0x01, SESSION.DEFAULT, UnLock.L0, '', '710102061001')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.PROGRAMMING, '62f18602')

    # BGM_SOC,BGM_MCU切会话，usagemode就恢复inactive，02会话下切driving，没意义
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x10_NRC22测试')
    def test_caseid_1981434(self):
        pass

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x11_NRC22测试')
    def test_caseid_1981419(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa040, 0x01, SESSION.EXTENDED, UnLock.L7, '0100', '7101a040')
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb165, SESSION.EMPTY, '62b16501')
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC, SESSION.PROGRAMMING, '62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x11, 0x01], '7f1122')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.PROGRAMMING, '62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x11, 0x01], '7f1122')
        self.sd_tester.close_fireware()

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x22_NRC14测试')
    def test_caseid_1981356(self):
        # self.sd_tester.read_did_and_check([TA.BGM_MCU,TA.BGM_SOC],0xf190f1aaf1abed20f1a0,SESSION.PROGRAMMING,['7f2214','7f2214'])
        pass

    # BGM_SOC 需要没有写过d01c,D01C那边覆盖了
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x22_NRC22测试')
    def test_caseid_1981355(self):
        pass

    # BGM_MCU #BGM_S0C
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x2E_NRC31测试')
    def test_caseid_1981352(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EMPTY, UnLock.L5, check_data='6706')
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L5, check_data='6706')
        self.sd_tester.send_data_and_check([TA.BGM_SOC, TA.BGM_MCU], [0x2e, 0x00, 0x00, 0x00], ['7f2e31', '7f2e31'])
        self.sd_tester.send_data_and_check([TA.BGM_SOC, TA.BGM_MCU], [0x2e, 0xff, 0xff, 0xff], ['7f2e31', '7f2e31'])
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L11, check_data='6712')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2e, 0x00, 0x00, 0x00], '7f2e31')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2e, 0xff, 0xff, 0xff], '7f2e31')
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EMPTY, UnLock.L7, check_data='6708')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x2e, 0x00, 0x00, 0x00], '7f2e31')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x2e, 0xff, 0xff, 0xff], '7f2e31')


    # BGM_SOC,BGM_MCU 02会话下必须要退BOOT才可以切会话，切boot后，会变为默认会话
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下执行10 01')
    def test_caseid_1981458(self):
        # self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        # current_time = time.time()
        # self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x10,0x01],'5001')
        # second_time = time.time()
        # assert (second_time-current_time)<=0.2 or (second_time-current_time)<=5
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x10,0x01],'5001')
        second_time = time.time()
        assert (second_time-current_time)<=0.2 or (second_time-current_time)<=5
        self.sd_tester.send_data_and_check(TA.BGM_SOC,'22f186','62f18601')

    # BGM_SOC,BGM_MCU 02会话下需要退BOOT，不能直接进03
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下执行10 03')
    def test_caseid_1981452(self):
        # self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        # current_time = time.time()
        # self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x10,0x03],'5003')
        # second_time = time.time()
        # assert (second_time-current_time)<=0.2 or (second_time-current_time)<=5
        # self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        # current_time = time.time()
        # self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x10,0x03],'5003')
        # second_time = time.time()
        # assert (second_time-current_time)<=0.2 or (second_time-current_time)<=5
        pass

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下执行10 81')
    def test_caseid_1981455(self):
        # self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        # current_time = time.time()
        # data=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x10,0x81])
        # if data == '7f1078':
        #     second_time = time.time()
        #     assert  (second_time-current_time)<=5
        # else:
        #     assert True
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        current_time = time.time()
        data=self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x10,0x81])
        if data == '7f1078':
            second_time = time.time()
            assert  (second_time-current_time)<=5
        else:
            assert True
        self.sd_tester.send_data_and_check(TA.BGM_SOC,'22f186','62f18601')

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下执行10 83')
    def test_caseid_1981449(self):
        # self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        # current_time = time.time()
        # data=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x10,0x83])
        # if data == '7f1078':
        #     second_time = time.time()
        #     assert  (second_time-current_time)<=5
        # else:
        #     assert True
        # current_time = time.time()
        # self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x10,0x83])
        # if data == '7f1078':
        #     second_time = time.time()
        #     assert  (second_time-current_time)<=5
        # else:
        #     assert True
        pass

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x10_NRC12测试')
    def test_caseid_1981441(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x10, 0x11], ['7f1012', '7f1012'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x10, 0x22], ['7f1012', '7f1012'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x10, 0x33], ['7f1012', '7f1012'])

    # BGM_SOC,BGM_MCU SOC不做超出的判定，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x10_NRC13测试')
    def test_caseid_1981438(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x10], ['7f1013', '7f1013'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x10, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06], '7f1013')
        # self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x10,0x01,0x02,0x03,0x04,0x05,0x06],['7f1013','7f1013'])

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x10_NRC22测试')
    def test_caseid_1981435(self):
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x10, 0x02], '7f1022')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x02], '7f1022')
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        # pass

    # BGM_SOC,BGM_MCU  成功回负响应，但是BGM会异常断联，导致DOIP连不上
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x11_NRC12测试')
    def test_caseid_1981426(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x11, 0x11], ['7f1112', '7f1112'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x11, 0x51], ['7f1112', '7f1112'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x11, 0xff], ['7f1112', '7f1112'])

    #     pass

    # BGM_SOC,BGM_MCU SOC不对超过的长度做判定，会回正响应，提票,发11，也会导致doip断联
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x11_NRC13测试')
    def test_caseid_1981423(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x11], ['7f1113', '7f1113'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x11, 0x01, 0x01], '7f1113')
        # self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x11,0x01,0x01],['7f1113','7f1113'])

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x11_NRC22测试')
    def test_caseid_1981420(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa040, 0x01, SESSION.EXTENDED, UnLock.L7, '0100', '7101a040')
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb165, SESSION.EMPTY, '62b16501')
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x11, 0x01], ['7f1122', '7f1122'])
        self.sd_tester.close_fireware()

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x31_NRC13测试')
    def test_caseid_1981275(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x31], ['7f3113', '7f3113'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x31, 0x01], ['7f3113', '7f3113'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x31, 0x01, 0x02], ['7f3113', '7f3113'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x31, 0x01, 0x02, 0x06, 0x06], '7f3113')
        # self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x31,0x01,0x02,0x06,0x06],['7f3113','7f3113'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x31, 0x01, 0x20, 0xf2], '7f3113')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x31, 0x01, 0x20, 0xf2, 0xf2], '7f3113')

    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x14功能测试')
    def test_caseid_1981343(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff, 0xff, 0xff], '54')

    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x14测试')
    def test_caseid_1981346(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0x00, 0x00, 0x00], '7f1431')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff, 0xff, 0x00], '7f1431')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff, 0xff, 0x33], '7f1431')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff, 0xff, 0xd0], '7f1431')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x14测试_NRC13')
    def test_caseid_1981341(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14], '7f1413')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff], '7f1413')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x14, 0xff, 0xff], '7f1413')

    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x19_0x02测试')
    def test_caseid_1981335(self):
        self.mix.set_dtc_precontion()
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.send_dtc_request_and_return_check_status()

    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x19_0x04测试')
    def test_caseid_1981334(self):
        self.mix.set_dtc_precontion()
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x04, 0xf1, 0x17, 0x88, 0x20], '5904f11788')

    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x19_0x0a测试')
    def test_caseid_1981333(self):
        self.mix.set_dtc_precontion()
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x0a], '590a')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x19_NRC12测试')
    def test_caseid_1981328(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        for sv in range(0x00, 0xFF):
            if (sv == 0x02 or sv == 0x04 or sv == 0x0a or sv == 0x82 or sv == 0x84 or sv == 0x8a):
                continue
            else:
                self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, sv], '7f1912')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x19_NRC13测试')
    def test_caseid_1981326(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19], '7f1913')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x02], '7f1913')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x02, 0x7f, 0x00], '7f1913')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x04], '7f1913')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x04, 0xf1], '7f1913')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x04, 0xf1, 0x17, 0x88, 0x20, 0x00], '7f1913')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x0a, 0x00], '7f1913')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x19_NRC31测试')
    def test_caseid_1981324(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x04, 0xf1, 0x17, 0x88, 0x01], '7f1931')

    # BGM_SOC,BGM_MCU  1001在22f18601下回正响应，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x22_NRC13测试')
    def test_caseid_1981365(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.DEFAULT, ['62f18601', '62f18601'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x22], ['7f2213', '7f2213'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x22, 0xf1, 0x86, 0x01], '7f2213')
        # self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x22,0xf1,0x86,0x01],['7f2213','7f2213'])
        # pass

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x22_NRC14测试')
    def test_caseid_1981357(self):
        # self.sd_tester.read_did_and_check([TA.BGM_MCU,TA.BGM_SOC],0xf190f1aaf1abed20f1a0ed20ed20ed20,SESSION.EMPTY,['7f2214','7f2214'])
        pass

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x22_NRC31测试')
    def test_caseid_1981362(self):
        self.sd_tester.read_did_and_check([TA.BGM_MCU, TA.BGM_SOC], 0xffff, SESSION.EXTENDED, ['7f2231', '7f2231'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x22, 0x00, 0x00], ['7f2231', '7f2231'])

    # BGM_SOC
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x22_NRC33测试_1')
    def test_caseid_1981360(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb163, SESSION.EXTENDED, '7f2233')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x22_NRC33测试_2')
    def test_caseid_1981359(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x408f, SESSION.EXTENDED, '7f2233')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x43c4, SESSION.EXTENDED, '7f2233')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd12f, SESSION.EXTENDED, '7f2233')

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_NRC12测试')
    def test_caseid_1981415(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x27, 0x09], ['7f2712', '7f2712'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x27, 0x13], ['7f2712', '7f2712'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x27, 0xff], ['7f2712', '7f2712'])

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_NRC13测试')
    def test_caseid_1981413(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x27], ['7f2713', '7f2713'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x27, 0x05, 0x05], ['7f2713', '7f2713'])

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_NRC24测试')
    def test_caseid_1981411(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x04], '7f2724')
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x27, 0x06], ['7f2724', '7f2724'])
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x08], '7f2724')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x12], '7f2724')

    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_SecurityAccess功能测试_不同会话切换_L03')
    def test_caseid_1981379(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L3, check_data='6704')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x03], '6703000000')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.DEFAULT, '62f18601')
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L3, check_data='6704')

    # BGM_MCU BGM_SOC
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_SecurityAccess功能测试_不同会话切换_L05')
    def test_caseid_1981376(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5, check_data='6706')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x05], '6705000000')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.DEFAULT, '62f18601')
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5, check_data='6706')
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EXTENDED, UnLock.L5, check_data='6706')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x05], '6705000000')
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC, SESSION.DEFAULT, '62f18601')
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EXTENDED, UnLock.L5, check_data='6706')

    # BGM_SOC
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_SecurityAccess功能测试_不同会话切换_L07')
    def test_caseid_1981373(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EXTENDED, UnLock.L7)
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x07], '6707000000')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x01], '5001')
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EXTENDED, UnLock.L7)

    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_SecurityAccess功能测试_不同会话切换_L11')
    def test_caseid_1981370(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L11, check_data='6712')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x11], '6711000000')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.DEFAULT, '62f18601')
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L11, check_data='6712')

    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_SecurityAccess功能测试_其他安全请求切换_L03')
    def test_caseid_1981381(self):
        seed1 = self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L3, UnlockStep.seed,
                                                check_data='6703')[4:]
        seed2 = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x05], '6705')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_MCU, UnLock.L3, seed1)
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x04] + key1, '7f2724')

    # BGM_MCU BGM_SOC
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_SecurityAccess功能测试_其他安全请求切换_L05')
    def test_caseid_1981378(self):
        seed1 = self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5, UnlockStep.seed,
                                                check_data='6705')[4:]
        seed2 = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x03], '6703')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_MCU, UnLock.L5, seed1)
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x06] + key1, '7f2724')
        seed1 = self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EXTENDED, UnLock.L5, UnlockStep.seed,
                                                check_data='6705')[4:]
        seed2 = self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x03], '6703')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_SOC, UnLock.L5, seed1)
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x06] + key1, '7f2724')

    # BGM_SOC
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_SecurityAccess功能测试_其他安全请求切换_L07')
    def test_caseid_1981375(self):
        seed1 = self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EXTENDED, UnLock.L7, UnlockStep.seed,
                                                check_data='6707')[4:]
        seed2 = self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x05], '6705')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_SOC, UnLock.L7, seed1)
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x08] + key1, '7f2724')

    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_SecurityAccess功能测试_其他安全请求切换_L11')
    def test_caseid_1981372(self):
        seed1 = self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L11, UnlockStep.seed,
                                                check_data='6711')[4:0]
        seed2 = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x05], '6705')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_MCU, UnLock.L11, seed1)
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x12] + key1, '7f2724')

    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_SecurityAccess功能测试_相同会话切换_L03')
    def test_caseid_1981380(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L3, check_data='6704')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x03], '6703000000')
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L3, check_data='6704')

    # BGM_MCU BGM_SOC
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_SecurityAccess功能测试_相同会话切换_L05')
    def test_caseid_1981377(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5, check_data='6706')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x05], '6705000000')
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5, check_data='6706')
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EXTENDED, UnLock.L5, check_data='6706')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x05], '6705000000')
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EXTENDED, UnLock.L5, check_data='6706')

    # BGM_SOC
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_SecurityAccess功能测试_相同会话切换_L07')
    def test_caseid_1981374(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EXTENDED, UnLock.L7)
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x07], '6707000000')
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EXTENDED, UnLock.L7, check_data='6708')

    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27_SecurityAccess功能测试_相同会话切换_L11')
    def test_caseid_1981371(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L11, check_data='6712')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x11], '6711000000')
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L11, check_data='6712')

    # BGM_SOC,BGM_MCU S0C可以回2703的正响应
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x27服务测试')
    def test_caseid_1981417(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x27, 0x01], check_data=['7f277e', '7f277e'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x07], check_data='7f2712')
        # self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x27,0x03],check_data='7f2712')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x11], check_data='7f2712')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x28测试')
    def test_caseid_1981397(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x00, 0x01, SESSION.EMPTY, UnLock.L0, '6800')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x00, 0x02, SESSION.EMPTY, UnLock.L0, '6800')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x00, 0x03, SESSION.EMPTY, UnLock.L0, '6800')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x01, 0x01, SESSION.EMPTY, UnLock.L0, '6801')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x01, 0x02, SESSION.EMPTY, UnLock.L0, '6801')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x01, 0x03, SESSION.EMPTY, UnLock.L0, '6801')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x02, 0x01, SESSION.EMPTY, UnLock.L0, '6802')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x02, 0x02, SESSION.EMPTY, UnLock.L0, '6802')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x02, 0x03, SESSION.EMPTY, UnLock.L0, '6802')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x03, 0x01, SESSION.EMPTY, UnLock.L0, '6803')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x03, 0x02, SESSION.EMPTY, UnLock.L0, '6803')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x03, 0x03, SESSION.EMPTY, UnLock.L0, '6803')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x28测试-带正响应抑制')
    def test_caseid_1981396(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x80, 0x01, SESSION.EMPTY, UnLock.L0)
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x80, 0x02, SESSION.EMPTY, UnLock.L0)
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x80, 0x03, SESSION.EMPTY, UnLock.L0)
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x81, 0x01, SESSION.EMPTY, UnLock.L0)
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x81, 0x02, SESSION.EMPTY, UnLock.L0)
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x81, 0x03, SESSION.EMPTY, UnLock.L0)
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x82, 0x01, SESSION.EMPTY, UnLock.L0)
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x82, 0x02, SESSION.EMPTY, UnLock.L0)
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x82, 0x03, SESSION.EMPTY, UnLock.L0)
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x83, 0x01, SESSION.EMPTY, UnLock.L0)
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x83, 0x02, SESSION.EMPTY, UnLock.L0)
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x83, 0x03, SESSION.EMPTY, UnLock.L0)

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x2E_NRC13测试')
    def test_caseid_1981354(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L5, check_data='6706')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2e], '7f2e13')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2e, 0xdd, 0x01, 0x01], '7f2e13')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2e, 0xdd, 0x01, 0x01, 0x01], '7f2e13')
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L11, check_data='6712')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2e], '7f2e13')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2e, 0x40, 0xde, 0xde], '7f2e13')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2e, 0x40, 0xde, 0xde, 0xde], '7f2e13')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x2E_NRC33测试')
    def test_caseid_1981350(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.DEFAULT, '62f18601')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2e, 0xdd, 0x01, 0x00, 0x00, 0x00], '7f2e33')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2e, 0x42, 0x97, 0x00], '7f2e33')

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x31_NRC12测试')
    def test_caseid_1981279(self):
        self.sd_tester.routine_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], 0x0206, 0x10, SESSION.EXTENDED, UnLock.L0, '',
                                              ['7f3112', '7f3112'])

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x31_NRC31测试')
    def test_caseid_1981270(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.routine_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], 0xffff, 0x01, SESSION.EMPTY, UnLock.L0, '',
                                              ['7f3131', '7f3131'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x31, 0x01, 0x00, 0x00], ['7f3131', '7f3131'])

    # #BGM_SOC,BGM_MCU  SOC在03会话下34回正响应，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x34 0x00测试')
    def test_caseid_1981299(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC],
                                           [0x34, 0x00, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                           ['7f3411', '7f347f'])

    # BGM_SOC,BGM_MCU  SOC在03会话下34回正响应，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x34 0x10测试')
    def test_caseid_1981296(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC],
                                           [0x34, 0x10, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                           ['7f3411', '7f347f'])

    # BGM_SOC,BGM_MCUSOC在03会话下34回正响应，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x34 0x80测试')
    def test_caseid_1981293(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC],
                                           [0x34, 0x80, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                           ['7f3411', '7f347f'])

    # BGM_SOC,BGM_MCU SOC在03会话下34回正响应，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x36测试')
    def test_caseid_1981290(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x36, 0x01], ['7f3611', '7f3611'])

    # BGM_SOC,BGM_MCU  SOC在03会话下34回正响应，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x37测试')
    def test_caseid_1981286(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x37], ['7f3711', '7f3711'])

    # S3 Timer
    # BGM_SOC,BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x3E诊断会话维持时间测试')
    def test_caseid_1981268(self):
        self.sd_tester.sd_tester.stop_tester_present()
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        # self.sd_tester.enter_mcu_boot(reconnect=False)
        self.sd_tester.send_data_and_check(TA.BGM_MCU, '3e00', '7e00')
        time.sleep(4.9)
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x22, 0xf1, 0x86], '62f18603')
        time.sleep(5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x22, 0xf1, 0x86], '62f18601')
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC, SESSION.EXTENDED, '62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, '3e00', '7e00')
        time.sleep(16.6)
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x22, 0xf1, 0x86], '62f18603')
        time.sleep(16.8)
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x22, 0xf1, 0x86], '62f18601')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下0x85测试')
    def test_caseid_1981384(self):
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU, 0x01, SESSION.EXTENDED, UnLock.L0, 'c501')
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU, 0x02, SESSION.EMPTY, UnLock.L0, 'c502')
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU, 0x81, SESSION.EMPTY, UnLock.L0)
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU, 0x82, SESSION.EMPTY, UnLock.L0)

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下11 01复位测试')
    def test_caseid_1981432(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.hard_reset(TA.BGM_MCU)
        self.sd_tester.hard_reset(TA.BGM_SOC)

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下11 81复位测试')
    def test_caseid_1981430(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.reset_0x1181()

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下3E 00测试')
    def test_caseid_1981404(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x3e, 0x00], ['7e00', '7e00'])

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下3E 80测试')
    def test_caseid_1981402(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x3e, 0x80], ['', ''])

    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下DTC掩码测试')
    def test_caseid_1981322(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.send_dtc_request_and_return_check_status()

    # BGM_SOC,BGM_MCU 功能寻址没有接口做
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下功能寻址请求长度测试')
    def test_caseid_1981468(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.EXTENDED,['62f18603','62f18603'])
        self.sd_tester.send_data_and_check(TA.FUNCTION, '22f1aa',
                                           {'10 01': f'62f1aa{self.f1aa}', '10 02': f'62f1aa{self.f1aa}'})
        self.sd_tester.send_data_and_check(TA.FUNCTION, '22f1aaf1ab', {'10 01': f'62f1aa{self.f1aa}f1ab{self.f1ab}',
                                                                       '10 02': f'62f1aa{self.f1aa}f1ab{self.f1ab}'})
        self.sd_tester.send_data_and_check(TA.FUNCTION, '22f1aaf1abf18cf186', {'10 01': '62', '10 02': '62'})
        self.sd_tester.send_data_and_check(TA.BGM_MCU, '22f1aaf1abf18cf186f1aaf1abf18cf186f1aaf1ab', '62')

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下执行10 01')
    def test_caseid_1981459(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x10, 0x01], '5001')
        second_time = time.time()
        assert (second_time - current_time) <= 0.2 or (second_time - current_time) <= 5
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x01], '5001')
        second_time = time.time()
        assert (second_time - current_time) <= 0.2 or (second_time - current_time) <= 5

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下执行10 02')
    def test_caseid_1981447(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x10, 0x02], '5002')
        second_time = time.time()
        assert (second_time - current_time) <= 0.2 or (second_time - current_time) <= 5
        time.sleep(20)
        self.sd_tester.exit_muc_boot()
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x02], '5002')
        second_time = time.time()
        assert (second_time - current_time) <= 0.2 or (second_time - current_time) <= 5
        self.sd_tester.quit_boot()

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下执行10 03')
    def test_caseid_1981453(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x10, 0x03], '5003')
        second_time = time.time()
        assert (second_time - current_time) <= 0.2 or (second_time - current_time) <= 5
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x03], '5003')
        second_time = time.time()
        assert (second_time - current_time) <= 0.2 or (second_time - current_time) <= 5

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下执行10 81')
    def test_caseid_1981456(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        current_time = time.time()
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x10, 0x81])
        if data == '7f1078':
            second_time = time.time()
            assert (second_time - current_time) <= 5
        else:
            assert True
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x81])
        if data == '7f1078':
            second_time = time.time()
            assert (second_time - current_time) <= 5
        else:
            assert True

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下执行10 82')
    def test_caseid_1981444(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        current_time = time.time()
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x10, 0x82])
        if data == '7f1078':
            second_time = time.time()
            assert (second_time - current_time) <= 5
        else:
            assert True
        current_time = time.time()
        time.sleep(20)
        self.sd_tester.exit_muc_boot()
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x82])
        if data == '7f1078':
            second_time = time.time()
            assert (second_time - current_time) <= 5
        else:
            assert True
        self.sd_tester.quit_boot()

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下执行10 83')
    def test_caseid_1981450(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        current_time = time.time()
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x10, 0x83])
        if data == '7f1078':
            second_time = time.time()
            assert (second_time - current_time) <= 5
        else:
            assert True
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x83])
        if data == '7f1078':
            second_time = time.time()
            assert (second_time - current_time) <= 5
        else:
            assert True

    # 判断结果参照UDS
    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下诊断服务遍历测试')
    def test_caseid_1981462(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x29, 0x00], ['7f2911', '7f2911'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x83, 0x00], ['7f8311', '7f8311'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x84, 0x00], ['7f8411', '7f8411'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x86, 0x00], ['7f8611', '7f8613'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x87, 0x00], ['7f8711', '7f8711'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x23, 0x00], ['7f2313', '7f2311'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x24, 0x00], ['7f2411', '7f2411'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x2c, 0x00], ['7f2c11', '7f2c11'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x2a, 0x00], ['7f2a11', '7f2a11'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x3d, 0x00], ['7f3d13', '7f3d11'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x35, 0x00], ['7f3511', '7f3513'])

    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下进入ProgrammingSession的条件检查_Pre-condition_ECU电压＜9V')  # 手动测试
    def test_caseid_1981303(self):
        pass

    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下进入ProgrammingSession的条件检查_Pre-condition_ECU电压＞16V')  # 手动测试
    def test_caseid_1981304(self):
        pass

    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下进入ProgrammingSession的条件检查_Pre-condition_usgmod=Driving')
    def test_caseid_1981305(self):
        try:
            with allure.step("切换usagmod=Driving"):
                self.bus_comm.set('backbonefr', 'BcmVddmBackBoneFr00', 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
                self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0206, 0x01, SESSION.EMPTY, UnLock.L0, '',
                                                  '710102061002')
            self.sd_tester.send_data_and_check(TA.BGM_SOC, '1002', '7f1022')
            self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0206, 0x01, SESSION.EMPTY, UnLock.L0, '',
                                                  '710102061002')
            self.sd_tester.send_data_and_check(TA.BGM_MCU, '1002', '7f1022')
        except Exception as e:
            logger.info(f'ERROR:{e}')
            assert False
        finally:
            with allure.step("切换usgmod=ABANDONED"):
                self.sd_tester.change_usage_mode(UsageMode.ABANDONED)
            self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0206, 0x01, SESSION.EXTENDED, UnLock.L0, '',
                                                  '710102061001')
            self.sd_tester.session_ctrl_and_check(TA.BGM_SOC, SESSION.PROGRAMMING, '62f18602')
            self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0206, 0x01, SESSION.EXTENDED, UnLock.L0, '',
                                                  '710102061001')
            self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.PROGRAMMING, '62f18602')

    # BGM_MPU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下进入ProgrammingSession的条件检查_Pre-condition_开启防火墙')
    def test_caseid_1981302(self):
        try:
            with allure.step("打开防火墙"):
                self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa040, 0x01, SESSION.EXTENDED, UnLock.L7, '0100',
                                                      '7101a040')
                self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb165, SESSION.EMPTY, '62b16501')
            self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0206, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7f3122')
            # self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'7f1022',check_method=Check_Method.response)
        except Exception as e:
            logger.info(f'ERROR:{e}')
            assert False
        finally:
            self.sd_tester.close_fireware()
            self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0206, 0x01, SESSION.EXTENDED, UnLock.L0, '',
                                                  '710102061001')
            self.sd_tester.session_ctrl_and_check(TA.BGM_SOC, SESSION.PROGRAMMING, '62f18602')

    # #v1.1取消该判断条件
    # #BGM_MCU
    # @pytest.mark.smoke
    # @allure.story('基础诊断服务-New')
    # @allure.title('03会话下进入ProgrammingSession的条件检查_Pre-condition_防盗开启') MS已删除
    # def test_caseid_1981301(self):
    #     pass

    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('03会话下进入ProgrammingSession的条件检查_无Pre-condition')
    def test_caseid_1981307(self):
        self.mix.init_boot_per()
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0206, 0x01, SESSION.EXTENDED, UnLock.L0, '', '710102061001')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.PROGRAMMING, '62f18602')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x27_L03_NRC35_NRC36_NRC37测试')
    def test_caseid_1981410(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        seed1 = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x03], '6703')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_MCU, UnLock.L3, seed1)
        key1[-1] = (key1[-1] + 1) & 0xFF
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x04] + key1, '7f2735')
        seed1 = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x03], '6703')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_MCU, UnLock.L3, seed1)
        key1[-1] = (key1[-1] + 1) & 0xFF
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x04] + key1, '7f2736')
        time.sleep(9)
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x03], '7f2737')
        time.sleep(1)
        seed1 = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x03], '6703')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_MCU, UnLock.L3, seed1)
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x04] + key1, '6704')

    # BGM_MCU BGM_SOC
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x27_L05_NRC35_NRC36_NRC37测试')
    def test_caseid_1981409(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.DEFAULT, ['62f18601', '62f18601'])
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU, TA.BGM_SOC], SESSION.EXTENDED, ['62f18603', '62f18603'])
        seed1 = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x05], '6705')[4:]
        seed2 = self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x05], '6705')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_MCU, UnLock.L5, seed1)
        key2 = self.sd_tester.caculate_key(TA.BGM_SOC, UnLock.L5, seed2)
        key1[-1] = (key1[-1] + 1) & 0xFF
        key2[-1] = (key2[-1] + 1) & 0xFF
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x06] + key1, '7f2735')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x06] + key2, '7f2735')
        seed1 = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x05], '6705')[4:]
        seed2 = self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x05], '6705')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_MCU, UnLock.L5, seed1)
        key2 = self.sd_tester.caculate_key(TA.BGM_SOC, UnLock.L5, seed2)
        key1[-1] = (key1[-1] + 1) & 0xFF
        key2[-1] = (key2[-1] + 1) & 0xFF
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x06] + key1, '7f2736')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x06] + key2, '7f2736')
        time.sleep(9)
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x27, 0x05], ['7f2737', '7f2737'])
        time.sleep(1)
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L5,check_data='6706')
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EMPTY, UnLock.L5,check_data='6706')

    # BGM_SOC
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x27_L07_NRC35_NRC36_NRC37测试')
    def test_caseid_1981408(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC, SESSION.EXTENDED, '62f18603')
        seed1 = self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x07], '6707')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_SOC, UnLock.L7, seed1)
        key1[-1] = (key1[-1] + 1) & 0xFF
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x08] + key1, '7f2735')
        seed1 = self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x07], '6707')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_SOC, UnLock.L7, seed1)
        key1[-1] = (key1[-1] + 1) & 0xFF
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x08] + key1, '7f2736')
        time.sleep(9)
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x07], '7f2737')
        time.sleep(1)
        seed1 = self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x07], '6707')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_SOC, UnLock.L7, seed1)
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x08] + key1, '6708')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x27_L11_NRC35_NRC36_NRC37测试')
    def test_caseid_1981407(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        seed1 = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x11], '6711')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_MCU, UnLock.L11, seed1)
        key1[-1] = (key1[-1] + 1) & 0xFF
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x12] + key1, '7f2735')
        seed1 = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x11], '6711')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_MCU, UnLock.L11, seed1)
        key1[-1] = (key1[-1] + 1) & 0xFF
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x12] + key1, '7f2736')
        time.sleep(9)
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x11], '7f2737')
        time.sleep(1)
        seed1 = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x11], '6711')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_MCU, UnLock.L11, seed1)
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x12] + key1, '6712')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x28_0x00功能测试')
    def test_caseid_1981393(self):
        with allure.step(f"检查CAN应用报文: 0x114"):
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
            assert captured_msgdata1
        with allure.step(f"检查CAN网络管理报文: 0x533"):
            self.bus_comm.clear_bus_buffer("connectivitycanfd")
            captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
            assert captured_msgdata0
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x00, 0x01, SESSION.EXTENDED, UnLock.L0, '6800')
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1, '应用报文收发不正常'
        self.bus_comm.clear_bus_buffer("connectivitycanfd")
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0, '网络管理收发不正常'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x00, 0x02, SESSION.EXTENDED, UnLock.L0, '6800')
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1, '应用报文不正常'
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0, '网络管理收发不正常'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x00, 0x03, SESSION.EXTENDED, UnLock.L0, '6800')
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1, '应用报文收发不正常'
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0, '网络管理收发不正常'
        # pass

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x28_0x01功能测试')
    def test_caseid_1981391(self):
        with allure.step(f"检查CAN应用报文: 0x114"):
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
            assert captured_msgdata1
        with allure.step(f"检查CAN网络管理报文: 0x533"):
            self.bus_comm.clear_bus_buffer("connectivitycanfd")
            captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
            assert captured_msgdata0
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x01, 0x01, SESSION.EXTENDED, UnLock.L0, '6801')
        self.bus_comm.clear_bus_buffer("bodycan")
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1 is None, '应用报文发送正常'
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0, '网络管理收发不正常'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x01, 0x02, SESSION.EXTENDED, UnLock.L0, '6801')
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1, '应用报文不正常'
        self.bus_comm.clear_bus_buffer("connectivitycanfd")
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0 is None, '网络管理发送正常'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x01, 0x03, SESSION.EXTENDED, UnLock.L0, '6801')
        self.bus_comm.clear_bus_buffer("bodycan")
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1 is None, '应用报文发送正常'
        self.bus_comm.clear_bus_buffer("connectivitycanfd")
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0 is None, '网络管理发送正常'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x00, 0x03, SESSION.EXTENDED, UnLock.L0, '6800')

    # BGM_MCU 找到接收的信号,能发送但抑制接收
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x28_0x02功能测试')
    def test_caseid_1981389(self):
        with allure.step(f"检查BGM发送CAN应用报文: 0x114"):
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan",0x114,timeout=2)
            assert captured_msgdata1
        with allure.step(f"检查BGM接收CAN应用报文: 0x410"):
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",2)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",2)
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",3)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",3)
        with allure.step("抑制应用管理报文接收"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x02,0x01,SESSION.EXTENDED,UnLock.L0,'6802')
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",4)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",3)
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan",0x114,timeout=2)
            assert captured_msgdata1,'应用报文发送不正常'
            with allure.step(f"检查BGM发送CAN网络管理报文: 0x501"):
                self.bus_comm.clear_bus_buffer("bodycan")
                captured_msgdata0 = self.bus_comm.recv_pdu("bodycan", 0x501, timeout=2)
                assert captured_msgdata0,'网络管理报文发送不正常'
        with allure.step("使能应用报文和网络管理报文收发"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x00,0x03,SESSION.EXTENDED,UnLock.L0,'6800')
        #with allure.step("抑制网络管理报文收发"):BGM接收无法测试
        with allure.step("抑制应用报文和网络管理报文接收"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x02,0x03,SESSION.EXTENDED,UnLock.L0,'6802')
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",5)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",4)
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan",0x114,timeout=2)
            assert captured_msgdata1 ,'应用报文发不正常'
            with allure.step(f"检查BGM发送CAN网络管理报文: 0x501"):
                self.bus_comm.clear_bus_buffer("bodycan")
                captured_msgdata0 = self.bus_comm.recv_pdu("bodycan", 0x501, timeout=2)
                assert captured_msgdata0 ,'网络管理报文发送不正常'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x00,0x03,SESSION.EXTENDED,UnLock.L0,'6800')
    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x28_0x03功能测试')
    def test_caseid_1981387(self):
        with allure.step(f"检查BGM发送CAN应用报文: 0x114"):
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan",0x114,timeout=2)
            assert captured_msgdata1
        with allure.step(f"检查BGM接收CAN应用报文: 0x410"):
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",2)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",2)
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",3)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",3)
        with allure.step("抑制应用管理报文收发"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x03,0x01,SESSION.EXTENDED,UnLock.L0,'6803')
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",4)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",3)
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan",0x114,timeout=2)
            assert captured_msgdata1 is None,'应用报文发正常'
            with allure.step(f"检查BGM发送CAN网络管理报文: 0x501"):
                self.bus_comm.clear_bus_buffer("bodycan")
                captured_msgdata0 = self.bus_comm.recv_pdu("bodycan", 0x501, timeout=2)
                assert captured_msgdata0,'网络管理报文发送不正常'
        with allure.step("使能应用报文和网络管理报文收发"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x00,0x03,SESSION.EXTENDED,UnLock.L0,'6800')
        with allure.step("抑制网络管理报文收发"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x03,0x02,SESSION.EXTENDED,UnLock.L0,'6803')
            with allure.step(f"检查BGM发送CAN网络管理报文: 0x501"):
                self.bus_comm.clear_bus_buffer("bodycan")
                captured_msgdata0 = self.bus_comm.recv_pdu("bodycan", 0x501, timeout=2)
                assert captured_msgdata0 is None,'网络管理报文发送正常'
            with allure.step(f"检查BGM发送CAN应用报文: 0x114"):
                self.bus_comm.clear_bus_buffer("bodycan")
                captured_msgdata1 = self.bus_comm.recv_pdu("bodycan",0x114,timeout=2)
                assert captured_msgdata1
            with allure.step(f"检查BGM接收CAN应用报文: 0x410"):
                self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",2)
                self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",2)
                self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",3)
                self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",3)
        with allure.step("使能应用报文和网络管理报文收发"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x00,0x03,SESSION.EXTENDED,UnLock.L0,'6800')
        with allure.step("抑制应用报文和网络管理报文收发"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x03,0x03,SESSION.EXTENDED,UnLock.L0,'6803')
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",4)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",3)
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan",0x114,timeout=2)
            assert captured_msgdata1 is None,'应用报文发正常'
            with allure.step(f"检查BGM发送CAN网络管理报文: 0x501"):
                self.bus_comm.clear_bus_buffer("bodycan")
                captured_msgdata0 = self.bus_comm.recv_pdu("bodycan", 0x501, timeout=2)
                assert captured_msgdata0 is None,'网络管理报文发送正常'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x00,0x03,SESSION.EXTENDED,UnLock.L0,'6800')
    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x28_0x80功能测试')
    def test_caseid_1981392(self):
        with allure.step(f"检查CAN应用报文: 0x114"):
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
            assert captured_msgdata1
        with allure.step(f"检查CAN网络管理报文: 0x533"):
            self.bus_comm.clear_bus_buffer("connectivitycanfd")
            captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
            assert captured_msgdata0
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x80, 0x01, SESSION.EXTENDED, UnLock.L0)
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1, '应用报文收发不正常'
        self.bus_comm.clear_bus_buffer("connectivitycanfd")
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0, '网络管理收发不正常'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x80, 0x02, SESSION.EXTENDED, UnLock.L0)
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1, '应用报文收发不正常'
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0, '网络管理收发不正常'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x80, 0x03, SESSION.EXTENDED, UnLock.L0)
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1, '应用报文收发不正常'
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0, '网络管理收发不正常'

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x28_0x81功能测试')
    def test_caseid_1981390(self):
        with allure.step(f"检查CAN应用报文: 0x114"):
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
            assert captured_msgdata1
        with allure.step(f"检查CAN网络管理报文: 0x533"):
            self.bus_comm.clear_bus_buffer("connectivitycanfd")
            captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
            assert captured_msgdata0
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x81, 0x01, SESSION.EXTENDED, UnLock.L0)
        self.bus_comm.clear_bus_buffer("bodycan")
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1 is None, '应用报文发送正常'
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0, '网络管理收发不正常'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x81, 0x02, SESSION.EXTENDED, UnLock.L0)
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1, '应用报文不正常'
        self.bus_comm.clear_bus_buffer("connectivitycanfd")
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0 is None, '网络管理发送正常'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x81, 0x03, SESSION.EXTENDED, UnLock.L0)
        self.bus_comm.clear_bus_buffer("bodycan")
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1 is None, '应用报文发送正常'
        self.bus_comm.clear_bus_buffer("connectivitycanfd")
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0 is None, '网络管理发送正常'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x00,0x03,SESSION.EXTENDED,UnLock.L0,'6800')

    # BGM_MCU  找到接收的信号
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x28_0x82功能测试')
    def test_caseid_1981388(self):
        with allure.step(f"检查BGM发送CAN应用报文: 0x114"):
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan",0x114,timeout=2)
            assert captured_msgdata1
        with allure.step(f"检查BGM接收CAN应用报文: 0x410"):
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",2)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",2)
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",3)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",3)
        with allure.step("抑制应用管理报文接收"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x82,0x01,SESSION.EXTENDED,UnLock.L0)
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",4)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",3)
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan",0x114,timeout=2)
            assert captured_msgdata1,'应用报文发不正常'
            with allure.step(f"检查BGM发送CAN网络管理报文: 0x501"):
                self.bus_comm.clear_bus_buffer("bodycan")
                captured_msgdata0 = self.bus_comm.recv_pdu("bodycan", 0x501, timeout=2)
                assert captured_msgdata0,'网络管理报文发送不正常'
        with allure.step("使能应用报文和网络管理报文收发"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x80,0x03,SESSION.EXTENDED,UnLock.L0)
        #with allure.step("抑制网络管理报文收发"):BGM接收无法测试
        with allure.step("抑制应用报文和网络管理报文接收"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x82,0x03,SESSION.EXTENDED,UnLock.L0)
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",5)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",4)
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan",0x114,timeout=2)
            assert captured_msgdata1 ,'应用报文发不正常'
            with allure.step(f"检查BGM发送CAN网络管理报文: 0x501"):
                self.bus_comm.clear_bus_buffer("bodycan")
                captured_msgdata0 = self.bus_comm.recv_pdu("bodycan", 0x501, timeout=2)
                assert captured_msgdata0 ,'网络管理报文发送不正常'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x00,0x03,SESSION.EXTENDED,UnLock.L0,'6800')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x28_0x83功能测试')
    def test_caseid_1981386(self):
        with allure.step(f"检查BGM发送CAN应用报文: 0x114"):
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan",0x114,timeout=2)
            assert captured_msgdata1
        with allure.step(f"检查BGM接收CAN应用报文: 0x410"):
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",2)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",2)
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",3)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",3)
        with allure.step("抑制应用管理报文收发"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x83,0x01,SESSION.EXTENDED,UnLock.L0)
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",4)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",3)
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan",0x114,timeout=2)
            assert captured_msgdata1 is None,'应用报文发正常'
            with allure.step(f"检查BGM发送CAN网络管理报文: 0x501"):
                self.bus_comm.clear_bus_buffer("bodycan")
                captured_msgdata0 = self.bus_comm.recv_pdu("bodycan", 0x501, timeout=2)
                assert captured_msgdata0,'网络管理报文发送不正常'
        with allure.step("使能应用报文和网络管理报文收发"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x80,0x03,SESSION.EXTENDED,UnLock.L0)
        with allure.step("抑制网络管理报文收发"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x83,0x02,SESSION.EXTENDED,UnLock.L0)
            with allure.step(f"检查BGM发送CAN网络管理报文: 0x501"):
                self.bus_comm.clear_bus_buffer("bodycan")
                captured_msgdata0 = self.bus_comm.recv_pdu("bodycan", 0x501, timeout=2)
                assert captured_msgdata0 is None,'网络管理报文发送正常'
            with allure.step(f"检查BGM发送CAN应用报文: 0x114"):
                self.bus_comm.clear_bus_buffer("bodycan")
                captured_msgdata1 = self.bus_comm.recv_pdu("bodycan",0x114,timeout=2)
                assert captured_msgdata1
            with allure.step(f"检查BGM接收CAN应用报文: 0x410"):
                self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",2)
                self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",2)
                self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",3)
                self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",3)
        with allure.step("使能应用报文和网络管理报文收发"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x80,0x03,SESSION.EXTENDED,UnLock.L0)
        with allure.step("抑制应用报文和网络管理报文收发"):
            self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x83,0x03,SESSION.EXTENDED,UnLock.L0)
            self.bus_comm.set("adcanfd","AcuADCANFDFr12","ACUCoolantFlwReq",4)
            self.bus_comm.check("propulsioncan","BgmPropulsionFr04","ACUCoolantFlwReq",3)
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan",0x114,timeout=2)
            assert captured_msgdata1 is None,'应用报文发正常'
            with allure.step(f"检查BGM发送CAN网络管理报文: 0x501"):
                self.bus_comm.clear_bus_buffer("bodycan")
                captured_msgdata0 = self.bus_comm.recv_pdu("bodycan", 0x501, timeout=2)
                assert captured_msgdata0 is None,'网络管理报文发送正常'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x00,0x03,SESSION.EXTENDED,UnLock.L0,'6800')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x2F_NRC31测试')
    def test_caseid_1981283(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xffff, 0x03, SESSION.EMPTY, UnLock.L0, '', '7f2f31',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xffff, 0x00, SESSION.EMPTY, UnLock.L0, '', '7f2f31',
                                         check_method=Check_Method.response, recover=False)

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x2F_NRC33测试')
    def test_caseid_1981282(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4252, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '7f2f33',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x432e, 0x03, SESSION.EMPTY, UnLock.L0, '00', '7f2f33',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4252, 0x00, SESSION.EMPTY, UnLock.L0, '', '7f2f33',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x432e, 0x00, SESSION.EMPTY, UnLock.L0, '', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x2F_NRC7F测试')
    def test_caseid_1981281(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4252, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x432e, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4252, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x432e, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x2F测试_NRC13')
    def test_caseid_1981284(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2f], '7f2f13')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2f, 0x40], '7f2f13')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2f, 0x40, 0x00], '7f2f13')
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L3, check_data='6704')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2f], '7f2f13')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2f, 0x42], '7f2f13')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2f, 0x42, 0x00], '7f2f13')
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L5, check_data='6706')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2f], '7f2f13')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2f, 0x43], '7f2f13')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2f, 0x43, 0x00], '7f2f13')

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x31_NRC12测试_L05')
    def test_caseid_1981278(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L5, check_data='6706')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa051, 0x10, SESSION.EMPTY, UnLock.L0, '', '7f3112')
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EMPTY, UnLock.L5, check_data='6706')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x10, SESSION.EMPTY, UnLock.L0, '01', '7f3112')

    # BGM_SOC
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x31_NRC12测试_L07')
    def test_caseid_1981277(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EMPTY, UnLock.L7, check_data='6708')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa040, 0x10, SESSION.EMPTY, UnLock.L0, '01', '7f3112')

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x31_NRC13测试_L05')
    def test_caseid_1981274(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L5, check_data='6706')
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EMPTY, UnLock.L5, check_data='6706')
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x31], ['7f3113', '7f3113'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x31, 0x01], ['7f3113', '7f3113'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x31, 0x01, 0x20], ['7f3113', '7f3113'])
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x31, 0x01, 0x20, 0x40], '7f3113')

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x31_NRC13测试_L07')
    def test_caseid_1981273(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EMPTY, UnLock.L7, check_data='6708')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x31], '7f3113')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x31, 0x01], '7f3113')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x31, 0x01, 0xa0], '7f3113')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x31, 0x01, 0xa0, 0x40], '7f3113')

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x31_NRC22测试')
    def test_caseid_1981272(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa040, 0x01, SESSION.EXTENDED, UnLock.L7, '0100', '7101a040')
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb165, SESSION.EMPTY, '62b16501')
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x31, 0x01, 0x02, 0x06], ['7f3122', '7f3122'])
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L5, check_data='6706')
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EMPTY, UnLock.L5, check_data='6706')
        self.sd_tester.send_data_and_check([TA.BGM_MCU, TA.BGM_SOC], [0x31, 0x01, 0x02, 0x06], ['7f3122', '7f3122'])
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EMPTY, UnLock.L7, check_data='6708', )
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x31, 0x01, 0x02, 0x06], '7f3122')
        self.sd_tester.close_fireware()

    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x31_NRC33测试')
    def test_caseid_1981269(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_SOC,TA.BGM_MCU],SESSION.DEFAULT,['62F18601','62F18601'])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2030, 0x01, SESSION.EXTENDED, UnLock.L0, '01', '7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa051, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7f3133')


    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x85功能测试')
    def test_caseid_1981382(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_data_and_check(TA.BGM_MCU, '14ffffff', '54')
            # data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x08, 0x87, 0x20], [
            #                                       0x59, 0x04, 0xD1, 0x08, 0x87,0x00], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.send_data_and_check(TA.BGM_MCU, '8502', 'c502')
        with allure.step('制造当前故障;读取当前故障快照'):
            self.bus_comm.pause_ecu_send('bodycan', 'RPOD')
            time.sleep(3)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x08, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD1, 0x08, 0x87], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.send_data_and_check(TA.BGM_MCU, '8501', 'c501')
            time.sleep(3)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x08, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD1, 0x08, 0x87], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            self.bus_comm.resume_all_bus_send()
            time.sleep(2)
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x08, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD1, 0x08, 0x87], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
        # pass

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('11复位时0x28诊断功能变化')
    def test_caseid_1981318(self):
        with allure.step(f"检查CAN应用报文: 0x114"):
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=10)
            assert captured_msgdata1, f'BGM Tx应用报文已禁能,报文内容{captured_msgdata1}'
        with allure.step(f"检查CAN网络管理报文: 0x533"):
            self.bus_comm.clear_bus_buffer("connectivitycanfd")
            captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
            assert captured_msgdata0, f'BGM Tx网络报文已禁能,报文内容{captured_msgdata0}'
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x03, 0x03, SESSION.EXTENDED, UnLock.L0, '6803')
        self.bus_comm.clear_bus_buffer("bodycan")
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1 is None, '应用报文收发正常'
        self.bus_comm.clear_bus_buffer("connectivitycanfd")
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0 is None, '网络管理收发正常'
        self.sd_tester.reset_0x1181()
        with allure.step(f"检查CAN应用报文: 0x114"):
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
            assert captured_msgdata1, '应用报文收发不正常'
        with allure.step(f"检查CAN网络管理报文: 0x533"):
            self.bus_comm.clear_bus_buffer("connectivitycanfd")
            captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
            assert captured_msgdata0, '网络管理收发不正常'

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('11复位时0x85诊断功能变化')
    def test_caseid_1981316(self):
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU, 0x02, SESSION.EXTENDED, UnLock.L0, 'c502')
        self.sd_tester.reset_0x1181()
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x02, 0x09], '5902')
        # pass

    # BGM_SOC
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('ECU ability to receive requests')
    def test_caseid_1981465(self):
        self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xb302, SESSION.EXTENDED, UnLock.L5, '00', '6eb302',
                                           check_method=Check_Method.response, recover=False)
        start_time = time.time()
        while time.time() - start_time < 30:
            first_time = time.time()
            response = self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x2e, 0xb3, 0x02, 0x00])
            second_time = time.time()
            if response == '6eb302':
                if (second_time - first_time) <= 0.2:
                    continue
                else:
                    assert False
            else:
                if (second_time - first_time) <= 5:
                    continue
                else:
                    assert False

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('ECU ability to receive requests')
    def test_caseid_1981466(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4109, SESSION.EXTENDED, UnLock.L5, '00', '6e4109',
                                           check_method=Check_Method.response, recover=False)
        start_time = time.time()
        while time.time() - start_time < 60:
            first_time = time.time()
            response = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x2e, 0x41, 0x09, 0x00])
            second_time = time.time()
            if response == '6e4109':
                if (second_time - first_time) <= 2:
                    continue
                else:
                    assert False
            else:
                assert False

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('ECU Address Test')
    def test_caseid_1981470(self):
        pass

    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('不同诊断会话切换对写入的非易失性内存数据的影响')
    def test_caseid_1981315(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xf190, SESSION.EXTENDED, UnLock.L5, self.vin, '62f190',
                                           check_method=Check_Method.read, recover=False)
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.DEFAULT, '62f18601')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf190, SESSION.EMPTY, f'62f190{self.vin}')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf190, SESSION.EMPTY, f'62f190{self.vin}')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('不同诊断会话切换时0x28诊断功能变化')
    def test_caseid_1981321(self):
        with allure.step(f"检查CAN应用报文: 0x114"):
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
            assert captured_msgdata1
        with allure.step(f"检查CAN网络管理报文: 0x533"):
            self.bus_comm.clear_bus_buffer("connectivitycanfd")
            captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
            assert captured_msgdata0
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x03, 0x03, SESSION.EXTENDED, UnLock.L0, '6803')
        self.bus_comm.clear_bus_buffer("bodycan")
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1 is None, '应用报文收发正常'
        self.bus_comm.clear_bus_buffer("connectivitycanfd")
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0 is None, '网络管理收发正常'
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.DEFAULT, '62f18601')
        with allure.step(f"检查CAN应用报文: 0x114"):
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
            assert captured_msgdata1
        with allure.step(f"检查CAN网络管理报文: 0x533"):
            self.bus_comm.clear_bus_buffer("connectivitycanfd")
            captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
            assert captured_msgdata0

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('不同诊断会话切换时0x85诊断功能变化')
    def test_caseid_1981320(self):
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU, 0x02, SESSION.EXTENDED, UnLock.L0, 'c502')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.DEFAULT, '62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x02, 0x09], '5902')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('相同诊断会话切换时0x28诊断功能变化')
    def test_caseid_1981319(self):
        with allure.step(f"检查CAN应用报文: 0x114"):
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
            assert captured_msgdata1
        with allure.step(f"检查CAN网络管理报文: 0x533"):
            self.bus_comm.clear_bus_buffer("connectivitycanfd")
            captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
            assert captured_msgdata0
        self.sd_tester.communication_control_and_check(TA.BGM_MCU, 0x03, 0x03, SESSION.EXTENDED, UnLock.L0, '6803')
        self.bus_comm.clear_bus_buffer("bodycan")
        captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
        assert captured_msgdata1 is None, '应用报文收发正常'
        self.bus_comm.clear_bus_buffer("connectivitycanfd")
        captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
        assert captured_msgdata0 is None, '网络管理收发正常'
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        with allure.step(f"检查CAN应用报文: 0x114"):
            self.bus_comm.clear_bus_buffer("bodycan")
            captured_msgdata1 = self.bus_comm.recv_pdu("bodycan", 0x114, timeout=2)
            assert captured_msgdata1 is None, '应用报文收发正常'
        with allure.step(f"检查CAN网络管理报文: 0x533"):
            self.bus_comm.clear_bus_buffer("connectivitycanfd")
            captured_msgdata0 = self.bus_comm.recv_pdu("connectivitycanfd", 0x533, timeout=2)
            assert captured_msgdata0 is None, '网络管理收发正常'

    # BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('相同诊断会话切换时0x85诊断功能变化')
    def test_caseid_1981317(self):
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU, 0x02, SESSION.EXTENDED, UnLock.L0, 'c502')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.EXTENDED, '62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x19, 0x02, 0x09], '5902')



@allure.feature('BGM BaseTech/诊断功能/基础诊断')
class TestUdsServiceBoot(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("before_class")
        self.vin = self.sd_tester.get_vehicle_identification_number()
        self.f1aa = self.sd_tester.get_ecu_core_assembly_part_number()
        self.f1ab = self.sd_tester.get_ecu_delivery_assembly_part_number()
        with allure.step("初始化环境"):
            self.mix.init_boot_per()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.PROGRAMMING,['62f18602','62f18602'])
        # self.sd_tester.update_serverdoipid(0x1002)
        # self.sd_tester.enter_boot()
        # self.sd_tester.update_serverdoipid(0x1001)
        # self.sd_tester.send_request_and_recv_response([0x10,0x02],recv=[0x50,0x02])
        # self.sd_tester.send_request_and_recv_response([0x22, 0xf1,0x86], recv=[0x62, 0xf1,0x86,0x02])

    def after_each_func(self, ecu):

        super().after_each_func(ecu)

    def after_class(self, ecu):
        logger.info("after_class")

        super().after_class(self, ecu)
        self.sd_tester.exit_muc_boot()




    #BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x14测试')
    def test_caseid_1981345(self):
        # self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x14,0xff,0xff,0xff],'7f1411')

    #BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x19_0x02测试')
    def test_caseid_1981332(self):
        # self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x02,0x09],'7f1911')

    #BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x19_0x04测试')
    def test_caseid_1981331(self):
        # self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xf1,0x17,0x88,0x20],'7f1911')
    #BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x19_0x0a测试')
    def test_caseid_1981330(self):
        # self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x0a],'7f1911')


    #BGM_SOC,BGM_MCU 22f18601,1001回正响应提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x22_NRC13测试')
    def test_caseid_1981364(self):
        # self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.PROGRAMMING,['62f18602','62f18602'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x22],['7f2213','7f2213'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x22,0xf1,0x86,0x01],'7f2213')
        #self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x22,0xf1,0x86,0x01],['7f2213','7f2213'])
        #pass

    #BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x22_NRC31测试')
    def test_caseid_1981361(self):
        # self.sd_tester.read_did_and_check([TA.BGM_MCU,TA.BGM_SOC],0xffff,SESSION.PROGRAMMING,['7f2231','7f2231'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x22,0x00,0x00],['7f2231','7f2231'])

    #BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x27_NRC12测试')
    def test_caseid_1981414(self):
        # self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.PROGRAMMING,['62f18602','62f18602'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x27,0x09],['7f2712','7f2712'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x27,0x13],['7f2712','7f2712'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x27,0xff],['7f2712','7f2712'])


    #BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x27_NRC13测试')
    def test_caseid_1981412(self):
        # self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.PROGRAMMING,['62f18602','62f18602'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x27],['7f2713','7f2713'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x27,0x01,0x01],['7f2713','7f2713'])



    #BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x28测试-带正响应抑制')
    def test_caseid_1981394(self):
        # self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x80,0x01,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x80,0x02,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x80,0x03,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x81,0x01,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x81,0x02,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x81,0x03,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x82,0x01,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x82,0x02,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x82,0x03,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x83,0x01,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x83,0x02,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x83,0x03,SESSION.EMPTY,UnLock.L0,'7f2811')



    #BGM_SOC
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x2E_NRC33测试')
    def test_caseid_1981349(self):
        # self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x2e,0xf1,0x02,0x00],'7f2e33')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x2e,0xd0,0x1c,0x00],'7f2e33')


    #BGM_SOC,BGM_MCU 1001不过安全等级回正响应，提票 1002回负响应（这个票没提）
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x34 0x00测试')
    def test_caseid_1981298(self):
        # self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x34,0x00,0x44,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],'7f3433')
        # #self.sd_tester.exit_muc_boot()
        # #self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EMPTY,UnLock.L1,check_data='6702')
        # #self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x34,0x00,0x44,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],'743007d000')
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.EMPTY,UnLock.L1,check_data='6702')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x34,0x00,0x44,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],'743007d000')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x36,0x01],'76')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x37],'77')
        # self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        # self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x34,0x00,0x44,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],'7f3433')
        # self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EMPTY,UnLock.L1,check_data='6702')
        # self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x34,0x00,0x44,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],'743007d000')
    #     #pass

    #BGM_SOC,BGM_MCU 1001同样
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x34 0x10测试')
    def test_caseid_1981295(self):
        #self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x34,0x10,0x44,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],'743007d000')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x36,0x01],'76')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x37],'77')


    #BGM_SOC,BGM_MCU 1001同样
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x34 0x80测试')
    def test_caseid_1981292(self):
        #self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x34,0x80,0x44,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],'743007d000')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x36,0x01],'76')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x37],'77')
    #     pass



    #BGM_SOC,BGM_MCU 提过票了SOC偏差接受
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x36测试')
    def test_caseid_1981289(self):
        #self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.DEFAULT,['62f18601','62f18601'])
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x36,0x01],'7f3624')
        # self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        # self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x36,0x01,0x00],'7f3624')

    #BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x37测试')
    def test_caseid_1981285(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x37],'7f3724')
        # self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        # self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x37],'7f3724')

    #BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下11 01复位测试')
    def test_caseid_1981429(self):
        # self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.PROGRAMMING,['62f18602','62f18602'])
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.sd_tester.hard_reset(TA.BGM_MCU)

    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下执行10 82')
    def test_caseid_1981443(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.PROGRAMMING, '62f18602')
        current_time = time.time()
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x10, 0x82])
        if data == '7f1078':
            second_time = time.time()
            assert (second_time - current_time) <= 5
        else:
            assert True
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC, SESSION.PROGRAMMING, '62f18602')
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x10, 0x82])
        if data == '7f1078':
            second_time = time.time()
            assert (second_time - current_time) <= 5
        else:
            assert True
    #判断结果参照UDS
    #BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下诊断服务遍历测试')
    def test_caseid_1981461(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.PROGRAMMING,['62f18602','62f18602'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x29,0x00],['7f2911','7f2911'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x83,0x00],['7f8311','7f8311'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x84,0x00],['7f8411','7f8411'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x86,0x00],['7f8611','7f8613'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x87,0x00],['7f8711','7f8711'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x23,0x00],['7f2311','7f2311'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x24,0x00],['7f2411','7f2411'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x2c,0x00],['7f2c11','7f2c11'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x2a,0x00],['7f2a11','7f2a11'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x3d,0x00],['7f3d11','7f3d11'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x35,0x00],['7f3513','7f3513'])

        # BGM_MCU BGM_SOC

    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x27_SecurityAccess功能测试_不同会话切换_L01')
    def test_caseid_1981367(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.PROGRAMMING, UnLock.L1, check_data='6702')
        # self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EMPTY,UnLock.L1,UnlockStep.seed,check_data='6701000000')
        self.sd_tester.send_data_and_check(TA.BGM_MCU, [0x27, 0x01], '6701000000')
        # key1=self.sd_tester.caculate_key(UnLock.L1,seed1)
        # self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x27,0x02]+key1,'7f2735')
        self.sd_tester.exit_muc_boot()
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU, SESSION.DEFAULT, '62f18601')
        # self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.PROGRAMMING, UnLock.L1, check_data='6702')
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.PROGRAMMING, UnLock.L1, check_data='6702')
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x01], '6701000000')
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC, SESSION.DEFAULT, '62f18601')
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.PROGRAMMING, UnLock.L1, check_data='6702')
        # data=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x27,0x01],'6701')
        # seed1=self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,UnLock.L1,UnlockStep.seed,check_data='6701')[4:]
        # key1=self.sd_tester.caculate_key(UnLock.L1,seed1)
        # self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x27,0x02,key1],'7f27')

        # if data == '6701000000':
        #     logger.info('已经解锁')
        #     assert False
        # else:
        #     logger.info('未解锁')

    #BGM_MCU BGM_SOC
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x27_SecurityAccess功能测试_其他安全请求切换_L01')
    def test_caseid_1981369(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.DEFAULT,'62f18601')
        seed1=self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,UnLock.L1,UnlockStep.seed,check_data='6701')
        seed2=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x27,0x01],'6701')[4:]
        key1=self.sd_tester.caculate_key(TA.BGM_MCU,UnLock.L1,seed1)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x27,0x02]+key1,'7f2735')
        seed1=self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,UnLock.L1,UnlockStep.seed,check_data='6701')
        seed2=self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x27,0x01],'6701')[4:]
        key1=self.sd_tester.caculate_key(TA.BGM_SOC,UnLock.L1,seed1)
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x27,0x02]+key1,'7f2735')


    #BGM_MCU BGM_SOC
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x27_SecurityAccess功能测试_相同会话切换_L01')
    def test_caseid_1981368(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x27,0x01],'6701000000')
        self.sd_tester.exit_muc_boot()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x27,0x01],'6701000000')
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')



    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('0x27_L01_NRC35_NRC36_NRC37测试')
    def test_caseid_1981406(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC, SESSION.PROGRAMMING, '62f18602')
        seed1 = self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x01], '6701')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_SOC, UnLock.L1, seed1)
        key1[-1] = (key1[-1] + 1) & 0xFF
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x02] + key1, '7f2735')
        seed1 = self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x01], '6701')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_SOC, UnLock.L1, seed1)
        key1[-1] = (key1[-1] + 1) & 0xFF
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x02] + key1, '7f2736')
        time.sleep(9)
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x01], '7f2737')
        time.sleep(1)
        seed1 = self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x01], '6701')[4:]
        key1 = self.sd_tester.caculate_key(TA.BGM_SOC, UnLock.L1, seed1)
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x27, 0x02] + key1, '6702')

        # BGM_MCU


    #BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x10_NRC12测试')
    def test_caseid_1981440(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.PROGRAMMING,['62f18602','62f18602'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x10,0x11],['7f1012','7f1012'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x10,0x22],['7f1012','7f1012'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x10,0x33],['7f1012','7f1012'])



    #BGM_SOC,BGM_MCU 1001没有做超出长度的判定，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x10_NRC13测试')
    def test_caseid_1981437(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.PROGRAMMING,['62f18602','62f18602'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x10],['7f1013','7f1013'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x10,0x01,0x02,0x03,0x04,0x05,0x06],'7f1013')
        #self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x10,0x01,0x02,0x03,0x04,0x05,0x06],['7f1013','7f1013'])


    #BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x11_NRC12测试')
    def test_caseid_1981425(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.PROGRAMMING,['62f18602','62f18602'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x11,0x11],['7f1112','7f1112'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x11,0x51],['7f1112','7f1112'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x11,0xff],['7f1112','7f1112'])


    #BGM_SOC,BGM_MCU 1001没有做超出长度的判定，提票
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x11_NRC13测试')
    def test_caseid_1981422(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.PROGRAMMING,['62f18602','62f18602'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x11],['7f1113','7f1113'])
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x11,0x01,0x01],'7f1113')
        #self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x11,0x01,0x01],['7f1113','7f1113'])


    #BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x27服务测试')
    def test_caseid_1981416(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x27,0x03],check_data='7f2712')
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x27,0x05],check_data=['7f2712','7f277e'])
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x27,0x07],check_data='7f277e')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x27,0x11],check_data='7f2712')


    #BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x28测试')
    def test_caseid_1981395(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x00,0x01,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x00,0x02,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x00,0x03,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x01,0x01,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x01,0x02,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x01,0x03,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x02,0x01,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x02,0x02,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x02,0x03,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x03,0x01,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x03,0x02,SESSION.EMPTY,UnLock.L0,'7f2811')
        self.sd_tester.communication_control_and_check(TA.BGM_MCU,0x03,0x03,SESSION.EMPTY,UnLock.L0,'7f2811')


    #BGM_SOC
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x2E_NRC13测试')
    def test_caseid_1981353(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.EMPTY,UnLock.L1,check_data='6702')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x2e],'7f2e13')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x2e,0xf1,0x02,0x02],'7f2e13')
        #pass

    #BGM_SOC
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x2E_NRC31测试')
    def test_caseid_1981351(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.EMPTY,UnLock.L1,check_data='6702')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x2e,0x00,0x00,0x00],'7f2e31')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x2e,0xff,0xff,0xff],'7f2e31')
        #pass


    #BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x85测试')
    def test_caseid_1981383(self):
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU,0x01,SESSION.PROGRAMMING,UnLock.L0,'7f8511')
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU,0x02,SESSION.EMPTY,UnLock.L0,'7f8511')
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU,0x81,SESSION.EMPTY,UnLock.L0,'7f8511')
        self.sd_tester.control_dtc_setting_and_check(TA.BGM_MCU,0x82,SESSION.EMPTY,UnLock.L0,'7f8511')


    #BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下11 81复位测试')
    def test_caseid_1981428(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.PROGRAMMING,['62f18602','62f18602'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x11,0x81],['',''])
        time.sleep(15)


    #BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下3E 00测试')
    def test_caseid_1981401(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.PROGRAMMING,['62f18602','62f18602'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x3e,0x00],['7e00','7e00'])



    #BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下3E 80测试')
    def test_caseid_1981400(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.PROGRAMMING,['62f18602','62f18602'])
        self.sd_tester.send_data_and_check([TA.BGM_MCU,TA.BGM_SOC],[0x3e,0x80],['',''])


    #BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下ECU ability to receive requests')
    def test_caseid_1981464(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x3e,0x00],'7e00')
        start_time = time.time()
        while time.time() - start_time < 30:
            first_time = time.time()
            response = self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x3e,0x00])
            second_time = time.time()
            if response == '7e00':
                if (second_time-first_time) <=0.2:
                    continue
                else:
                    assert False,'P2_sever超过200MS'
            else:
                if (second_time-first_time) <=5:
                    continue
                else:
                    assert False,'P2*_sever超过5000MS'
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x3e,0x00],'7e00')
        start_time = time.time()
        while time.time() - start_time < 100:
            first_time = time.time()
            response = self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x3e,0x00])
            second_time = time.time()
            if response == '7e00':
                if (second_time-first_time) <=0.2:
                    continue
                else:
                    assert False,'P2_sever超过200MS'
            else:
                if (second_time-first_time) <=5:
                    continue
                else:
                    assert False,'P2*_sever超过5000MS'


    #BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下执行10 02')
    def test_caseid_1981446(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x10,0x02],'5002')
        second_time = time.time()
        assert (second_time-current_time)<=0.2 or (second_time-current_time)<=5
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        current_time = time.time()
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x10,0x02],'5002')
        second_time = time.time()
        assert (second_time-current_time)<=0.2 or (second_time-current_time)<=5
        #pass

    @pytest.mark.full
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下功能寻址请求长度测试')
    def test_caseid_1981467(self):
        self.sd_tester.session_ctrl_and_check([TA.BGM_MCU,TA.BGM_SOC],SESSION.PROGRAMMING,['62f18602','62f18602'])
        self.sd_tester.send_data_and_check(TA.FUNCTION, '22f1aa',
                                           {'10 01': f'62f1aa{self.f1aa}', '10 02': f'62f1aa{self.f1aa}'})
        self.sd_tester.send_data_and_check(TA.FUNCTION, '22f1aaf1ab', {'10 01': f'62f1aa{self.f1aa}f1ab{self.f1ab}',
                                                                       '10 02': f'62f1aa{self.f1aa}f1ab{self.f1ab}'})
        self.sd_tester.send_data_and_check(TA.FUNCTION, '22f1aaf1abf18cf186', {'10 01': '62', '10 02': '62'})
        self.sd_tester.send_data_and_check(TA.BGM_MCU, '22f1aaf1abf18cf186f1aa', '62')
        

    #S3 Timer
    #BGM_SOC,BGM_MCU
    @pytest.mark.smoke
    @allure.story('基础诊断服务-New')
    @allure.title('02会话下0x3E诊断会话维持时间测试')
    def test_caseid_1981267(self):
        #self.sd_tester.sd_tester.stop_tester_present()
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.PROGRAMMING,'62f18602')
        #self.sd_tester.sd_tester.stop_tester_present()
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'3e00','7e00')
        self.sd_tester.sd_tester.stop_tester_present()
        time.sleep(15)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x22,0xf1,0x86],'62f18602')
        # time.sleep(17.2)
        # self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x22,0xf1,0x86],'62f18601')
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.sd_tester.stop_tester_present()
        self.sd_tester.send_data_and_check(TA.BGM_SOC,'3e00','7e00')
        self.sd_tester.sd_tester.stop_tester_present()
        time.sleep(14)
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x22,0xf1,0x86],'62f18602')
        # time.sleep(21)
        # self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x22,0xf1,0x86],'62f18601')
        self.sd_tester.sd_tester.tester_present()
        self.sd_tester.send_data_and_check(TA.BGM_SOC,'1001','5001')
        time.sleep(1)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'1181')
        time.sleep(20)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22f186','62f18601')
    # BGM_SOC,BGM_MCU 功能寻址底层逻辑没写好

        #pytest BaseTech/DiagFlash/test_diag_bgm_udsservice.py::TestUdsServiceBoot::test_caseid_1981267
#pytest BaseTech/DiagFlash/test_diag_bgm_udsservice.py::TestUdsServiceApp::test_caseid_1981467