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
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common import *
running_flag = True


@allure.feature("标定")
@allure.story("胎压标定")
class TestTPMS(TestABCBase):
    def before_class(self, ecu):
        global running_flag
        self.soa.update(["TyreService_client"])
        sleep(2)
        self.sd_tester.write_ccp(ccp={225: 4, 226: 4})
        self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)
        self.bus_comm.pause_bus_send_tpms()
        self.tire_sensor_dic = self.bus_comm.tire_sensor_ini()
        self.rolling_counter = 0
        running_flag = True
        self.start_send_tire_data_main(self)

    def before_each_func(self, ecu):
        # self.tire_sensor_dic = self.bus_comm.tire_sensor_ini()
        self.tire_sensor_dic["FrontLeft"]["send_rf"] = True
        self.tire_sensor_dic["FrontRight"]["send_rf"] = True
        self.tire_sensor_dic["RearRight"]["send_rf"] = True
        self.tire_sensor_dic["RearLeft"]["send_rf"] = True
        self.sd_tester.write_sensor_id(
            [0x11, 0x11, 0x11, 0x11, 0x02, 0x62, 0x86, 0x43, 0x02, 0x62, 0x84, 0xF4, 0x22, 0x22, 0x22, 0x22])
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

    
    @pytest.mark.sanity
    @pytest.mark.DTC
    @pytest.mark.wenti
    @pytest.mark.single_bgm
    def test_sensor_not_learning_caseid_115649(self,**kwargs):
        '''传感器未学习0x924D55'''
        self.sd_tester.write_sensor_id([0x00,0x00,0x00, 0x00,0x00,0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(5)  
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.SysWarnFlg, status=TireAlarmSts.LowPressureWarning)
        result, status1, status2 = self.sd_tester.send_dtc_request_and_return_check_status()
        self.sd_tester.check_dtc(result, [146,77,85], status1)
        time.sleep(5)
        self.sd_tester.write_sensor_id([0x11,0x11 ,0x11 ,0x11 ,0x02 ,0x62 ,0x86 ,0x43,0x02 ,0x62 ,0x84 ,0xF4 ,0x22 ,0x22 ,0x22 ,0x22])
        time.sleep(3)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.SysWarnFlg, status=TireAlarmSts.Normal)
        self.sd_tester.send_dtc_request_and_check_dtc_status([146,77,85], status2)
    
    @pytest.mark.sanity
    @pytest.mark.DTC
    @pytest.mark.longtime
    @pytest.mark.single_bgm
    def test_Lf_tire_pressure_sensor_signalloss_caseid_115647(self):
        '''左前胎压传感器丢失0x5A568F'''
        self.tire_sensor_dic["FrontLeft"]["send_rf"] = False
        time.sleep(565)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        result, status1, status2 = self.sd_tester.send_dtc_request_and_return_check_status()
        self.sd_tester.check_dtc(result, [90,86,143], status1)
        self.tire_sensor_dic["FrontLeft"]["send_rf"] = True
        time.sleep(20)
        self.sd_tester.send_dtc_request_and_check_dtc_status([90,86,143], status2)
      
    @pytest.mark.sanity
    @pytest.mark.DTC
    @pytest.mark.single_bgm
    def test_Leftfront_tirepressure_sensor_voltage_low_caseid_115612(self):
        '''0x5A5616_左前胎压传感器电压低'''  
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, factory=18, time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontLeft, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.LowPressureWarning)
        result, status1, status2 = self.sd_tester.send_dtc_request_and_return_check_status()
        self.sd_tester.check_dtc(result, [90,86,22], status1)
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontLeft, factory=2, time_wait=10)
        self.sd_tester.send_dtc_request_and_check_dtc_status([90,86,22], status2)
    
    @pytest.mark.full
    @pytest.mark.DTC
    @pytest.mark.single_bgm
    def test_Rr_tirepressure_sensor_voltage_low_caseid_115651(self):
        '''0x5A6216_右后胎压传感器电压低'''  
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, factory=18, time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.LowPressureWarning)
        result, status1, status2 = self.sd_tester.send_dtc_request_and_return_check_status()
        self.sd_tester.check_dtc(result, [90,98,22], status1)
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearRight, factory=2, time_wait=10)
        self.sd_tester.send_dtc_request_and_check_dtc_status([90,98,22], status2)
    
    @pytest.mark.full
    @pytest.mark.DTC
    @pytest.mark.longtime
    @pytest.mark.single_bgm
    # @pytest.mark.test
    def test_Rf_tire_pressure_sensor_signalloss_caseid_115646(self):
        '''DTC_0x5A588F_右前胎压传感器信号丢失'''
        self.tire_sensor_dic["FrontRight"]["send_rf"] = False
        time.sleep(565)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        result, status1, status2 = self.sd_tester.send_dtc_request_and_return_check_status()
        self.sd_tester.check_dtc(result, [90,88,143], status1)
        self.tire_sensor_dic["FrontRight"]["send_rf"] = True
        time.sleep(20)
        self.sd_tester.send_dtc_request_and_check_dtc_status([90,88,143], status2)
    
    @pytest.mark.full
    @pytest.mark.DTC
    @pytest.mark.longtime
    @pytest.mark.single_bgm
    def test_LR_tire_pressure_sensor_signalloss_caseid_115643(self):
        '''DTC_0x5A608F_左后胎压传感器信号丢失'''
        self.tire_sensor_dic["RearLeft"]["send_rf"] = False
        time.sleep(565)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        result, status1, status2 = self.sd_tester.send_dtc_request_and_return_check_status()
        self.sd_tester.check_dtc(result, [90,96,143], status1)
        self.tire_sensor_dic["RearLeft"]["send_rf"] = True
        time.sleep(20)
        self.sd_tester.send_dtc_request_and_check_dtc_status([90,96,143], status2)
    
    @pytest.mark.full
    @pytest.mark.DTC
    @pytest.mark.longtime
    @pytest.mark.single_bgm
    def test_RR_tire_pressure_sensor_signalloss_caseid_115634(self):
        '''DTC_0x5A628F_右后胎压传感器信号丢失'''
        self.tire_sensor_dic["RearRight"]["send_rf"] = False
        time.sleep(565)
        self.bus_comm.check_tire_flag(pos=TirePos.RearRight, flag=SysWarnFlg.SysWarnFlg,
                                      status=TireAlarmSts.LowPressureWarning)
        result, status1, status2 = self.sd_tester.send_dtc_request_and_return_check_status()
        self.sd_tester.check_dtc(result, [90,98,143], status1)
        self.tire_sensor_dic["RearRight"]["send_rf"] = True
        time.sleep(20)
        self.sd_tester.send_dtc_request_and_check_dtc_status([90,98,143], status2)
    
    @pytest.mark.full
    @pytest.mark.DTC
    @pytest.mark.single_bgm
    def test_Rr_tirepressure_sensor_voltage_low_caseid_115630(self):
        '''DTC_0x5A5816_右前胎压传感器电压低'''
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, factory=18, time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.FrontRight, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.LowPressureWarning)
        result, status1, status2 = self.sd_tester.send_dtc_request_and_return_check_status()
        self.sd_tester.check_dtc(result, [90,88,22], status1)
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.FrontRight, factory=2, time_wait=10)
        self.sd_tester.send_dtc_request_and_check_dtc_status([90,88,22], status2)
    
    @pytest.mark.full
    @pytest.mark.DTC
    @pytest.mark.single_bgm
    def test_Rr_tirepressure_sensor_voltage_low_caseid_115629(self):
        '''DTC_0x5A6016_左后胎压传感器电压低'''
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, factory=18, time_wait=30)
        self.bus_comm.check_tire_flag(pos=TirePos.RearLeft, flag=SysWarnFlg.BattLoSt,
                                      status=TireAlarmSts.LowPressureWarning)
        result, status1, status2 = self.sd_tester.send_dtc_request_and_return_check_status()
        self.sd_tester.check_dtc(result, [90,96,22], status1)
        self.bus_comm.set_tpms_factory(tire_sensor=self.tire_sensor_dic, pos=TirePos.RearLeft, factory=2, time_wait=10)
        self.sd_tester.send_dtc_request_and_check_dtc_status([90,96,22], status2)
    
    @pytest.mark.full
    @pytest.mark.DTC
    @pytest.mark.single_bgm
    def test_caseid_115632(self):
        '''DTC_0xD00C87_VDDM数据丢失'''
        self.bus_comm.set_vehspd_and_qf(vehspd=0, veh_qf= VehSpdQf.UndefindDataAccur)
        time.sleep(70)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.SysWarnFlg, status=TireAlarmSts.LowPressureWarning)
        result, status1, status2 = self.sd_tester.send_dtc_request_and_return_check_status()
        self.sd_tester.check_dtc(result, [208,12,135], status1)
        self.bus_comm.set_vehspd_and_qf(vehspd=0, veh_qf= VehSpdQf.AccurData)
        time.sleep(10)
        self.bus_comm.check_four_tire_flag(flag=SysWarnFlg.SysWarnFlg, status=TireAlarmSts.Normal)
        self.sd_tester.send_dtc_request_and_check_dtc_status([208,12,135], status2)
    
    @pytest.mark.full
    @pytest.mark.DTC
    @pytest.mark.bug
    @pytest.mark.longtime
    @pytest.mark.single_bgm
    def test_caseid_1892736(self,**kwargs):
        '''DTC_0x924D77_自动定位失败'''
        self.tire_sensor_dic["FrontRight"]["send_rf"] = False
        self.sd_tester.write_sensor_id([0x00,0x00,0x00, 0x00,0x00,0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  
        time.sleep(660)
        result, status1, status2 = self.sd_tester.send_dtc_request_and_return_check_status()
        self.sd_tester.check_dtc(result, [146,77,119], status1)
        self.sd_tester.write_sensor_id([0x11,0x11 ,0x11 ,0x11 ,0x02 ,0x62 ,0x86 ,0x43,0x02 ,0x62 ,0x84 ,0xF4 ,0x22 ,0x22 ,0x22 ,0x22])
        self.tire_sensor_dic["FrontRight"]["send_rf"] = True
        self.sd_tester.send_dtc_request_and_check_dtc_status([146,77,119], status1)
