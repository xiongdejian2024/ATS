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
    @staticmethod
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
        # new_tc_config = copy.deepcopy(self.tc_config)
        # new_tc_config['dut_ecu'] = ['BGM']
        # self.bus_comm = BusComm(self.cls_path, **new_tc_config)
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

    @pytest.mark.smoke
    @pytest.mark.verify_1
    @pytest.mark.abc
    def test_LF_LightLoad_LowPressure_Warn_caseid_115652(self):
        '''左前轮 胎压低压报警'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=178,
                                        time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=230,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.sanity
    @pytest.mark.msg_old
    def test_Message_old_Warn_Convenience_caseid_115650(self):
        '''停发FR消息报系统故障'''
        global running_flag
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        running_flag = False
        time.sleep(10)
        self.sd_tester.change_usagemode_a_to_b(UsageMode.INACTIVE, UsageMode.CONVENIENCE)
        time.sleep(5)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.MsgOldFlg, status=TireAlarmSts.LowPressureWarning)
        running_flag = True 
        self.start_send_tire_data()
        time.sleep(5)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.MsgOldFlg, status=TireAlarmSts.Normal)
    

    @pytest.mark.sanity
    def test_LowBattery_Warn_usagemode_caseid_115644(self):
        '''右前轮低电量'''
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, factory=18, time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.LowPressureWarning)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.LowPressureWarning)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, factory=2, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.Normal)
    
    @pytest.mark.sanity
    def test_LowBattery_Warn_caseid_115636(self):
        '''右前低压'''
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, factory=18, time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, factory=2, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.Normal)
    
    @pytest.mark.smoke
    def test_LHighTemperature_Warn_usagemode_caseid_115648(self):
        '''左前胎温'''
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, temperature=86, time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, temperature=80, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, temperature=79, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.Normal)
    
    @pytest.mark.smoke
    def test_Fast_Loss_Pressure_Warn_caseid_115633(self):
        '''快速漏气'''
        #设置右后轮胎胎压340kpa
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=340,
                                        time_wait=20)
        for i in range(18):
            self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=340-10*i,
                                        time_wait=5)
        #检查总线报出异常
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        time.sleep(90)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=260,
                                        time_wait=5)
    
    @pytest.mark.smoke
    def test_Loss_Pressure_usagemode_caseid_115641(self):
        '''快速漏气状态切换'''
        #设置右后轮胎胎压340kpa
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=340,
                                        time_wait=20)
        for i in range(18):
            self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=340-10*i,
                                        time_wait=5)
        #检查总线报出异常
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        time.sleep(90)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.Normal)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=260,
                                        time_wait=5)
    
    @pytest.mark.sanity
    def test_caseid_115621(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=149,
                                        time_wait=5)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=230,
                                        time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.Normal)
    
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_system_error_Warn_usagmode_caseid_115627(self):
        '''车速状态 系统故障'''
        self.tire_sensor_dic["FrontLeft"]["send_rf"] = False
        time.sleep(565)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        self.sd_tester.change_usagemode_a_to_b(UsageMode.INACTIVE, UsageMode.DRIVING)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.tire_sensor_dic["FrontLeft"]["send_rf"] = True
        time.sleep(20)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.Normal)
    
    @pytest.mark.sanity
    def test_system_error_Warn_caseid_115619(self):
        '''系统故障'''
        self.bus_comm.set_vehspd_and_qf(vehspd=0, veh_qf= VehSpdQf.UndefindDataAccur)
        time.sleep(90)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.SysWarnFlg, status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_vehspd_and_qf(vehspd=0, veh_qf= VehSpdQf.AccurData)
        time.sleep(20)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.SysWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.smoke
    def test_HighTemperature_Warn_caseid_115622(self):
        '''胎温告警'''
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, temperature=86, time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, temperature=80, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, temperature=79, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.Normal)
        
    @pytest.mark.full
    def test_LR_LightLoad_LowPressure_Warn_caseid_115645(self):
        '''四轮 胎压低压报警'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.All, pressure=172,
                                        time_wait=80)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.All, pressure=230,
                                        time_wait=10)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_LR_LightLoad_LowPressure_Warn_caseid_115625(self):
        '''左后轮 胎压低压报警'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=178,
                                        time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=230,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    @pytest.mark.msg_old
    def test_Message_old_Warn_Driving_caseid_115635(self):
        '''BGM_Message_old_Warn_Driving'''
        global running_flag
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        running_flag = False
        time.sleep(10)
        self.sd_tester.change_usagemode_a_to_b(UsageMode.INACTIVE, UsageMode.DRIVING)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.MsgOldFlg, status=TireAlarmSts.LowPressureWarning)
        running_flag = True 
        self.start_send_tire_data()
        time.sleep(5)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.MsgOldFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    @pytest.mark.msg_old
    def test_Message_old_Warn_Active_caseid_115623(self):
        '''BGM_Message_old_Warn_Active'''
        global running_flag
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        running_flag = False
        time.sleep(10)
        self.sd_tester.change_usagemode_a_to_b(UsageMode.INACTIVE, UsageMode.ACTIVE)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.MsgOldFlg, status=TireAlarmSts.LowPressureWarning)
        running_flag = True 
        self.start_send_tire_data()
        time.sleep(5)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.MsgOldFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    @pytest.mark.msg_old
    def test_Message_old_Warn_Active_caseid_115624(self):
        '''BGM_Message_old_Warn__usagemode切换'''
        global running_flag
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        running_flag = False
        time.sleep(10)
        self.sd_tester.change_usagemode_a_to_b(UsageMode.INACTIVE, UsageMode.ACTIVE)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.MsgOldFlg, status=TireAlarmSts.LowPressureWarning)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.MsgOldFlg, status=TireAlarmSts.LowPressureWarning)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.MsgOldFlg, status=TireAlarmSts.LowPressureWarning)
        running_flag = True 
        self.start_send_tire_data()
        time.sleep(5)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.MsgOldFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_RR_LightLoad_LowPressure_Warn_caseid_115617(self):
        '''右后轮 胎压低压报警'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=178,
                                        time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=230,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_RF_LightLoad_LowPressure_Warn_caseid_115616(self):
        '''右前轮 胎压低压报警'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=178,
                                        time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=230,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    def test_RR_LightLoad_LowPressure_Warn_usagemode_change_caseid_115614(self):
        '''右后轮 胎压低压报警切换usagemode'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=178,
                                        time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_vehspd_and_qf(vehspd=10.0)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=230,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    
    @pytest.mark.full
    @pytest.mark.tpmsid
    @pytest.mark.longtime
    def test_caseid_115640(self,**kwargs):
        '''TCAM_WUID_Auto_learn_24km|h'''
        #写入全0胎压id
        self.bus_comm.set_vehspd_and_qf(vehspd=6.66)
        time.sleep(5)  
        self.sd_tester.write_sensor_id([0x00,0x00,0x00, 0x00,0x00,0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(660)  
        self.sd_tester.get_and_check_tpms_id([17, 17, 17, 17, 34, 34, 34, 34, 2, 98, 134, 67, 2, 98, 132, 244], 1)
    
    @pytest.mark.full
    @pytest.mark.test
    @pytest.mark.tpmsid
    @pytest.mark.longtime
    def test_caseid_115638(self,**kwargs):
        '''TCAM_WUID_Auto_learn_55km|h'''
        #写入全0胎压id
        self.bus_comm.set_vehspd_and_qf(vehspd=15.27)
        time.sleep(5)  
        self.sd_tester.write_sensor_id([0x00,0x00,0x00, 0x00,0x00,0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(660)  
        self.sd_tester.get_and_check_tpms_id([17, 17, 17, 17, 34, 34, 34, 34, 2, 98, 134, 67, 2, 98, 132, 244], 0)
    
    @pytest.mark.full
    @pytest.mark.wrong
    @pytest.mark.tpmsid
    @pytest.mark.longtime
    def test_caseid_115637(self,**kwargs):
        '''TCAM_WUID_Auto_learn_95km|h'''
        #写入全0胎压id
        self.bus_comm.set_vehspd_and_qf(vehspd=26.38)
        time.sleep(5)  
        self.sd_tester.write_sensor_id([0x00,0x00,0x00, 0x00,0x00,0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(660)  
        self.sd_tester.get_and_check_tpms_id([17, 17, 17, 17, 34, 34, 34, 34, 2, 98, 134, 67, 2, 98, 132, 244], 0)
    
    @pytest.mark.full
    @pytest.mark.tpmsid
    @pytest.mark.longtime
    def test_caseid_115631(self,**kwargs):
        '''TCAM_WUID_Auto_learn_35km|h'''
        #写入全0胎压id
        self.bus_comm.set_vehspd_and_qf(vehspd=9.72)
        time.sleep(5)
        self.sd_tester.write_sensor_id([0x00,0x00,0x00, 0x00,0x00,0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(660)  
        self.sd_tester.get_and_check_tpms_id([17, 17, 17, 17, 34, 34, 34, 34, 2, 98, 134, 67, 2, 98, 132, 244], 0)
    
    @pytest.mark.full
    @pytest.mark.longtime
    @pytest.mark.tpmsid
    def test_caseid_115620(self,**kwargs):
        '''TCAM_WUID_Auto_learn_125km|h'''
        #写入全0胎压id
        self.bus_comm.set_vehspd_and_qf(vehspd=34.72)
        time.sleep(5)
        self.sd_tester.write_sensor_id([0x00,0x00,0x00, 0x00,0x00,0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(660)  
        self.sd_tester.get_and_check_tpms_id([17, 17, 17, 17, 34, 34, 34, 34, 2, 98, 134, 67, 2, 98, 132, 244], 0)
    
    @pytest.mark.full
    @pytest.mark.wrong
    @pytest.mark.bug
    @pytest.mark.tpmsid
    @pytest.mark.longtime
    def test_caseid_115626(self,**kwargs):
        '''TCAM_WUID_Auto_learn_35km|h_5min+stop2min+5min'''
        #写入全0胎压id
        self.bus_comm.set_vehspd_and_qf(vehspd=9.72)
        time.sleep(5)
        self.sd_tester.write_sensor_id([0x00,0x00,0x00, 0x00,0x00,0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(300)  
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        time.sleep(120)  
        self.bus_comm.set_vehspd_and_qf(vehspd=9.72)
        time.sleep(200)  
        self.sd_tester.get_and_check_tpms_id([17, 17, 17, 17, 34, 34, 34, 34, 2, 98, 134, 67, 2, 98, 132, 244], 1)
        time.sleep(120)
        self.sd_tester.get_and_check_tpms_id([17, 17, 17, 17, 34, 34, 34, 34, 2, 98, 134, 67, 2, 98, 132, 244], 0)
    
    @pytest.mark.full
    @pytest.mark.tpmsid
    @pytest.mark.longtime
    def test_caseid_115613(self,**kwargs):
        '''BGM_Fast_Loss_Pressure_Warn_not_upload_until_autoloacted'''
        self.bus_comm.set_vehspd_and_qf(vehspd=9.72)
        time.sleep(5)
        self.sd_tester.write_sensor_id([0x00,0x00,0x00, 0x00,0x00,0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=340,
                                        time_wait=20)
        for i in range(18):
            self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=340-10*i,
                                        time_wait=5)
        #检查总线报出异常
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.FastLoseWarnFlg,
                                      status=TireAlarmSts.Normal)
        time.sleep(550)  
        self.sd_tester.get_and_check_tpms_id([17, 17, 17, 17, 34, 34, 34, 34, 2, 98, 134, 67, 2, 98, 132, 244], 0)
    
    @pytest.mark.full
    @pytest.mark.bug
    def test_caseid_115618(self):
        '''BGM_Persistence_of_LowPressure_Warn_over_i/gnition_cycles'''
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=178,
                                        time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_vehspd_and_qf(vehspd=9.72)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=230,
                                        time_wait=10)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.PWarnFlg, status=TireAlarmSts.Normal)
    

    @pytest.mark.full
    def test_HighTemperature_Warn_caseid_115628(self):
        '''胎温告警'''
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, temperature=86, time_wait=90)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, temperature=79, time_wait=5)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.TWarnFlg,
                                      status=TireAlarmSts.Normal)

    @pytest.mark.sanity
    def test_FilterID_update_did281F_caseid_115615(self):
        "BGM_FilterID_update_did281F"
        check_value = [303174162, 320017171, 336860180, 353703189]
        time.sleep(5)
        self.sd_tester.write_sensor_id([0x12,0x12,0x12, 0x12,0x13,0x13, 0x13,0x13, 0x14, 0x14, 0x14, 0x14, 0x15, 0x15, 0x15, 0x15])
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        self.bus_comm.check_tire_config(id=check_value, config=[], is_id=1, is_config=0)
    
    @pytest.mark.full
    def test_FilterID_update_did281F_caseid_115642(self):
        "BGM_TireFil_FilterID_ok"
        check_value_1 = [286331153, 40011331, 40010996, 572662306]
        check_value_2 = [0, 0, 1, 1, 0]
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        time.sleep(0.3)
        self.sd_tester.change_usagemode_a_to_b(UsageMode.INACTIVE, UsageMode.DRIVING, wait_time=5)
        self.bus_comm.check_tire_config(id=check_value_1, config=check_value_2, is_id=1, is_config=1)
    
    @pytest.mark.full
    def test_caseid_1959963(self):
        "BGM收到胎压配置请求发送配置报文_driving"
        check_value_1 = [286331153, 40011331, 40010996, 572662306]
        check_value_2 = [0, 0, 1, 1, 0]
        self.bus_comm.set_tire_config_req()
        self.bus_comm.check_tire_config(id=check_value_1, config=check_value_2, is_id=1, is_config=1)
    
    @pytest.mark.full
    def test_caseid_1959964(self):
        "BGM收到胎压配置请求发送配置报文_active"
        check_value_1 = [286331153, 40011331, 40010996, 572662306]
        check_value_2 = [0, 0, 1, 2, 0]
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        self.bus_comm.set_tire_config_req()
        self.bus_comm.check_tire_config(id=check_value_1, config=check_value_2, is_id=1, is_config=1)
    
    @pytest.mark.full
    def test_caseid_1959965(self):
        "BGM收到胎压配置请求发送配置报文_convenience"
        check_value_1 = [286331153, 40011331, 40010996, 572662306]
        check_value_2 = [0, 0, 1, 2, 0]
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_tire_config_req()
        self.bus_comm.check_tire_config(id=check_value_1, config=check_value_2, is_id=1, is_config=1)
    
    @pytest.mark.sanity
    def test_caseid_1959966(self):
        "BGM收到胎压配置请求发送配置报文_inactive"
        check_value_1 = [286331153, 40011331, 40010996, 572662306]
        check_value_2 = [1, 0, 1, 0, 0]
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_tire_config_req()
        self.bus_comm.check_tire_config(id=check_value_1, config=check_value_2, is_id=1, is_config=1)
    
    @pytest.mark.full
    def test_caseid_1959967(self):
        "BGM收到胎压配置请求发送配置报文_abandon"
        check_value_1 = [286331153, 40011331, 40010996, 572662306]
        check_value_2 = [1, 0, 1, 0, 0]
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.set_tire_config_req()
        self.bus_comm.check_tire_config(id=check_value_1, config=check_value_2, is_id=1, is_config=1)
    
    @pytest.mark.sanity
    def test_caseid_1989388(self):
        ''' BGM_胎温胎压更新_左前'''
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T = self.bus_comm.get_four_tire_pressure_and_temperature()
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=200,
                                        time_wait=10)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, temperature=50,
                                        time_wait=10)
        tire_fl_P, tire_fl_T, check_tire_p, check_tire_t = self.sd_tester.generate_tire_P_and_T(pressure = 200, temperature = 50)
        self.bus_comm.check_four_tire_pressure_and_temperature(tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T)
        self.soa.get_and_check_Pressure(tyres=tyres.kTyreFrintLeft, pressure=check_tire_p)
        self.soa.get_and_check_Temperature(tyres=tyres.kTyreFrintLeft, temperature=check_tire_t)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, pressure=240,
                                        time_wait=10)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, temperature=70,
                                        time_wait=10)
        tire_fl_P, tire_fl_T, check_tire_p, check_tire_t = self.sd_tester.generate_tire_P_and_T(pressure = 240, temperature = 70)
        self.bus_comm.check_four_tire_pressure_and_temperature(tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T)
        self.soa.get_and_check_Pressure(tyres=tyres.kTyreFrintLeft, pressure=check_tire_p)
        self.soa.get_and_check_Temperature(tyres=tyres.kTyreFrintLeft, temperature=check_tire_t)

    @pytest.mark.full
    def test_caseid_1989387(self):
        ''' BGM_胎温胎压更新_右前'''
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T = self.bus_comm.get_four_tire_pressure_and_temperature()
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=200,
                                        time_wait=10)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, temperature=50,
                                        time_wait=10)
        tire_fr_P, tire_fr_T, check_tire_p, check_tire_t = self.sd_tester.generate_tire_P_and_T(pressure = 200, temperature = 50)
        self.bus_comm.check_four_tire_pressure_and_temperature(tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T)
        self.soa.get_and_check_Pressure(tyres=tyres.kTyreFrintRight, pressure=check_tire_p)
        self.soa.get_and_check_Temperature(tyres=tyres.kTyreFrintRight, temperature=check_tire_t)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, pressure=240,
                                        time_wait=10)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, temperature=70,
                                        time_wait=10)
        tire_fr_P, tire_fr_T, check_tire_p, check_tire_t = self.sd_tester.generate_tire_P_and_T(pressure = 240, temperature = 70)
        self.bus_comm.check_four_tire_pressure_and_temperature(tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T)
        self.soa.get_and_check_Pressure(tyres=tyres.kTyreFrintRight, pressure=check_tire_p)
        self.soa.get_and_check_Temperature(tyres=tyres.kTyreFrintRight, temperature=check_tire_t)

    @pytest.mark.full
    def test_caseid_1989386(self):
        ''' BGM_胎温胎压更新_左后'''
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T = self.bus_comm.get_four_tire_pressure_and_temperature()
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=200,
                                        time_wait=10)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, temperature=50,
                                        time_wait=10)
        tire_rl_P, tire_rl_T, check_tire_p, check_tire_t = self.sd_tester.generate_tire_P_and_T(pressure = 200, temperature = 50)
        self.bus_comm.check_four_tire_pressure_and_temperature(tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T)
        self.soa.get_and_check_Pressure(tyres=tyres.kTyreRearLeft, pressure=check_tire_p)
        self.soa.get_and_check_Temperature(tyres=tyres.kTyreRearLeft, temperature=check_tire_t)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, pressure=240,
                                        time_wait=10)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, temperature=70,
                                        time_wait=10)
        tire_rl_P, tire_rl_T, check_tire_p, check_tire_t = self.sd_tester.generate_tire_P_and_T(pressure = 240, temperature = 70)
        self.bus_comm.check_four_tire_pressure_and_temperature(tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T)
        self.soa.get_and_check_Pressure(tyres=tyres.kTyreRearLeft, pressure=check_tire_p)
        self.soa.get_and_check_Temperature(tyres=tyres.kTyreRearLeft, temperature=check_tire_t)

    @pytest.mark.full
    def test_caseid_1989385(self):
        ''' BGM_胎温胎压更新_右后'''
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T = self.bus_comm.get_four_tire_pressure_and_temperature()
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=200,
                                        time_wait=10)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, temperature=50,
                                        time_wait=10)
        tire_rr_P, tire_rr_T, check_tire_p, check_tire_t = self.sd_tester.generate_tire_P_and_T(pressure = 200, temperature = 50)
        self.bus_comm.check_four_tire_pressure_and_temperature(tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T)
        self.soa.get_and_check_Pressure(tyres=tyres.kTyreRearRight, pressure=check_tire_p)
        self.soa.get_and_check_Temperature(tyres=tyres.kTyreRearRight, temperature=check_tire_t)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, pressure=240,
                                        time_wait=10)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, temperature=70,
                                        time_wait=10)
        tire_rr_P, tire_rr_T, check_tire_p, check_tire_t = self.sd_tester.generate_tire_P_and_T(pressure = 240, temperature = 70)
        self.bus_comm.check_four_tire_pressure_and_temperature(tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T)
        self.soa.get_and_check_Pressure(tyres=tyres.kTyreRearRight, pressure=check_tire_p)
        self.soa.get_and_check_Temperature(tyres=tyres.kTyreRearRight, temperature=check_tire_t)

    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994578(self):
        ''' BGM_胎压数据存储_诊断重启'''
        global running_flag
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.All, pressure=230,
                                        time_wait=10)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.All, temperature=40,
                                        time_wait=10)
        running_flag = False
        tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T = self.bus_comm.get_four_tire_pressure_and_temperature()
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.pause_all_bus_send()
        time.sleep(5)
        self.sd_tester.reset_bgm()
        self.bus_comm.resume_all_bus_send()
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.check_four_tire_pressure_and_temperature(tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T)
        running_flag = True
    
    @pytest.mark.sanity
    @pytest.mark.nvm
    def test_caseid_1980100(self):
        ''' BGM_胎压数据存储_上下电'''
        global running_flag
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.All, pressure=230,
                                        time_wait=10)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.All, temperature=40,
                                        time_wait=10)
        running_flag = False
        tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T = self.bus_comm.get_four_tire_pressure_and_temperature()
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        time.sleep(5)
        self.io.bgm_power_off()
        time.sleep(5)
        self.io.bgm_power_on()
        time.sleep(20)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.check_four_tire_pressure_and_temperature(tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T)
        running_flag = True

    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1980101(self):
        ''' BGM_胎压数据存储_休眠唤醒'''
        global running_flag
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        self.bus_comm.set_tpms_pressure(tire_sensor=self.tire_sensor_dic, pos=TirePos.All, pressure=230,
                                        time_wait=10)
        self.bus_comm.set_tpms_temperature(tire_sensor=self.tire_sensor_dic, pos=TirePos.All, temperature=40,
                                        time_wait=10)
        running_flag = False
        tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T = self.bus_comm.get_four_tire_pressure_and_temperature()
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.network_sleep()
        self.io.bgm_diag_line_up()
        self.sd_tester.start_sd_tester()
        time.sleep(20)
        self.bus_comm.resume_all_bus_send()
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.check_four_tire_pressure_and_temperature(tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T)
        running_flag = True
    