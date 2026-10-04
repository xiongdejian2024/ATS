import os
import sys
import pytest
import allure
from time import sleep
import threading
import math


sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_ecu.legacy.driver.ssh_interface import command_send
from xat_ecu.legacy.common.data_type_handing import logger
# from test_case.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
# from ecu_simulator.ecu_sim.sd_tester import Sd_Tester

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.tsp.rvs_client import RvsClient
from signal_value_mapping import *

@allure.feature("SOA服务接口")
@allure.story("BGM应用/ConditionCheckService")
class TestRVS(TestABCBase):
    
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        # self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        for process_name in ["monitor_em2.sh", "em2", "s2s_service","SOAApp","service_monitor"]:
            res = command_send(
                device_name="BGM",
                cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                timeout=60,
            )[1]
            logger.info(f"res: {res}")
            pid = res.split()[1]
            command_send(device_name="BGM", cmd=f"kill -9 {pid}")
        sleep(2)
        command_send(device_name="BGM", cmd='su - service_monitor -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/service_monitor  -c /app/etc/service_monitor.json &"', timeout=15)

        self.soa.update(["ClimateControlService_server","HighVoltageService_server","WiperService_server","ChassisService_server","ShieldWindowService_server","VehicleModeService_server","CentralLockService_server","OuterRearViewService_server","InteractiveService_server","TyreService_server","SentryModeService_server","SteerWheelService_server","AccountService_server","VehicleSetStatusService_server","LowVoltageService_server","KeyService_server","LightService_server","MarsPilotMarsDriverService_server","PedalService_server","SeatService_server","RPAAPAService_server","LocationFusionService_server","HighVoltageAppService_server","WTIService_server","WTIAutoDriveService_server"])
   
        self.soa.start_send_GetHVBatterySOH_response()
        self.soa.start_send_GetHVSOCInfo_response()
        self.soa.start_send_GetRange_response()
        self.soa.start_send_GetBatteryStatus_response()
        
        self.vid = self.tb_config["vid"]
        self.rvs_client = RvsClient(vid=self.vid)
        logger.info("VID: {0}".format(self.vid))
        sleep(2)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        # self.bus_comm.set_vehspd_and_qf(vehspd=0)
        # self.sd_tester.write_ccp({225: 7, 226: 7}) 
        # try:
        #     self.mix.set_common_precontion(
        #         usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
        #     )
        # except Exception as e:
        #     logger.info(f"----------> after_class Error{str(e)}")
        # self.sd_tester.hard_reset(TA.BGM_MCU)
        # self.sd_tester.hard_reset(TA.BGM_SOC)
        self.soa.stop_soa()
        sleep(1)
        self.io.bgm_power_off()
        sleep(1)
        self.io.bgm_power_on()
        sleep(15)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        # super().before_each_func(ecu, start=False)
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.sd_tester.write_ccp(ccp={566: 25})
        self.bus_comm.set_dtc_pre()
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.Disconnected, DispHvBattLvlOfChrg=80.0)
        self.bus_comm.set_charging_sts(ChargingSts.Default)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_dcdc_battary_act_sts_on_can(DcDcActvd=DcDcActvd.ConversionToLVSide)
        self.bus_comm.set_dispbattegyout(DispBattEgyOut=40.0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        pass

    def after_each_func(self, ecu):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        self.io.hazard_light_close()
        self.io.bgm_diag_line_up()
        pass
        # super().after_each_func(ecu, start=False)  
    
    
    @pytest.mark.sanity
    def test_outview_defrost_caseid_112830(self):
        '''后视镜加热 '''
        self.sd_tester.write_multi_ccp({182: 5, 13: 4})
        self.soa.send_event_notify("OuterRearViewService_server", "OuterRearViewHeatStatus", {"sts":{"workSts":0,"heatSts":0}})
        sleep(1)
        self.soa.send_event_notify("OuterRearViewService_server", "OuterRearViewHeatStatus", {"sts":{"workSts":1,"heatSts":1}})
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.CabinStatus,keys=["defrostStatus","viewSwitchInfo","status"],target_value=1)
        self.soa.send_event_notify("OuterRearViewService_server", "OuterRearViewHeatStatus", {"sts":{"workSts":0,"heatSts":0}})
        sleep(1)
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.CabinStatus,keys=["defrostStatus","viewSwitchInfo","status"],target_value=0)
    

    @pytest.mark.sanity
    def test_shieldWindow_defrost_caseid_116063(self):
        '''后挡风加热 '''
        self.soa.send_event_notify("ShieldWindowService_server",  "RearShieldWindowHeatStatus",
                                       {"sts": 0})
        sleep(1)
        self.soa.send_event_notify("ShieldWindowService_server",  "RearShieldWindowHeatStatus",
                                       {"sts": 1})
        self.tsp.check_rvs_data_update_new(
            block=BlockName.CabinStatus,keys=["defrostStatus","shieldWindow","windowId==2","ventWorkStatus"],target_value=1)
        sleep(1)
        self.soa.send_event_notify("ShieldWindowService_server",  "RearShieldWindowHeatStatus",
                                       {"sts": 0})
        self.tsp.check_rvs_data_update_new(
            block=BlockName.CabinStatus,keys=["defrostStatus","shieldWindow","windowId==2","ventWorkStatus"],target_value=0)

    @pytest.mark.sanity
    def test_steer_wheel_heating_level_caseid_112828(self):
        '''方向盘加热等级 '''
        self.soa.send_event_notify("SteerWheelService_server",  "Heat",
                                       {"sts": {"level":0}})
        for key in [3,2,1,0]:
            self.soa.send_event_notify("SteerWheelService_server",  "Heat",
                                       {"sts": {"level":key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["steerWheel","level"],target_value=key
            )


    @pytest.mark.sanity
    def test_steer_wheel_heating_status_caseid_1983034(self):
        '''方向盘加热状态 '''
        self.soa.send_event_notify("SteerWheelService_server",  "SteerHeatAvailiable",
                                       {"status": 2})
        for key in [5,4,3,1,2,0]:
            self.soa.send_event_notify("SteerWheelService_server",  "SteerHeatAvailiable",
                                       {"status": key})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["steerWheel","status"],target_value=key
            )

    @pytest.mark.sanity
    def test_chargspeed_caseid_112361(self):
        '''充电速度 '''        
        self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"chargingState":0,"chargeSpeedCalculate":0}})
        sleep(1)        
        for key in [1000,2000,0]:
            self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"chargingState":15,"chargeSpeedCalculate":key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargingSpeed"],target_value=key,timeout=12
            )
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"chargingState":0,"chargeSpeedCalculate":0}})


    @pytest.mark.sanity
    def test_charg_InputPower_caseid_1919008(self):
        '''桩充功率 '''
        self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
                                       {"info": {"chargePowerInput": 220000}})
        for key in [100000,150000,837020]:
            self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
                                       {"info": {"chargePowerInput": key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargerInputPower"],target_value=key,timeout=12
            )

    @pytest.mark.full
    def test_equipmentTypes_caseid_1990883_1983037_116052(self):
        '''充电桩类型 '''
        self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
                                       {'info': {'equipmentTypes': [0]}})
        for key in [3,4,7]:
            self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
                                       {"info": {"equipmentTypes": [1,key,8]}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","equipmentInfo","type"],target_value=[1,key,8],timeout=12
            )
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
                                       {'info': {'equipmentTypes': [0]}})
        for key in [2,0,1]:
            self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
                                       {"info": {"equipmentTypes": [key,4,8]}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","equipmentInfo","type"],target_value=[key,4,8],timeout=12
            )
    # @pytest.mark.sanity
    # def test_CalculateSoc_caseid_350350(self):
    #     self.soa.send_event_notify("LowVoltageService_server","BatteryStatus",
    #                                    {"status": {"calculatedStatus":0,"isValid":True,"calculatedSoc": 0}})
    #     for key in [50,80,100]:
    #         self.soa.send_event_notify("LowVoltageService_server","BatteryStatus",
    #                                    {"status": {"calculatedStatus":0,"isValid":True,"calculatedSoc": key}})
    #         self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["batteryInfo","calculatedSoc"],target_value=key,timeout=12
    #         )
    
    # @pytest.mark.sanity
    # def test_calculatedSoh_caseid_360360(self):
    #     self.soa.send_event_notify("LowVoltageService_server","BatteryStatus",
    #                                    {"status": {"isValid":True,"calculatedSoh": 50}})
    #     for key in [0,80,100]:
    #         self.soa.send_event_notify("LowVoltageService_server","BatteryStatus",
    #                                    {"status": {"isValid":True,"calculatedSoh": key}})
    #         self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["batteryInfo","calculatedSoh"],target_value=key,timeout=12
    #         )
    
    
    @pytest.mark.sanity
    def test_parkMode_lefttime_caseid_1988380(self):
        '''维持上电预估剩余时间 '''
        self.soa.send_event_notify("VehicleSetStatusService_server","ParkingComfortModeSts",
                                       {"sts": {"leftTime":500}})
        for key in [15,30,61,1440,1500]:
            self.soa.send_event_notify("VehicleSetStatusService_server","ParkingComfortModeSts",
                                       {"sts": {"leftTime":key}})
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode,keys=["parkingComfortMode","leftTime"],target_value=key)

    
    @pytest.mark.full
    def test_displayLeftTime_caseid_1988381_1988379_1988378_1988377(self):
        '''维持上电预估剩余时间提示 '''
        self.soa.send_event_notify("VehicleSetStatusService_server","ParkingComfortModeSts",
                                       {"sts": {"displayLeftTime":0}})
        for key in range(1,30):
            self.soa.send_event_notify("VehicleSetStatusService_server","ParkingComfortModeSts",
                                       {"sts": {"displayLeftTime":key}})
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode,keys=["parkingComfortMode","displayLeftTime"],target_value=key)

        
        
    @pytest.mark.sanity
    def test_PetmodeSts_caseid_1988854_1988853_1988852_1988851_1988850_1988855(self):
        '''宠物模式 '''
        self.soa.send_event_notify("InteractiveService_server", "PetModeSts", {"sts": 0})
        for key in [1,2,1,0]:
            self.soa.send_event_notify("InteractiveService_server", "PetModeSts", {"sts": key})
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode,keys=["petModeSts"],target_value=key)


    @allure.title("左前胎压")
    @pytest.mark.sanity
    def test_caseid_1983046(self):
        self.soa.send_event_notify("TyreService_server", "AllTyrePressure", 
                                       {"infos": [{"id": 0, "pressure": 230.5},
                                                {"id": 1, "pressure": 220.5},
                                                {"id": 2, "pressure": 220.5},
                                                {"id": 3, "pressure": 220.5}]})
        sleep(1)
        for key in [220.5,226.5,350.114]:
            self.soa.send_event_notify("TyreService_server", "AllTyrePressure", 
                                       {"infos": [{"id": 0, "pressure": key},
                                                {"id": 1, "pressure": 220.5},
                                                {"id": 2, "pressure": 220.5},
                                                {"id": 3, "pressure": 220.5}]})
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["tire","id==0","pressure"],target_value=round(key*0.01,1))


    @allure.title("右前胎压")
    @pytest.mark.sanity
    def test_caseid_1983045(self):
        self.soa.send_event_notify("TyreService_server", "AllTyrePressure", 
                                       {"infos": [{"id": 0, "pressure": 230.5},
                                                {"id": 1, "pressure": 200.5},
                                                {"id": 2, "pressure": 220.5},
                                                {"id": 3, "pressure": 220.5}]})
        sleep(1)
        for key in [220.5,226.5,350.114]:
            self.soa.send_event_notify("TyreService_server", "AllTyrePressure", 
                                       {"infos": [{"id": 0, "pressure": 230.5},
                                                {"id": 1, "pressure": key},
                                                {"id": 2, "pressure": 220.5},
                                                {"id": 3, "pressure": 220.5}]})
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["tire","id==1","pressure"],target_value=round(key*0.01,1))
    

    @allure.title("左后胎压")
    @pytest.mark.sanity
    def test_caseid_1983044(self):
        self.soa.send_event_notify("TyreService_server", "AllTyrePressure", 
                                       {"infos": [{"id": 0, "pressure": 230.5},
                                                {"id": 1, "pressure": 200.5},
                                                {"id": 2, "pressure": 160.5},
                                                {"id": 3, "pressure": 220.5}]})
        sleep(1)
        for key in [220.5,226.5,350.114]:
            self.soa.send_event_notify("TyreService_server", "AllTyrePressure", 
                                       {"infos": [{"id": 0, "pressure": 230.5},
                                                {"id": 1, "pressure": 200.5},
                                                {"id": 2, "pressure": key},
                                                {"id": 3, "pressure": 220.5}]})
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["tire","id==2","pressure"],target_value=round(key*0.01,1))

    
    @allure.title("右后胎压")
    @pytest.mark.sanity
    def test_caseid_1983043(self):
        self.soa.send_event_notify("TyreService_server", "AllTyrePressure", 
                                       {"infos": [{"id": 0, "pressure": 230.5},
                                                {"id": 1, "pressure": 200.5},
                                                {"id": 2, "pressure": 160.5},
                                                {"id": 3, "pressure": 170.5}]})
        sleep(1)
        for key in [220.5,226.5,350.114]:
            self.soa.send_event_notify("TyreService_server", "AllTyrePressure", 
                                       {"infos": [{"id": 0, "pressure": 230.5},
                                                {"id": 1, "pressure": 200.5},
                                                {"id": 2, "pressure": 160.5},
                                                {"id": 3, "pressure": key}]})
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["tire","id==3","pressure"],target_value=round(key*0.01,1))
    

    @allure.title("左前胎温")
    @pytest.mark.sanity
    def test_caseid_116059(self):
        self.soa.send_event_notify("TyreService_server", "AllTyreTemperature", 
                                       {"infos": [{"id": 0, "temperature": 30},
                                                {"id": 1, "temperature": 30},
                                                {"id": 2, "temperature": 30},
                                                {"id": 3, "temperature": 30}]})
        sleep(1)
        for key in [-50,32,205,25]:
            self.soa.send_event_notify("TyreService_server", "AllTyreTemperature", 
                                       {"infos": [{"id": 0, "temperature": key},
                                                {"id": 1, "temperature": 30},
                                                {"id": 2, "temperature": 30},
                                                {"id": 3, "temperature": 30}]})
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["tire","id==0","temperature"],target_value=key)


    @allure.title("右前胎温")
    @pytest.mark.sanity
    def test_caseid_112370(self):
        self.soa.send_event_notify("TyreService_server", "AllTyreTemperature", 
                                       {"infos": [{"id": 0, "temperature": 30},
                                                {"id": 1, "temperature":40},
                                                {"id": 2, "temperature": 30},
                                                {"id": 3, "temperature": 30}]})
        sleep(1)
        for key in [-50,32,205,25]:
            self.soa.send_event_notify("TyreService_server", "AllTyreTemperature", 
                                       {"infos": [{"id": 0, "temperature": 30},
                                                {"id": 1, "temperature": key},
                                                {"id": 2, "temperature": 30},
                                                {"id": 3, "temperature": 30}]})
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["tire","id==1","temperature"],target_value=key)


    @allure.title("左后胎温")
    @pytest.mark.sanity
    def test_caseid_112369(self):
        self.soa.send_event_notify("TyreService_server", "AllTyreTemperature", 
                                       {"infos": [{"id": 0, "temperature": 30},
                                                {"id": 1, "temperature":30},
                                                {"id": 2, "temperature": 50},
                                                {"id": 3, "temperature": 30}]})
        sleep(1)
        for key in [-50,32,205,25]:
            self.soa.send_event_notify("TyreService_server", "AllTyreTemperature", 
                                       {"infos": [{"id": 0, "temperature": 30},
                                                {"id": 1, "temperature": 30},
                                                {"id": 2, "temperature": key},
                                                {"id": 3, "temperature": 30}]})
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["tire","id==2","temperature"],target_value=key)


    @allure.title("右后胎温")
    @pytest.mark.sanity
    def test_caseid_112368(self):
        self.soa.send_event_notify("TyreService_server", "AllTyreTemperature", 
                                       {"infos": [{"id": 0, "temperature": 30},
                                                {"id": 1, "temperature":30},
                                                {"id": 2, "temperature": 30},
                                                {"id": 3, "temperature": 60}]})
        sleep(1)
        for key in [-50,32,205,25]:
            self.soa.send_event_notify("TyreService_server", "AllTyreTemperature", 
                                       {"infos": [{"id": 0, "temperature": 30},
                                                {"id": 1, "temperature": 30},
                                                {"id": 2, "temperature": 30},
                                                {"id": 3, "temperature": key}]})
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["tire","id==3","temperature"],target_value=key)


    @allure.title("档位")
    @pytest.mark.sanity
    def test_caseid_1918795(self):
        self.soa.send_event_notify("ChassisService_server", "Gear", {"gear": 0}) 
        sleep(1)
        for key in [3,1,2,0]:
            self.soa.send_event_notify("ChassisService_server", "Gear", {"gear": key})
            self.tsp.check_rvs_data_update_new(block=BlockName.DrivingStatus,keys=["gearLevel"],target_value=key)

    
    
    @allure.title("哨兵模式")
    @pytest.mark.full
    def test_caseid_112334(self):
        self.soa.send_event_notify("SentryModeService_server", "NotifySentryModeSts", {"sentryModeSts":{"mainSts":0,"workSts":0}})
        sleep(1)
        for key in [1,0]:
            self.soa.send_event_notify("SentryModeService_server", "NotifySentryModeSts", {"sentryModeSts":{"mainSts":key,"workSts":0}})

            self.tsp.check_rvs_data_update_new(block=BlockName.BusStatus,keys=["sentryModeStatus","mainStatus"],target_value=key)
        sleep(1)
        for key in [1,2,1,0]:
            self.soa.send_event_notify("SentryModeService_server", "NotifySentryModeSts", {"sentryModeSts":{"mainSts":0,"workSts":key}})
            self.tsp.check_rvs_data_update_new(block=BlockName.BusStatus,keys=["sentryModeStatus","workStatus"],target_value=key)



    @allure.title("账号Id和在线状态")
    @pytest.mark.full
    def test_caseid_109755_109716(self):
        self.soa.send_event_notify("AccountService_server", "NotifyAccountSts",
                                       {"sts": {"uid": 0, "token": "1"},
                                        "logInSts": 0})
        sleep(1)
        for key in [1,0]:
            self.soa.send_event_notify("AccountService_server", "NotifyAccountSts",
                                       {"sts": {"uid": 0, "token": "1"},
                                        "logInSts": key})
            self.tsp.check_rvs_data_update_new(block=BlockName.BusStatus,keys=["accountInfo","loginStatus"],target_value=key)
        sleep(1)
        self.soa.send_event_notify("AccountService_server", "NotifyAccountSts",
                                       {"sts": {"uid": 0, "token": "1"},
                                        "logInSts": 0})
        sleep(1)
        for key in [441020177218088450]:
            self.soa.send_event_notify("AccountService_server", "NotifyAccountSts",
                                       {"sts": {"uid": key, "token": "1"},
                                        "logInSts": 0})
            self.tsp.check_rvs_data_update_new(block=BlockName.BusStatus,keys=["accountInfo","uid"],target_value=4.4102017721808845e+17)
        self.soa.send_event_notify("AccountService_server", "NotifyAccountSts",
                                       {"sts": {"uid": 0, "token": "1"},
                                        "logInSts": 0})

    
    @allure.title("雨天自动关窗")
    @pytest.mark.full
    def test_caseid_112344(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_singal("bodycan","PdmBodyFr01","WinPosnStsAtPass",26)
        self.soa.send_event_notify("WiperService_server", "RainStatusRestricted", {"status": False})
        sleep(1)
        self.soa.send_event_notify("WiperService_server", "RainStatusRestricted", {"status": True})
        sleep(1)
        self.tsp.check_rvs_data_update_new(block=BlockName.BusStatus,keys=["remindInfo","rainStatusRestricted"],target_value=1)
        sleep(1)
        self.soa.send_event_notify("WiperService_server", "RainStatusRestricted", {"status": False})
        sleep(1)
        self.tsp.check_rvs_data_update_new(block=BlockName.BusStatus,keys=["remindInfo","rainStatusRestricted"],target_value=0)

    
    @allure.title("中控锁状态")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1990892(self):
        self.soa.send_event_notify("CentralLockService_server", "NotifyCentralLockSysInfo",  {"info": {"sts":0}})
        for key in [1,2,3,0]:
            self.soa.send_event_notify("CentralLockService_server", "NotifyCentralLockSysInfo",  {"info": {"sts":key}})
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["centralLock","status"],target_value=key)
    
    
    
    @allure.title("中控锁源")
    @pytest.mark.full
    @pytest.mark.v210
    def test_caseid_1990891(self):
        self.soa.send_event_notify("CentralLockService_server", "NotifyCentralLockSysInfo",  {"info": {"triggerId":2}})
        for key in range(0,13):
            self.soa.send_event_notify("CentralLockService_server", "NotifyCentralLockSysInfo",  {"info": {"triggerId":key}})
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["centralLock","triggerSourceId"],target_value=key)

    
    
    @allure.title("目标里程")
    @pytest.mark.sanity
    def test_caseid_1986515(self):
        self.soa.send_event_notify("HighVoltageService_server","NotifyRange",{"infos":{"type": 0,"targetRange":200}})
        for key in [0,100,999]:
            self.soa.send_event_notify("HighVoltageService_server","NotifyRange",{"infos":{"type": 0,"targetRange":key}})
            self.tsp.check_rvs_data_update_new(BlockName.EicCharging,keys=["charging", "chargeTargetMileage"], target_value=key,timeout=12)



    @allure.title("满充提醒")
    @pytest.mark.sanity
    def test_caseid_1987845(self):
        self.soa.send_event_notify("HighVoltageService_server","FullChargingRemind",{"info":{"remind":False}})
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","FullChargingRemind",{"info":{"remind":True}})
        self.tsp.check_rvs_data_update_new(BlockName.EicCharging,keys=["charging", "fullChargingRemind","remind"], target_value=True,timeout=12)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","FullChargingRemind",{"info":{"remind":False}})
        self.tsp.check_rvs_data_update_new(BlockName.EicCharging,keys=["charging", "fullChargingRemind","remind"], target_value=False,timeout=12)


    @allure.title("充电慢原因")
    @pytest.mark.sanity
    def test_caseid_1987840_1987839_1987838_1987837_1987836_1987835_1987834_1987833(self):
        self.soa.send_event_notify("HighVoltageService_server","ChargingSlowRemind",{"info":{"reasons":[0]}})
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","ChargingSlowRemind",{"info":{"reasons":[1]}})
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","reason"],target_value=[1],timeout=12)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","ChargingSlowRemind",{"info":{"reasons":[1,2]}})
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","reason"],target_value=[1,2],timeout=12)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","ChargingSlowRemind",{"info":{"reasons":[1,3]}})
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","reason"],target_value=[1,3],timeout=12)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","ChargingSlowRemind",{"info":{"reasons":[2,3]}})
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","reason"],target_value=[2,3],timeout=12)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","ChargingSlowRemind",{"info":{"reasons":[1,2,3]}})
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","reason"],target_value=[1,2,3],timeout=12)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","ChargingSlowRemind",{"info":{"reasons":[0]}})
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","reason"],target_value=[0],timeout=12)
        
    
    
    @allure.title("电池显示温度")
    @pytest.mark.sanity
    def test_caseid_1987841(self):
        self.soa.send_event_notify("HighVoltageService_server","ChargingSlowRemind",{"info":{"temperature":0}})
        sleep(1)
        for key in [-256,100,255.9]:
            self.soa.send_event_notify("HighVoltageService_server","ChargingSlowRemind",{"info":{"temperature":key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","temperature"],target_value=key,timeout=12)
            
    @allure.title("交直流设备属性")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1990885(self):
        self.soa.send_event_notify("HighVoltageService_server", "ChargingInfo",{"info":{"acdcType":0}})
        for key in [1,2,3,255,0]:
            self.soa.send_event_notify("HighVoltageService_server", "ChargingInfo",{"info":{"acdcType":key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","acdcType"],target_value=key,timeout=12
            )

    
    @allure.title("请求电流")
    @pytest.mark.full
    def test_caseid_1987844(self):
        self.soa.send_event_notify("HighVoltageService_server", "ChargingInfo",{"info":{"batteryReqCurrent":0}})
        for key in [20,819.1,0]:
            self.soa.send_event_notify("HighVoltageService_server", "ChargingInfo",{"info":{"batteryReqCurrent":key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","batteryReqCurrent"],target_value=key,timeout=12
            )


    @allure.title("数字钥匙id")
    @pytest.mark.sanity
    def test_caseid_112347(self):
        self.soa.send_event_notify("KeyService_server", "DigitalKeyConnectedStatus",{"status":[{"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0}]})
        sleep(1)
        for key in [[0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15]]:
            self.soa.send_event_notify("KeyService_server", "DigitalKeyConnectedStatus",{"status":[{"keyId": key,
                        "type": 2, "isConnected": True, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0}]})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.DeviceInfo,keys=["key","connectInfo","keyId"],target_value="AAECAwQFBgcICRAREhMUFQ==",timeout=8)
        self.soa.send_event_notify("KeyService_server", "DigitalKeyConnectedStatus",{"status":[{"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0}]})

    @allure.title("数字钥匙类型")
    @pytest.mark.full
    def test_caseid_112308(self):
        self.soa.send_event_notify("KeyService_server", "DigitalKeyConnectedStatus",{"status":[{"keyId": [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15],
                        "type": 2, "isConnected": True, "zone": 1},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0}]})
        for key in range(0,10):
            self.soa.send_event_notify("KeyService_server", "DigitalKeyConnectedStatus",{"status":[{"keyId": [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15],
                        "type": key, "isConnected": True, "zone": 1},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0}]})
            self.tsp.check_rvs_data_update_new(block=BlockName.DeviceInfo,keys=["key","connectInfo","keyType"],target_value=key)
    
    @allure.title("数字钥匙区域")
    @pytest.mark.full
    def test_caseid_1988838(self):
        self.soa.send_event_notify("KeyService_server", "DigitalKeyConnectedStatus",{"status":[{"keyId": [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15],
                        "type": 2, "isConnected": True, "zone": 1},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0}]})
        for key in range(0,17):
            self.soa.send_event_notify("KeyService_server", "DigitalKeyConnectedStatus",{"status":[{"keyId": [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15],
                        "type": 2, "isConnected": True, "zone": key},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0},
                       {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                        "type": 0, "isConnected": False, "zone": 0}]})
            self.tsp.check_rvs_data_update_new(block=BlockName.DeviceInfo,keys=["key","connectInfo","zone"],target_value=key)
    
    
    
    @allure.title("极速制冷状态")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1993239(self):
        self.soa.send_event_notify("ClimateControlService_server", "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})
        sleep(1)
        self.soa.send_event_notify("ClimateControlService_server", "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :True,"maxHeatingSts":False}})
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["coolingHeatingInfo","maxCoolingSts"],target_value=True)
        sleep(1)
        self.soa.send_event_notify("ClimateControlService_server", "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["coolingHeatingInfo","maxCoolingSts"],target_value=False)
        sleep(1)
        self.soa.send_event_notify("ClimateControlService_server", "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})
        sleep(1)
        self.soa.send_event_notify("ClimateControlService_server", "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":True}})
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["coolingHeatingInfo","maxHeatingSts"],target_value=True)
        sleep(1)
        self.soa.send_event_notify("ClimateControlService_server", "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["coolingHeatingInfo","maxHeatingSts"],target_value=False)
    
    @allure.title("热管理系统部件故障状态")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1993242(self):
        self.soa.send_event_notify("HighVoltageService_server", "ThermalSystemDeviceFaultInfo", 
                                                   {"infos": [{"device": 0, "faultSts": 0}, {"device": 255, "faultSts": 0}]})
        sleep(1)
        for key in [255,0,1,0]:
            self.soa.send_event_notify("HighVoltageService_server", "ThermalSystemDeviceFaultInfo", 
                                                   {"infos": [{"device": 0, "faultSts": 0}, {"device": 255, "faultSts": key}]})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["thermalSysDevFauSts"],target_value=key)
            
    
    @allure.title("更新充电速度范围0-9999")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_chargspeed_caseid_1993238(self):       
        self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"chargingState":0,"chargeSpeedCalculate":0}})
        sleep(1)        
        for key in [800,2100,6000,9999,0]:
            self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"chargingState":15,"chargeSpeedCalculate":key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargingSpeed"],target_value=key,timeout=12)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"chargingState":0,"chargeSpeedCalculate":0}})
        
    @allure.title("新增充电枪状态")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1990884(self):       
        self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"pluggerStatus":1}})
        sleep(1)        
        for key in range(0,12):
            self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"pluggerStatus":key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","pluggerStatus"],target_value=key,timeout=12
            )
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"pluggerStatus":0}})
        

    @allure.title("本次充电增加电量")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_112351(self):       
        self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"chargeEnergyThisTime":0}})
        sleep(1)        
        for key in [200000,100000,0]:
            self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"chargeEnergyThisTime":key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargeEgyThisTime"],target_value=key,timeout=12
            )
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"chargeEnergyThisTime":0}})
        

    @allure.title("充电增加里程")
    @pytest.mark.sanity
    @pytest.mark.v200
    def test_caseid_112349(self):
        self.soa.send_event_notify("HighVoltageService_server","NotifyRange",{"infos":{"type": 0,"CLTCRangeIncrease":200,"estimatedRangeIncrease":999}})
        sleep(1)
        for key in [0,100,999]:
            self.soa.send_event_notify("HighVoltageService_server","NotifyRange",{"infos":{"type": 0,"CLTCRangeIncrease":key,"estimatedRangeIncrease":999}})
            self.tsp.check_rvs_data_update_new(BlockName.EicCharging,keys=["charging", "incMileageThisTime"], target_value=key,timeout=12)

    
    @allure.title("充电桩实际输出电流按照1A的精度做变化上传")
    @pytest.mark.full
    def test_charg_actualcurrent_caseid_118664_1987848(self):
        self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
                                       {'info': {'actualCurrent': 0}})
        sleep(1)
        for key in [-1638,10,11,1638.7]:
            self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
                                       {'info': {'actualCurrent': key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","equipmentInfo","actualCurrent"],target_value=key,timeout=12
            )

    @allure.title("充电桩最大输出电流按照0.1 A的精度做变化上传")
    @pytest.mark.full
    @pytest.mark.v210
    def test_charg_maxcurrent_caseid_1993530(self):
        self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
                                       {'info': {'maxCurrent': 0}})
        sleep(1)
        for key in [-1638,10,10.1,1638.7]:
            self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
                                       {'info': {'maxCurrent': key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","equipmentInfo","maxCurrent"],target_value=key,timeout=12
            )


    @allure.title("充电桩实际输出电流按照0.1A的精度做变化上传")
    @pytest.mark.full
    @pytest.mark.v210
    def test_charg_actualcurrent_caseid_1993531(self):
        self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
                                       {'info': {'actualCurrent': 0}})
        sleep(1)
        for key in [-1638,100,100.2,1638.7]:
            self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
                                       {'info': {'actualCurrent': key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","equipmentInfo","actualCurrent"],target_value=key,timeout=12
            )


    @pytest.mark.sanity
    def test_chargTime_caseid_112353(self):
        self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"recentChargeStartTime":0}})
        sleep(1)
        for key in [1724904242463]:
            self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"recentChargeStartTime":key}})
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","recentChargeStartTime"],target_value=key,timeout=12)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"recentChargeEndTime":0}})
        sleep(1)
        for key in [1724904842000]:
            self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"recentChargeEndTime":key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","recentChargeEndTime"],target_value=key,timeout=12)
            

    @pytest.mark.sanity
    def test_chargbook_status_caseid_1981197(self):
        self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"bookChargests":0}})
        sleep(1)
        for key in [1,2,0]:
            self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"bookChargests":key}})
            self.tsp.check_rvs_data_update_new(
            BlockName.EicCharging,keys=["charging", "bookInfo", "bookStatus"], target_value=key,timeout=12)


    @pytest.mark.full
    def test_LightShowActive_caseid_1983453(self):
        self.soa.send_event_notify("LightService_server", "LightShowActivateStatus",
                                         {"status": 1})
        sleep(1)
        for key in range(3):
            self.soa.send_event_notify("LightService_server", "LightShowActivateStatus",
                                         {"status": key})
            self.tsp.check_rvs_data_update_new(
            BlockName.Light,keys=["showActive"], target_value=key,timeout=12)


    @allure.title("维持上电_车辆开始FOTA升级退出")
    @pytest.mark.sanity
    def test_caseid_1983499(self):
        self.soa.send_event_notify("VehicleSetStatusService_server", "ParkingComfortModeSts",
                                         {"sts":{"modeSts": 1,"reason":0}})
        sleep(1)
        self.soa.send_event_notify("VehicleSetStatusService_server", "ParkingComfortModeSts",
                                         {"sts":{"modeSts": 0,"reason":5}})
        self.tsp.check_rvs_data_update_new(BlockName.VehicleMode,keys=["parkingComfortMode","offReason"], target_value=5)


    @allure.title("10105,置信度")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1994886(self):
            self.soa.send_event_notify("LocationFusionService_server", "FusionLocationInfo", {"info":{"confidenceValue":0}})
            for key in [30,70,100,0]:
                sleep(5)
                self.soa.send_event_notify("LocationFusionService_server", "FusionLocationInfo", {"info":{"confidenceValue":key}})
                self.tsp.check_rvs_data_update_new(BlockName.GISAndTravel,keys=["gnss","confidenceOriginal"], target_value=key,timeout=7)
            sleep(5)
            self.soa.send_event_notify("LocationFusionService_server", "FusionLocationInfo", {"info":{"confidenceValue":101}})
            self.tsp.check_rvs_data_update_new(BlockName.GISAndTravel,keys=["gnss","confidenceOriginal"], target_value=0,timeout=7)

    @allure.title("10105,方向角")
    @pytest.mark.full
    @pytest.mark.v210
    def test_caseid_1994885(self):
            self.soa.send_event_notify("LocationFusionService_server", "FusionLocationInfo", {"info":{"yawValue":50.0}})
            for key in [80.0,180.0,0.0,360.0]:
                sleep(5)
                self.soa.send_event_notify("LocationFusionService_server", "FusionLocationInfo", {"info":{"yawValue":key}})
                self.tsp.check_rvs_data_update_new(BlockName.GISAndTravel,keys=["gnss","angle"], target_value=key,timeout=7)
            sleep(5)
            self.soa.send_event_notify("LocationFusionService_server", "FusionLocationInfo", {"info":{"yawValue":361}})
            self.tsp.check_rvs_data_update_new(BlockName.GISAndTravel,keys=["gnss","angle"], target_value=360.0,timeout=7)


    @allure.title("10105,定位时间戳")
    @pytest.mark.full
    @pytest.mark.v210
    def test_caseid_1994883(self):
            self.soa.send_event_notify("LocationFusionService_server", "FusionLocationInfo", {"info":{"timeStampValue":1727662339}})
            sleep(5)
            for key in [1727343263000,1727344208000]:
                sleep(5)
                self.soa.send_event_notify("LocationFusionService_server", "FusionLocationInfo", {"info":{"timeStampValue":key}})
                self.tsp.check_rvs_data_update_new(BlockName.GISAndTravel,keys=["gnss","timestamp"], target_value=key,timeout=7)


    @allure.title("10105,经纬度") 
    @pytest.mark.full
    @pytest.mark.v210
    def test_caseid_1994884(self):
            self.soa.send_event_notify("LocationFusionService_server", "FusionLocationInfo", {"info":{"gcj02lontitudeValue":114.51290771484375,"gcj02latitudeValue":30.49212727864583}})
            sleep(5)
            self.soa.send_event_notify("LocationFusionService_server", "FusionLocationInfo", {"info":{"gcj02lontitudeValue":121.499718,"gcj02latitudeValue": 31.239703}})
            self.tsp.check_rvs_data_update_new(BlockName.GISAndTravel,keys=["gnss","longitude"], target_value=121.499718,timeout=7)
            self.tsp.check_rvs_data_update_new(BlockName.GISAndTravel,keys=["gnss","latitude"], target_value=31.239703,timeout=7)
            sleep(5)
            self.soa.send_event_notify("LocationFusionService_server", "FusionLocationInfo", {"info":{"gcj02lontitudeValue":114.51290771484375,"gcj02latitudeValue":30.49212727864583}})
            self.tsp.check_rvs_data_update_new(BlockName.GISAndTravel,keys=["gnss","longitude"], target_value=114.51290771484375,timeout=7)
            self.tsp.check_rvs_data_update_new(BlockName.GISAndTravel,keys=["gnss","latitude"], target_value=30.49212727864583,timeout=7)


    # @allure.title("10105,海外版本新增云配置开关-关闭经纬度") 
    # @pytest.mark.sanity
    # @pytest.mark.v220
    # def test_caseid_210210(self):
    #         self.soa.send_event_notify("LocationFusionService_server", "FusionLocationInfo", {"info":{"gcj02lontitudeValue":114.51290771484375,"gcj02latitudeValue":30.49212727864583}})
    #         sleep(5)
    #         self.soa.send_event_notify("LocationFusionService_server", "FusionLocationInfo", {"info":{"gcj02lontitudeValue":121.499718,"gcj02latitudeValue": 31.239703}})
    #         self.tsp.check_rvs_data_update_new(BlockName.GISAndTravel,keys=["gnss","longitude"], target_value=1.7976931348623157E308,timeout=7)
    #         self.tsp.check_rvs_data_update_new(BlockName.GISAndTravel,keys=["gnss","latitude"], target_value=1.7976931348623157E308,timeout=7)
    #         sleep(5)
    #         self.soa.send_event_notify("LocationFusionService_server", "FusionLocationInfo", {"info":{"gcj02lontitudeValue":114.51290771484375,"gcj02latitudeValue":30.49212727864583}})
    #         self.tsp.check_rvs_data_update_new(BlockName.GISAndTravel,keys=["gnss","longitude"], target_value=1.7976931348623157E308,timeout=7)
    #         self.tsp.check_rvs_data_update_new(BlockName.GISAndTravel,keys=["gnss","latitude"], target_value=1.7976931348623157E308,timeout=7)
    
    
    @allure.title("更新充电速度范围0-9999")
    @pytest.mark.sanity
    @pytest.mark.v220
    def test_chargspeed_caseid_1995973(self):       
        self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"isCharging":False,"chargeSpeedCalculate":0}})
        sleep(1)        
        for key in [800,2100,6000,9999,0]:
            self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
                                       {"info":{"isCharging":True,"chargeSpeedCalculate":key}})
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargingSpeed"],target_value=key,timeout=12)
        # sleep(1)
        # self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
        #                                {"info":{"isCharging":False,"chargeSpeedCalculate":0}})
        # for key in [800,2100,6000,9999,0]:
        #     self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
        #                                {"info":{"isCharging":False,"chargeSpeedCalculate":key}})
    
  

    @pytest.mark.sanity
    @pytest.mark.v220
    def test_DisChargingState_caseid_1995990(self):
        '''放电状态 '''
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargingState": 1}})
        sleep(1)
        for key in range(0,7):
            self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargingState": key}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["disChargingInfo","disChargingState"],target_value=key)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargingState": 0}})
        

    @pytest.mark.sanity
    @pytest.mark.v220
    def test_isConnect_caseid_1995989(self):
        '''是否连接放电枪 '''
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"isConnect": False}})
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"isConnect": True}})
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["disChargingInfo","isConnect"],target_value=True)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"isConnect": False}})
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["disChargingInfo","isConnect"],target_value=False)
        


    @pytest.mark.sanity
    @pytest.mark.v220
    def test_dischargeLimitSoc_caseid_1995988(self):
        '''放电限值SOC '''
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargeLimitSoc": 50.0}})
        sleep(1)
        for key in [20.0,20.2,100,20.0,255,0]:
            self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargeLimitSoc": key}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["disChargingInfo","dischargeLimitSoc"],target_value=key)
        # sleep(1)
        # for key in [30.0,30.05]:
        #     self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
        #                                {"info": {"dischargeLimitSoc": key}})
        #     self.tsp.check_rvs_data_update_new(
        #          block=BlockName.EicCharging,keys=["disChargingInfo","dischargeLimitSoc"],target_value=key)
    

    @pytest.mark.sanity
    @pytest.mark.v220
    def test_isDischargingPreparing_caseid_1995987(self):
        '''放电准备中 '''
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"isDischargingPreparing": False}})
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"isDischargingPreparing": True}})
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["disChargingInfo","isDischargingPreparing"],target_value=True)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"isDischargingPreparing": False}})
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["disChargingInfo","isDischargingPreparing"],target_value=False)
        

    @pytest.mark.full
    @pytest.mark.v220
    def test_recentDischargeStartTime_caseid_1995986(self):
        '''最近一次放电的开始时间 '''
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"recentDischargeStartTime": 0}})
        sleep(1)
        for key in [1728633910,1728634025,0]:
            self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"recentDischargeStartTime": key}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["disChargingInfo","recentDischargeStartTime"],target_value=key,timeout=12)
    

    @pytest.mark.full
    @pytest.mark.v220
    def test_recentDischargeEndTime_caseid_1995985(self):
        '''最近一次放电的结束时间 '''
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"recentDischargeEndTime": 0}})
        sleep(1)
        for key in [1728655800,1728656400,0]:
            self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"recentDischargeEndTime": key}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["disChargingInfo","recentDischargeEndTime"],target_value=key,timeout=12)


    @pytest.mark.full
    @pytest.mark.v220
    def test_dischargingLeftTime_caseid_1995984(self):
        '''剩余放电时间 '''
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargingLeftTime": 0}})
        sleep(1)
        for key in [600,500,0,-1]:
            self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargingLeftTime": key}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["disChargingInfo","dischargeLeftTime"],target_value=key,timeout=12)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargingLeftTime": 0}})



    @pytest.mark.full
    @pytest.mark.v220
    def test_dischargeEnergyThisTime_caseid_1995983(self):
        '''本次放电电量 '''
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargeEnergyThisTime": 0}})
        sleep(1)
        for key in [100000,100001,200000,200001,-1]:
            self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargeEnergyThisTime": key}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["disChargingInfo","dischargeEnergyThisTime"],target_value=key,timeout=12)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargeEnergyThisTime": 0}})


    @pytest.mark.full
    @pytest.mark.v220
    def test_dischargeCurrent_caseid_1995982(self):
        '''放电电流 '''
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargeCurrent": 0}})
        sleep(1)                              
        for key in [100,100.2,200,200.1,0,-1]:
            self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargeCurrent": key}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["disChargingInfo","dischargeCurrent"],target_value=key,timeout=12)
        # sleep(1)
        # for key in [150,150.05]:
        #     self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
        #                                {"info": {"dischargeCurrent": key}})
        #     self.tsp.check_rvs_data_update_new(
        #          block=BlockName.EicCharging,keys=["disChargingInfo","dischargeCurrent"],target_value=key,timeout=10)


    @pytest.mark.full
    @pytest.mark.v220
    def test_dischargePower_caseid_1995981(self):
        '''放电输出功率 '''
        self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargePower": 0}})
        sleep(1)
        for key in [10000,10001,51100,51200,0,-1]:
            self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
                                       {"info": {"dischargePower": key}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["disChargingInfo","dischargePower"],target_value=key,timeout=12)
        # sleep(1)
        # for key in [20000,20000.5]:
        #     self.soa.send_event_notify("HighVoltageService_server","DischargingInfo",
        #                                {"info": {"dischargePower": key}})
        #     self.tsp.check_rvs_data_update_new(
        #          block=BlockName.EicCharging,keys=["disChargingInfo","dischargePower"],target_value=key,timeout=10)


    @pytest.mark.sanity
    @pytest.mark.v220
    def test_ACBookChargingReqSts_caseid_1995980(self):
        '''预约充电请求状态（交流设置） '''
        self.soa.send_event_notify("HighVoltageAppService_server","BookChargingInfo",{"info":{"acInfo":{"reqSts":1}}})
        sleep(1)
        for key in range(0,4):
            self.soa.send_event_notify("HighVoltageAppService_server","BookChargingInfo",{"info":{"acInfo":{"reqSts":key}}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","acInfo","reqSts"],target_value=key)
        sleep(1)
        self.soa.send_event_notify("HighVoltageAppService_server","BookChargingInfo",{"info":{"acInfo":{"reqSts":0}}}) 



    @pytest.mark.sanity
    @pytest.mark.v220
    def test_BookChargingTime_caseid_1995979(self):
        '''预约充电开始与结束时间（交流设置）'''
        self.soa.send_event_notify("HighVoltageAppService_server","BookChargingInfo",{"info":{"acInfo":{"reqSts":0,
                                                                    "info":{"startTime":1609509600,"endTime":1609538400},
                                                                    "isToTargetSOCStop":False}}})
        sleep(1)                                                           
        for key in [1728914400,1728901500,1728991500,1728914400]:
            self.soa.send_event_notify("HighVoltageAppService_server","BookChargingInfo",{"info":{"acInfo":{"reqSts":1,
                                                                    "info":{"startTime":key,"endTime":1609538400},
                                                                    "isToTargetSOCStop":True}}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","acInfo","info","startTime"],target_value=key)
        sleep(1)
        self.soa.send_event_notify("HighVoltageAppService_server","BookChargingInfo",{"info":{"acInfo":{"reqSts":0,
                                                                    "info":{"startTime":1609509600,"endTime":1609538400},
                                                                    "isToTargetSOCStop":False}}})
        sleep(1)                                                           
        for key in [1728943200,1728948180,1729038180,1728943200]:
            self.soa.send_event_notify("HighVoltageAppService_server","BookChargingInfo",{"info":{"acInfo":{"reqSts":1,
                                                                    "info":{"startTime":1609509600,"endTime":key},
                                                                    "isToTargetSOCStop":True}}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","acInfo","info","endTime"],target_value=key)
        sleep(1)
        self.soa.send_event_notify("HighVoltageAppService_server","BookChargingInfo",{"info":{"acInfo":{"reqSts":0,
                                                                    "info":{"startTime":1609509600,"endTime":1609538400},
                                                                    "isToTargetSOCStop":False}}})


    

    @pytest.mark.sanity
    @pytest.mark.v220
    def test_isToTargetSOCStop_caseid_1995978(self):
        '''交流预约结束类型（是否充满为止） '''
        self.soa.send_event_notify("HighVoltageAppService_server","BookChargingInfo",{"info":{"acInfo":{"isToTargetSOCStop":False}}})
        sleep(1)
        self.soa.send_event_notify("HighVoltageAppService_server","BookChargingInfo",{"info":{"acInfo":{"isToTargetSOCStop":True}}})
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","acInfo","isToTargetSOCStop"],target_value=True)
        sleep(1)
        self.soa.send_event_notify("HighVoltageAppService_server","BookChargingInfo",{"info":{"acInfo":{"isToTargetSOCStop":False}}})
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","acInfo","isToTargetSOCStop"],target_value=False) 
    
    

    @pytest.mark.sanity
    @pytest.mark.v220
    def test_DisplayBookChargingType_caseid_1995977(self):
        '''显示预约充电类型 '''
        self.soa.send_event_notify("HighVoltageAppService_server","DisplayBookChargingInfo", {"info":{"type":1}})
        sleep(1)
        for key in [0,1,2,0]:
            self.soa.send_event_notify("HighVoltageAppService_server","DisplayBookChargingInfo", {"info":{"type":key}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","type"],target_value=key) 

    
    
    @pytest.mark.sanity
    @pytest.mark.v220
    def test_DisplayBook_startTime_caseid_1995976(self):
        '''预约充电显示开始时间 '''
        self.soa.send_event_notify("HighVoltageAppService_server","DisplayBookChargingInfo", {"info":{"type":1,"startTime":{"kYear":2024,"kMonth":10,
                                                                 "kDay":30,"kHour":24,"kMinute":60},
                                           "endTime":{"kYear":2024,"kMonth":10,
                                                      "kDay":30,"kHour":24,"kMinute":60}}})
        sleep(1)
        for key in [0,16,24,25]:
            self.soa.send_event_notify("HighVoltageAppService_server","DisplayBookChargingInfo", {"info":{"type":1,"startTime":{"kYear":2024,"kMonth":10,
                                                                 "kDay":30,"kHour":key,"kMinute":60},
                                           "endTime":{"kYear":2024,"kMonth":10,
                                                      "kDay":30,"kHour":24,"kMinute":60}}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","bookInfo","startHour"],target_value=key)
        sleep(1)
        for key in [0,16,60,61]:
            self.soa.send_event_notify("HighVoltageAppService_server","DisplayBookChargingInfo", {"info":{"type":1,"startTime":{"kYear":2024,"kMonth":10,
                                                                 "kDay":30,"kHour":24,"kMinute":key},
                                           "endTime":{"kYear":2024,"kMonth":10,
                                                      "kDay":30,"kHour":24,"kMinute":60}}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","bookInfo","startMinute"],target_value=key)




    @pytest.mark.sanity
    @pytest.mark.v220
    def test_DisplayBook_endTime_caseid_1995975(self):
        '''预约充电显示结束时间 '''
        self.soa.send_event_notify("HighVoltageAppService_server","DisplayBookChargingInfo", {"info":{"type":1,"startTime":{"kYear":2024,"kMonth":10,
                                                                 "kDay":30,"kHour":24,"kMinute":60},
                                           "endTime":{"kYear":2024,"kMonth":10,
                                                      "kDay":30,"kHour":24,"kMinute":60}}})
        sleep(1)
        for key in [0,18,24,25]:
            self.soa.send_event_notify("HighVoltageAppService_server","DisplayBookChargingInfo", {"info":{"type":1,"startTime":{"kYear":2024,"kMonth":10,
                                                                 "kDay":30,"kHour":24,"kMinute":60},
                                           "endTime":{"kYear":2024,"kMonth":10,
                                                      "kDay":30,"kHour":key,"kMinute":60}}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","bookInfo","endHour"],target_value=key)
        sleep(1)
        for key in [0,20,60,61]:
            self.soa.send_event_notify("HighVoltageAppService_server","DisplayBookChargingInfo", {"info":{"type":1,"startTime":{"kYear":2024,"kMonth":10,
                                                                 "kDay":30,"kHour":24,"kMinute":60},
                                           "endTime":{"kYear":2024,"kMonth":10,
                                                      "kDay":30,"kHour":24,"kMinute":key}}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","bookInfo","endMinute"],target_value=key)
            


    @pytest.mark.full
    @pytest.mark.v200
    def test_BookChargingType_caseid_1996909(self):
        '''预约充电类型 '''
        self.soa.send_event_notify("HighVoltageService_server","BookChargingTime", {"info":{"type":1}})
        sleep(1)
        for key in [0,1,2]:
            self.soa.send_event_notify("HighVoltageService_server","BookChargingTime", {"info":{"type":key}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","bookInfo","bookType"],target_value=key)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","BookChargingTime", {"info":{"type":3}})
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","bookInfo","bookType"],target_value=-1)


    # @allure.title("本次充电增加里程")
    # @pytest.mark.sanity
    # def test_incMileageThisTime_caseid_1986514(self):
    #     self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
    #                                    {"info":{"isCharging":True}})
    #     sleep(1)        
    #     self.soa.send_event_notify("HighVoltageService_server", "NotifyRange",
    #                                    {"info":{"type":0,"CLTCRangeIncrease":100}})
    #     sleep(10)        
    #     for key in [0,200,999]:
    #         self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
    #                                    {"info":{"isCharging":True}})
    #         sleep(1)
    #         self.soa.send_event_notify("HighVoltageService_server", "NotifyRange",
    #                                    {"info":{"type":0,"CLTCRangeIncrease":key}})
    #         self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging", "incMileageThisTime"],target_value=key,timeout=12)



    @pytest.mark.sanity
    @pytest.mark.v220
    def test_chargeVoltageInput_caseid_1996911(self):
        '''充电桩输入电压 '''
        self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
                                       {'info': {'chargeVoltageInput': 100}})
        sleep(1)
        for key in [0,511,1023,1023.2,-1,0]:
            sleep(5)
            self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
                                       {'info': {'chargeVoltageInput': key}})
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","equipmentInfo","chargeVoltageInput"],target_value=key,timeout=12)
        # sleep(1)
        # for key in [511,511.05]:
        #     self.soa.send_event_notify("HighVoltageService_server","NotifyChargingEquipmentInformation",
        #                                {'info': {'chargeVoltageInput': key}})
        #     self.tsp.check_rvs_data_update_new(
        #          block=BlockName.EicCharging,keys=["charging","bookInfo","bookType"],target_value=-1)



    @pytest.mark.sanity
    @pytest.mark.v220
    def test_isInhibitByHVBoost_caseid_1996912(self):
        '''升压充电导致禁用信息 '''
        self.soa.send_event_notify("HighVoltageService_server","ChargingInhibitInfo",
                                       {'info': {'isInhibitByHVBoost': False}})
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","ChargingInhibitInfo",
                                       {'info': {'isInhibitByHVBoost': True}})
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","chargingInhibitInfo","isInhibitByHVBoost"],target_value=True)
        sleep(1)
        self.soa.send_event_notify("HighVoltageService_server","ChargingInhibitInfo",
                                       {'info': {'isInhibitByHVBoost': False}})
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.EicCharging,keys=["charging","chargingInhibitInfo","isInhibitByHVBoost"],target_value=False)


    @allure.title("充电口盖关闭失败 ,WTI-772")
    @pytest.mark.full
    def test_caseid_1997109(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "ChargeLidCloseFailed",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "ChargeLidCloseFailed",'info':"1"}]})
        assert self.tsp.log_search_wti(wtiKey="ChargeLidCloseFailed",wtiFlag=1)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "ChargeLidCloseFailed",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="ChargeLidCloseFailed",wtiFlag=0)


    @allure.title("清洗液液位低,WTI-2351")
    @pytest.mark.full
    def test_caseid_1997110(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Wiper Liquid",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Wiper Liquid",'info':"1"}]})
        assert self.tsp.log_search_wti(wtiKey="Wiper Liquid",wtiFlag=1)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Wiper Liquid",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Wiper Liquid",wtiFlag=0)


    @pytest.mark.full
    def test_MaintenanceMode_caseid_1983456(self):
        '''维修模式 '''
        self.soa.send_event_notify("VehicleSetStatusService_server","NotifyMaintenanceMode",
                                       {'mode': False})
        sleep(1)
        self.soa.send_event_notify("VehicleSetStatusService_server","NotifyMaintenanceMode",
                                       {'mode': True})
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.VehicleMode,keys=["maintenanceMode"],target_value=11,timeout=5)
        self.soa.send_event_notify("VehicleSetStatusService_server","NotifyMaintenanceMode",
                                       {'mode': False})
        sleep(1)
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.VehicleMode,keys=["maintenanceMode"],target_value=10,timeout=5)
        
    
    @allure.title("两个踏板同时被踩下，动力输出受限,WTI-2362")
    @pytest.mark.full
    def test_caseid_1994671(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Brake Overide Accelerator",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Brake Overide Accelerator",'info':"1"}]})
        assert self.tsp.log_search_wti(wtiKey="Brake Overide Accelerator",wtiFlag=1)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Brake Overide Accelerator",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Brake Overide Accelerator",wtiFlag=0)


    @allure.title("请先挂挡再驾驶车辆,WTI-2361")
    @pytest.mark.full
    def test_caseid_1994670(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Shift Reminder",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Shift Reminder",'info':"1"}]})
        assert self.tsp.log_search_wti(wtiKey="Shift Reminder",wtiFlag=1)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Shift Reminder",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Shift Reminder",wtiFlag=0)

    
    @allure.title("踩下刹车过久，完全松一次刹车再换挡,WTI-2375")
    @pytest.mark.full
    def test_caseid_1994669(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Release Brake Reminder",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Release Brake Reminder",'info':"1"}]})
        assert self.tsp.log_search_wti(wtiKey="Release Brake Reminder",wtiFlag=1)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Release Brake Reminder",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Release Brake Reminder",wtiFlag=0)
    
    
    @allure.title("副驾或后排安全带未系提醒,WTI-2384")
    @pytest.mark.full
    def test_caseid_1994633(self):
        self.soa.send_event_notify("WTIAutoDriveService_server","WarningMsgList",
                                       {'list': [{'name': "Auto Driving Belt Unfasten Reminder",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIAutoDriveService_server","WarningMsgList",
                                       {'list': [{'name': "Auto Driving Belt Unfasten Reminder",'info':"1"}]})
        assert self.tsp.log_search_wti(wtiKey="Auto Driving Belt Unfasten Reminder",wtiFlag=1)
        sleep(1)
        self.soa.send_event_notify("WTIAutoDriveService_server","WarningMsgList",
                                       {'list': [{'name': "Auto Driving Belt Unfasten Reminder",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Auto Driving Belt Unfasten Reminder",wtiFlag=0)
    
    
    @allure.title("这里空间有点窄，将临时收起后视镜继续泊车,WTI-2353")
    @pytest.mark.full
    def test_caseid_1994621(self):
        self.soa.send_event_notify("WTIAutoDriveService_server","WarningMsgList",
                                       {'list': [{'name': "APA TTS",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIAutoDriveService_server","WarningMsgList",
                                       {'list': [{'name': "APA TTS",'info':"70"}]})
        assert self.tsp.log_search_wti(wtiKey="APA TTS",wtiFlag=70)
        sleep(1)
        self.soa.send_event_notify("WTIAutoDriveService_server","WarningMsgList",
                                       {'list': [{'name': "APA TTS",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="APA TTS",wtiFlag=0)
    
    
    @allure.title("我退出自动泊车了，因为暂停时间超过了五分钟,WTI-2346")
    @pytest.mark.full
    def test_caseid_1990881(self):
        self.soa.send_event_notify("WTIAutoDriveService_server","WarningMsgList",
                                       {'list': [{'name': "APA TTS",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIAutoDriveService_server","WarningMsgList",
                                       {'list': [{'name': "APA TTS",'info':"69"}]})
        assert self.tsp.log_search_wti(wtiKey="APA TTS",wtiFlag=69)
        sleep(1)
        self.soa.send_event_notify("WTIAutoDriveService_server","WarningMsgList",
                                       {'list': [{'name': "APA TTS",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="APA TTS",wtiFlag=0)
    

    @allure.title("离车自动落锁关门提示-车外,WTI-2313")
    @pytest.mark.full
    def test_caseid_1990863(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Cannot unLock",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Cannot unLock",'info':"3"}]})
        assert self.tsp.log_search_wti(wtiKey="Cannot unLock",wtiFlag=3)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Cannot unLock",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Cannot unLock",wtiFlag=0)


    @allure.title("主驾无线充电故障状态提示：内部故障,WTI-1356")
    @pytest.mark.full
    def test_caseid_1986505(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Driver Wireless Charging Remind",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Driver Wireless Charging Remind",'info':"5"}]})
        assert self.tsp.log_search_wti(wtiKey="Driver Wireless Charging Remind",wtiFlag=5)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Driver Wireless Charging Remind",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Driver Wireless Charging Remind",wtiFlag=0)


    
    @allure.title("副驾无线充电故障状态提示：内部故障,WTI-2195")
    @pytest.mark.full
    def test_caseid_1986504(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Passenger Wireless Charging Remind",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Passenger Wireless Charging Remind",'info':"5"}]})
        assert self.tsp.log_search_wti(wtiKey="Passenger Wireless Charging Remind",wtiFlag=5)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Passenger Wireless Charging Remind",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Passenger Wireless Charging Remind",wtiFlag=0)


    @allure.title("请关好所有车门和前盖,WTI-2299")
    @pytest.mark.full
    def test_caseid_1986503(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"2"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=2)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=0)


    @allure.title("请切换到D档,WTI-2296")
    @pytest.mark.full
    def test_caseid_1986502(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"4"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=4)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=0)


    @allure.title("WTI-2300,请系好安全带")
    @pytest.mark.full
    def test_caseid_1986501(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"3"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=3)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=0)


    @allure.title("WTI-2301,请回正方向盘")
    @pytest.mark.full
    def test_caseid_1986500(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"5"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=5)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=0)


    @allure.title("请深踩制动踏板,WTI-2302")
    @pytest.mark.full
    def test_caseid_1986499(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"6"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=6)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=0)


    @allure.title("请深踩加速踏板,WTI-2303")
    @pytest.mark.full
    def test_caseid_1986498(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"7"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=7)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=0)
    
    
    @allure.title("请松开制动踏板以弹射,WTI-2304")
    @pytest.mark.full
    def test_caseid_1986497(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"8"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=8)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=0)


    @allure.title("请驾驶车辆至平地,WTI-2298")
    @pytest.mark.full
    def test_caseid_1986496(self):
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"1"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=1)
        sleep(1)
        self.soa.send_event_notify("WTIService_server","WarningMsgList",
                                       {'list': [{'name': "Launch Mode Operation Reminder",'info':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="Launch Mode Operation Reminder",wtiFlag=0)


    

    