import os
import sys
import pytest
import allure
import threading
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
import copy
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from framework.automotive.utils.data_type import EcuInfo
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common import *
running_flag = True


@allure.feature("标定")
@allure.story("胎压标定")
class TestTPMS(TestABCBase):
    def change_bench_config(ecu:EcuInfo) -> EcuInfo:
        ecu.domain.single_bgm = True
        ecu.domain.two_domain = False
        ecu.tc_config["dut_ecu"] = ["BGM"]
        return ecu
    def before_class(self, ecu):
        global running_flag
        self.soa.update(["TyreService_client"])
        self.io.tcam_power_off()
        sleep(2)
        self.sd_tester.write_ccp(ccp={225: 7, 226: 7, 19: 5})
        self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)
        self.bus_comm.pause_bus_send_tpms()
        self.tire_sensor_dic = self.bus_comm.tire_sensor_ini()
        self.rolling_counter = 0
        running_flag = True
        self.sd_tester.write_sensor_id(
            [0x11, 0x11, 0x11, 0x11, 0x02, 0x62, 0x86, 0x43, 0x02, 0x62, 0x84, 0xF4, 0x22, 0x22, 0x22, 0x22])
        self.start_send_tire_data_main(self)

    def before_each_func(self, ecu):
        self.tire_sensor_dic["FrontLeft"]["send_rf"] = True
        self.tire_sensor_dic["FrontRight"]["send_rf"] = True
        self.tire_sensor_dic["RearRight"]["send_rf"] = True
        self.tire_sensor_dic["RearLeft"]["send_rf"] = True
        time.sleep(3)
        self.bus_comm.set_dtc_pre()
        time.sleep(1)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_vehspd_and_qf(vehspd=9.0)
        self.bus_comm.set_AmbTEstimd_and_qf(AmbTEstimd=37.0)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.All, temperature=47, time_wait=0)
        time.sleep(3)

    def after_each_func(self, ecu):
        try:
            self.sd_tester.write_sensor_id(
                [0x11, 0x11, 0x11, 0x11, 0x02, 0x62, 0x86, 0x43, 0x02, 0x62, 0x84, 0xF4, 0x22, 0x22, 0x22, 0x22])
            self.bus_comm.set_vehspd_gear(vehspd=0.0)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        

    def after_class(self, ecu):
        self.io.tcam_power_on()
        global running_flag
        running_flag = False
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        self.sd_tester.write_ccp({225: 7, 226: 7})  # 260kpa
        pass
    

    def generate_and_send_rf_data(self, pos):
        """
        发送胎压数据
        :param pos: FrontLeft：左前；FrontRight：右前；RearRight：右后；RearLeft左后
        :return:
        """
        global running_flag
        st = time.time()
        running_flag = True
        while running_flag:
            sensor = self.tire_sensor_dic[pos]
            while time.time() - st < sensor["cycle_time"]:
                time.sleep(0.1)
            if sensor["send_rf"]:
                for _ in range(sensor["counter_per_pkg"]):
                    rf_data = sensor["tire_id"] + [math.ceil(sensor["pressure"] / 1.373), int(sensor["temp"] + 50),
                                                   sensor["acc"], sensor["factory"], sensor["function"]]
                    
                    self.bus_comm.send_tpms_rf_data(rf_data, self.rolling_counter)
                    self.rolling_counter = (self.rolling_counter + 1) & 0xFF
                    sleep(0.12)
            st = time.time()

    def start_send_tire_data_main(self, tire_dic: list = ["FrontLeft", "FrontRight", "RearRight", "RearLeft"]):
        """
        启动进程发送胎压数据报文
        :param tire_dic: 需要发送的胎压数据列表
        :return:
        """
        global running_flag
        logger.info(f"------->开始胎压报文发送")
        for key in tire_dic:
            send_data_thread = threading.Thread(target=self.generate_and_send_rf_data, args=(self, key,),name="start_class")
            send_data_thread.start()
            sleep(.5)
    
    def start_send_tire_data(self, tire_dic: list = ["FrontLeft", "FrontRight", "RearRight", "RearLeft"]):
        """
        启动进程发送胎压数据报文
        :param tire_dic: 需要发送的胎压数据列表
        :return:
        """
        global running_flag
        logger.info(f"------->开始胎压报文发送")
        for key in tire_dic:
            send_data_thread = threading.Thread(target=self.generate_and_send_rf_data, args=(key,),name="start_function")
            send_data_thread.start()
            sleep(.5)


    def stop_send_tire_data(self):
        """
        停止胎压报文发送
        :return:
        """
        global running_flag
        running_flag = False

    @pytest.mark.full
    def test_tpms_caseid_1995302(self):
        '''欧标下右后胎压低报警产生恢复_低于83%prec'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=215,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_tpms_caseid_1995301(self):
        '''欧标下左后胎压低报警产生恢复_低于83%prec'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=215,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_tpms_caseid_1995300(self):
        '''欧标下右前胎压低报警产生恢复_低于83%prec'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=215,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.sanity
    def test_tpms_caseid_1995299(self):
        '''欧标下左前胎压低报警产生恢复_低于83%prec'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=215,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.sanity
    def test_tpms_caseid_1995259(self):
        '''欧标下左前胎压低报警产生恢复_低于88%prec'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=239,
                                        time_wait=485)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.sanity
    def test_tpms_caseid_1995258(self):
        '''欧标下左前胎压低报警产生恢复_低于80%pwarm'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=217,
                                        time_wait=245)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.sanity
    def test_tpms_caseid_1995257(self):
        '''欧标下左前胎压低报警产生恢复_低于150kpa'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=149,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_tpms_caseid_1995256(self):
        '''欧标下右前胎压低报警产生恢复_低于88%prec'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=239,
                                        time_wait=485)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_tpms_caseid_1995255(self):
        '''欧标下右前胎压低报警产生恢复_低于80%pwarm'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=217,
                                        time_wait=245)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_tpms_caseid_1995254(self):
        '''欧标下右前胎压低报警产生恢复_低于150kpa'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=149,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_tpms_caseid_1995253(self):
        '''欧标下左后胎压低报警产生恢复_低于88%prec'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=239,
                                        time_wait=485)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_tpms_caseid_1995252(self):
        '''欧标下左后胎压低报警产生恢复_低于80%pwarm'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=217,
                                        time_wait=245)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_tpms_caseid_1995251(self):
        '''欧标下左后胎压低报警产生恢复_低于150kpa'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=149,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_tpms_caseid_1995250(self):
        '''欧标下右后胎压低报警产生恢复_低于88%prec'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=239,
                                        time_wait=485)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_tpms_caseid_1995249(self):
        '''欧标下右后胎压低报警产生恢复_低于80%pwarm'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=217,
                                        time_wait=245)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_tpms_caseid_1995248(self):
        '''欧标下右后胎压低报警产生恢复_低于150kpa'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=149,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=255,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_tpms_caseid_1995247(self):
        '''欧标下低速四轮胎压低报警无法产生_低于88%Pwarm'''
        self.bus_comm.set_vehspd_and_qf(vehspd=8.0)
        time.sleep(1)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.All, pressure=239,
                                        time_wait=485)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_tpms_caseid_1995246(self):
        '''欧标下低速四轮胎压低报警无法产生_低于88%Pwarm'''
        self.bus_comm.set_vehspd_and_qf(vehspd=8.0)
        time.sleep(1)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.All, pressure=217,
                                        time_wait=245)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    
    
    
    
    