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
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from framework.automotive.utils.data_type import EcuInfo
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common import *
running_flag = True


@allure.feature("标定")
@allure.story("胎压标定")
class TestTPMS(TestABCBase):
    @staticmethod
    def change_bench_config(ecu:EcuInfo) -> EcuInfo:
        ecu.domain.single_bgm = True
        ecu.domain.two_domain = False
        ecu.tc_config["dut_ecu"] = ["BGM"]
        return ecu
    def before_class(self, ecu):
        self.io.tcam_power_off()
        global running_flag
        self.soa.update(["TyreService_client", "WTIService_client"])
        sleep(2)
        self.sd_tester.write_ccp(ccp={225: 4, 226: 4, 19: 6})
        self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)
        self.bus_comm.pause_bus_send_tpms()
        self.tire_sensor_dic = self.bus_comm.tire_sensor_ini()
        self.rolling_counter = 0
        running_flag = True
        self.sd_tester.write_sensor_id(
            [0x11, 0x11, 0x11, 0x11, 0x02, 0x62, 0x86, 0x43, 0x02, 0x62, 0x84, 0xF4, 0x22, 0x22, 0x22, 0x22])
        self.start_send_tire_data_main(self)

    def before_each_func(self, ecu):
        # self.tire_sensor_dic = self.bus_comm.tire_sensor_ini()
        self.tire_sensor_dic["FrontLeft"]["send_rf"] = True
        self.tire_sensor_dic["FrontRight"]["send_rf"] = True
        self.tire_sensor_dic["RearRight"]["send_rf"] = True
        self.tire_sensor_dic["RearLeft"]["send_rf"] = True
        time.sleep(3)

        self.bus_comm.set_dtc_pre()
        time.sleep(1)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_vehspd_and_qf(vehspd=37.0)
        time.sleep(1)

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

    @allure.title("左前轮胎胎压低一级警告信息(MsgTireFLPressureLowLevel1)_告警产生恢复")
    @pytest.mark.sanity
    def test_caseid_1981928(self):
        '''左前轮 胎压低压报警'''
        hint = "Front Left Tire Pressure Low Level 1"
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=178,
                                        time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=230,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @allure.title("右前轮胎胎压低一级警告信息(MsgTireFLPressureLowLevel1)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_1981927(self):
        hint = "Front Right Tire Pressure Low Level 1"
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=178,
                                        time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=230,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @allure.title("左后轮胎胎压低一级警告信息(MsgTireFLPressureLowLevel1)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_1981926(self):
        hint = "Rear Left Tire Pressure Low Level 1"
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=178,
                                        time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=230,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @allure.title("右后轮胎胎压低一级警告信息(MsgTireFLPressureLowLevel1)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_1981925(self):
        hint = "Rear Right Tire Pressure Low Level 1"
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=178,
                                        time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=230,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @allure.title("左前轮胎胎压低二级警告信息(MsgTireFLPressureLowLevel2)_告警产生恢复")
    @pytest.mark.sanity
    def test_caseid_1981924(self):
        hint = "Front Left Tire Pressure Low Level 2"
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=138,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=230,
                                        time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")

    
    @allure.title("右前轮胎胎压低二级警告信息(MsgTireFLPressureLowLevel2)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_1981923(self):
        hint = "Front Right Tire Pressure Low Level 2"
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=138,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=230,
                                        time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @allure.title("左后轮胎胎压低二级警告信息(MsgTireFLPressureLowLevel2)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_1981922(self):
        hint = "Rear Left Tire Pressure Low Level 2"
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=138,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=230,
                                        time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @allure.title("右后轮胎胎压低二级警告信息(MsgTireFLPressureLowLevel2)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_1981921(self):
        hint = "Rear Right Tire Pressure Low Level 2"
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=138,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=230,
                                        time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.sanity
    def test_caseid_1981920(self):
        '''左前胎温高告警'''
        hint = "Front Left Tire Temperature High"
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, temperature=86, time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, temperature=79, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.full
    def test_caseid_1981919(self):
        '''右前胎温高告警'''
        hint = "Front Right Tire Temperature High"
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, temperature=86, time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, temperature=79, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.full
    def test_caseid_1981918(self):
        '''左后胎温高告警'''
        hint = "Rear Left Tire Temperature High"
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, temperature=86, time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, temperature=79, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.full
    def test_caseid_1981917(self):
        '''右后胎温高告警'''
        hint = "Rear Right Tire Temperature High"
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, temperature=86, time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, temperature=79, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.sanity
    def test_caseid_1981916(self):
        '''左前快速漏气'''
        hint = "Front Left Tire Pressure Fast Lost"
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=340,
                                        time_wait=20)
        for i in range(18):
            self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=340-10*i,
                                        time_wait=5)
        #检查总线报出异常
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        time.sleep(90)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=260,
                                        time_wait=5)
    
    @pytest.mark.full
    def test_caseid_1981915(self):
        '''右前快速漏气'''
        hint = "Front Right Tire Pressure Fast Lost"
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=340,
                                        time_wait=20)
        for i in range(18):
            self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=340-10*i,
                                        time_wait=5)
        #检查总线报出异常
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        time.sleep(90)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=260,
                                        time_wait=5)
    
    @pytest.mark.full
    def test_caseid_1981914(self):
        '''左后快速漏气'''
        hint = "Rear Left Tire Pressure Fast Lost"
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=340,
                                        time_wait=20)
        for i in range(18):
            self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=340-10*i,
                                        time_wait=5)
        #检查总线报出异常
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        time.sleep(90)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=260,
                                        time_wait=5)
    
    @pytest.mark.full
    def test_caseid_1981913(self):
        '''右后快速漏气'''
        hint = "Rear Right Tire Pressure Fast Lost"
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=340,
                                        time_wait=20)
        for i in range(18):
            self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=340-10*i,
                                        time_wait=5)
        #检查总线报出异常
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        time.sleep(90)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=260,
                                        time_wait=5)
    
    @pytest.mark.sanity
    def test_caseid_1981912(self):
        '''左前轮低电量'''
        #设置电压12v
        hint = "Front Left Tire Sensor Batt Low"
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, factory=18, time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, factory=2, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.full
    def test_caseid_1981911(self):
        '''右前轮低电量'''
        #设置电压12v
        hint = "Front Right Tire Sensor Batt Low"
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, factory=18, time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, factory=2, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.full
    def test_caseid_1981910(self):
        '''左后轮低电量'''
        #设置电压12v
        hint = "Rear Left Tire Sensor Batt Low"
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, factory=18, time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, factory=2, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.full
    def test_caseid_1981909(self):
        '''右后轮低电量'''
        #设置电压12v
        hint = "Rear Right Tire Sensor Batt Low"
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, factory=18, time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, factory=2, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.longtime
    @pytest.mark.sanity
    def test_caseid_1981908(self):
        '''左前胎压系统告警'''
        hint = "Left Front Tire System Failure"
        self.tire_sensor_dic["FrontLeft"]["send_rf"] = False
        time.sleep(565)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.tire_sensor_dic["FrontLeft"]["send_rf"] = True
        time.sleep(20)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1981907(self):
        '''右前胎压系统告警'''
        hint = "Right Front Tire System Failure"
        self.tire_sensor_dic["FrontRight"]["send_rf"] = False
        time.sleep(565)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.tire_sensor_dic["FrontRight"]["send_rf"] = True
        time.sleep(20)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1981906(self):
        '''左后胎压系统告警'''
        hint = "Rear Left Tire System Failure"
        self.tire_sensor_dic["RearLeft"]["send_rf"] = False
        time.sleep(565)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.tire_sensor_dic["RearLeft"]["send_rf"] = True
        time.sleep(20)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1981905(self):
        '''右后胎压系统告警'''
        hint = "Rear Right Tire System Failure"
        self.tire_sensor_dic["RearRight"]["send_rf"] = False
        time.sleep(565)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.tire_sensor_dic["RearRight"]["send_rf"] = True
        time.sleep(20)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.sanity
    def test_caseid_1981904(self):
        '''车速系统故障'''
        #车速为0，qf为0
        hint1 = "Left Front Tire System Failure"
        hint2 = "Right Front Tire System Failure"
        hint3 = "Rear Left Tire System Failure"
        hint4 = "Rear Right Tire System Failure"
        self.bus_comm.set_vehspd_and_qf(vehspd=0, veh_qf= VehSpdQf.UndefindDataAccur)
        time.sleep(90)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.SysWarnFlg, status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_info_list(name = hint1, info="1")
        self.soa.get_warning_info_list(name = hint2, info="1")
        self.soa.get_warning_info_list(name = hint3, info="1")
        self.soa.get_warning_info_list(name = hint4, info="1")
        self.bus_comm.set_vehspd_and_qf(vehspd=0, veh_qf= VehSpdQf.AccurData)
        time.sleep(20)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.SysWarnFlg, status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_info_list(name = hint1, info="0")
        self.soa.get_warning_info_list(name = hint2, info="0")
        self.soa.get_warning_info_list(name = hint3, info="0")
        self.soa.get_warning_info_list(name = hint4, info="0")

    @pytest.mark.sanity
    def test_caseid_1981903(self):
        '''胎压报警灯0-1-2-1-0'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=138,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "1")
        self.bus_comm.set_vehspd_and_qf(vehspd=0, veh_qf= VehSpdQf.UndefindDataAccur)
        time.sleep(90)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.SysWarnFlg, status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "2")
        self.bus_comm.set_vehspd_and_qf(vehspd=0, veh_qf= VehSpdQf.AccurData)
        time.sleep(20)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.SysWarnFlg, status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "1")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=230,
                                        time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "0")
    
    @pytest.mark.sanity
    def test_caseid_1981902(self):
        '''胎压报警灯0-2-2-1-0'''
        self.bus_comm.set_vehspd_and_qf(vehspd=0, veh_qf= VehSpdQf.UndefindDataAccur)
        time.sleep(90)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.SysWarnFlg, status=TireAlarmSts.LowPressureWarning)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "2")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=138,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.soa.get_warning_light_list(name= "Tire Pressure", state= "2")
        self.bus_comm.set_vehspd_and_qf(vehspd=0, veh_qf= VehSpdQf.AccurData)
        time.sleep(20)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.SysWarnFlg, status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "1")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=230,
                                        time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "0")
    
    @pytest.mark.sanity
    def test_caseid_1981901(self):
        '''胎压报警灯1 usagemode变化'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=138,
                                        time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_vehspd_and_qf(vehspd=0, veh_qf= VehSpdQf.AccurData)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "1")
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "0")
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "1")
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "0")
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "1")
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=230,
                                        time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "0")
    
    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1981900(self):
        '''胎压报警灯2 usagemode变化'''
        self.tire_sensor_dic["FrontLeft"]["send_rf"] = False
        time.sleep(565)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_vehspd_and_qf(vehspd=0, veh_qf= VehSpdQf.AccurData)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "2")
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "0")
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "2")
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "0")
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "2")
        self.tire_sensor_dic["FrontLeft"]["send_rf"] = True
        time.sleep(20)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.soa.get_and_event_check_warning_light_list(name= "Tire Pressure", state= "0")
    
    