#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_KeyService.py
@Time         :2023/04/08 17:20:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
from datetime import datetime, timedelta
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_cases.legacy.soa.case_helper.gnss_server import GNSSServiceServer
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester


GNSS_SERVICE_SERVER_HD = "GNSSService_server_GNSSService_HD"


def handle_utctime(ori_date: int, ori_time: int, detal_time: timedelta, action="add"):
    """
    处理utctime
    @param ori_date: 原始日期，ddmmyy（日月年）格式
    @param ori_time: 原始时间，hhmmsssss，后三位为毫秒
    @param detal_time: timedelta对象
    @param action: 加减操作，默认加
    return: 新计算的ori_date和ori_time
    """
    timestr = str(ori_time)
    sss = int(timestr[-3:])
    ss = int(timestr[-5: -3])
    mm = int(timestr[-7: -5])
    hh = int(timestr[0: -7])

    datestr = str(ori_date)
    yy = int(datestr[-2:])
    MM = int(datestr[-4: -2])
    dd = int(datestr[-6: -4])

    ori_datetime = datetime(year=yy, month=MM, day=dd, hour=hh, minute=mm, second=ss, microsecond=sss * 1000)

    new = ori_datetime + detal_time
    return int(f"{new.day:02d}{new.month:02d}{new.year:02d}"), int(f"{new.hour:02d}{new.minute:02d}{new.second:02d}{new.microsecond//1000:03d}")


@allure.feature("SOA服务接口")
@allure.story("架构基础/TimeManagementService")
@pytest.mark.zjb
class TestTimeManagementServiceTcamOnline(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD"), # GNSSService为TCAM的服务端，GNSSService_HD为ACU的服务端
            ("VehicleTimeService", "client")
        ])
        self.partner.GNSSStatus = 1
        self.partner.UTCDate = 150823
        self.partner.UTCTime = 101525000
        self.partner.longitude = 121.4  # 上海的位置 经度
        self.partner.latitude = 31.2 # 纬度
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD)
        self.partner.wait_for_service_reconnect(VEHICLETIME_SERVICE_CLIENT)
        self.partner.unregister_event(VEHICLETIME_SERVICE_CLIENT)
        sleep(1)
        self.partner.register_event(VEHICLETIME_SERVICE_CLIENT)
        sleep(1)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
    
    @allure.title("启动后RTC授时->NTP授时并触发通知网络时间和系统时间偏差")
    @pytest.mark.smoke
    def test_caseid_1984285(self): # TCAM在线，BGM诊断重启
        self.sd_tester.reset_ecu()
        self.partner.empty_all()
        self.partner.wait_for_service_reconnect(VEHICLETIME_SERVICE_CLIENT)
        # 启动后授时谁先到，上报谁的数据，不一定肯定有2
        # 台架如果GNSS好的话，可能会比RTC或NTP来的早
        info1 = self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo", {}, timeout=5)["info"]
        status1=  info1["SynchronizationStatus"]
        utc_datetime = datetime.now() - timedelta(hours=8)
        exp_UTCData = int(f"{utc_datetime.day:02d}{utc_datetime.month:02d}{str(utc_datetime.year)[-2:]}")
        if status1 == 0: # 无效数据，继续等授时
            info1 = self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo", {}, timeout=5)["info"]
            status1=  info1["SynchronizationStatus"]

        if status1 == 2: # 如果先来2了，那就等3或4进行时间偏差计算
            # 此处超时60s是因为NTP为网络时间，与网络好坏有关系
            status2 = self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",  {}, timeout=200)["info"]["SynchronizationStatus"]
            if status2 not in [3, 4]:
                # 存在重启后上报两次SynchronizationStatus=2的情况，时间同步前/后发生；
                # 会在时间同步时上报一次event；拿本地持久化时区时上报一次event；
                status2 = self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo",  {}, timeout=200)["info"]["SynchronizationStatus"]
            assert status2 in [3, 4]

            time1 = self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "NetAndSysTimeDeviation", {})["time"]
            assert -300 <time1 < 2000  # 出现负数是因为时间精度的问题
            self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetNetAndSysTimeDeviation", {},
                                                  {"out": time1})
            
        elif status1 == 4: # GNSS先来，那1s后就直接计算时间偏差了
            time1 = self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "NetAndSysTimeDeviation", {})["time"]
            assert -300 <time1 < 1500
            self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetNetAndSysTimeDeviation", {},
                                                    {"out": time1})
            
        else: # 若重启后先收到了NTP的VehicleTimeInfo上报
            try:
                time1 = self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "NetAndSysTimeDeviation", {}, timeout=20)["time"]
                assert -300 <time1 < 1500
                self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetNetAndSysTimeDeviation", {},
                                                        {"out": time1})        
            except Exception as e: # 若收不到TCAM的GNSS时间，那可以通过GNSS_HD注入
                self.partner.UTCDate, self.partner.UTCTime = handle_utctime(exp_UTCData, info1['UTCTime'], timedelta(seconds=20))
                self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation",
                                               {"gnssInfo": self.partner.gnss_info})
                time1 = self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "NetAndSysTimeDeviation", {}, timeout=20)["time"]
                assert -300 <time1 < 1500
                self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetNetAndSysTimeDeviation", {},
                                                        {"out": time1})       
                pass
        
    @allure.title("启动后无RTC授时->NTP授时->GNSS授时并触发通知网络时间和系统时间偏差")
    @pytest.mark.smoke
    def test_caseid_1919335(self): # TCAM在线，BGM上下电重启，即无RTC授时
        # 用例步骤1
        self.partner.longitude = 121.4  # 上海的位置
        self.partner.latitude = 31.2
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation",
                                       {"gnssInfo": self.partner.gnss_info})
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.partner.start_single_partner("GNSSService", "server", "GNSSService_HD")
        sleep(1)
        # 上下电mcu不会存RTC时间，重启后mcu上行的时间是默认时间，Mpu不认为是有效时间，不会进行授时
        self.restart_bgm_and_connect_service(VEHICLETIME_SERVICE_CLIENT)
        utc_datetime = datetime.now() - timedelta(hours=8)
        exp_UTCData = int(f"{utc_datetime.day:02d}{utc_datetime.month:02d}{str(utc_datetime.year)[-2:]}")
        # 此处考虑台架环境TCAM的GNSS获取不到数据的情况，如果台架能获取到GNSS则下面同步源为4，属于正常情况
        # 且TimeManager会1s一次去获取GNSS时间，第一次拿到时间会设置系统时间并更新mcu的RTC时间，第二次拿到计算NetAndSysTimeDeviation

        # 上电后拿系统时间
        info1 = self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo", 
                                          {"info": {"UTCData": exp_UTCData, "TimeZone":8, "politicalTimeZone": "Asia/Shanghai"}}, timeout=60)["info"]
        # 拿到第一个外部时间不会计算时间偏差，调用get获取到默认值
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetNetAndSysTimeDeviation", {},
                                              {"out": 0x7FFFFFFF})
        if info1["SynchronizationStatus"] == 0:
            info1 = self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo", {}, timeout=5)["info"]
        UTCTime, SynchronizationStatus = info1['UTCTime'], info1['SynchronizationStatus']
        if SynchronizationStatus == 4:
            # 说明当前环境GNSS能接收到数据，时间偏差无法通过GNSS_HD进行注入测试
            time1 = self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "NetAndSysTimeDeviation", {})["time"]
            assert -300 <time1 < 1500

            timeinfo = self.partner.send_request_and_return_resp(VEHICLETIME_SERVICE_CLIENT,    
                                                             "GetVehicleTimeInfo", {})['out']
            ck_data(timeinfo, {"UTCData": exp_UTCData, "TimeZone": 8, "SynchronizationStatus": 4, "politicalTimeZone": "Asia/Shanghai"})
            assert 700 < timeinfo['UTCTime'] - UTCTime < 1300  # 两次GNSS周期相差1s，偏差值给了300ms
        else:  # 无GNSS，那可以通过GNSS_HD注入，说明前面来的NTP
            # 用例步骤2
            self.partner.empty_all()
            self.partner.UTCDate, self.partner.UTCTime = handle_utctime(exp_UTCData, UTCTime, timedelta(seconds=5))
            self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation",
                                        {"gnssInfo": self.partner.gnss_info})
            time1 = self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "NetAndSysTimeDeviation", {})["time"]
            assert 4000 < time1 < 5000  # GNSS_HD 注入的时间+5s
            self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetNetAndSysTimeDeviation", {},
                                                {"out": time1})

            timeinfo = self.partner.send_request_and_return_resp(VEHICLETIME_SERVICE_CLIENT,    
                                                                "GetVehicleTimeInfo", {})['out']
            ck_data(timeinfo, {"UTCData": exp_UTCData, "TimeZone": 8, "SynchronizationStatus": 3, "politicalTimeZone": "Asia/Shanghai"})
            assert 0 < timeinfo['UTCTime'] - UTCTime < 1000

            self.partner.ck_no_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo", timeout=3)

@allure.feature("SOA服务接口")
@allure.story("架构基础/TimeManagementService")
@pytest.mark.zjb
class TestTimeManagementServiceTcamOffline(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("TCAM下电")
        self.nucapp.tcam_power_off()
        sleep(30)
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD"),
            ("VehicleTimeService", "client")
        ])
        self.partner.GNSSStatus = 1
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD)
        self.partner.wait_for_service_reconnect(VEHICLETIME_SERVICE_CLIENT)
        self.partner.unregister_event(VEHICLETIME_SERVICE_CLIENT)
        sleep(1)
        self.partner.register_event(VEHICLETIME_SERVICE_CLIENT)
        sleep(1)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.partner.UTCDate = 150823
        self.partner.UTCTime = 101525000
        self.partner.empty_all()

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        self.partner.stop_operators()
        self.nucapp.bgm_power_off()
        sleep(1)
        self.nucapp.bgm_power_on()
        self.nucapp.tcam_power_on()
        sleep(180)
        super().after_class(self, ecu)
    
    def pre_process(self, UTCDate=150823, UTCTime=101525000):
        # 前处理步骤，按预期授时并校准RTC时间
        if GNSS_SERVICE_SERVER_HD in self.partner.partner_infos:
            self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.restart_bgm_and_connect_service(VEHICLETIME_SERVICE_CLIENT)
        self.partner.start_single_partner("GNSSService", "server", "GNSSService_HD")
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD)
        self.partner.UTCDate = UTCDate
        self.partner.UTCTime = UTCTime
        self.partner.longitude = 121.4  # 上海的位置
        self.partner.latitude = 31.2
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation",
                                       {"gnssInfo": self.partner.gnss_info})
    
    @allure.title("启动后无RTC授时->GNSS(ACU)授时")
    @pytest.mark.sanity
    def test_caseid_1919334(self): # TCAM不在线，BGM上下电重启
        # 前置条件
        self.pre_process()

        # 用例步骤1
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.restart_bgm_and_connect_service(VEHICLETIME_SERVICE_CLIENT)

        timeinfo = self.partner.send_request_and_return_resp(VEHICLETIME_SERVICE_CLIENT,
                                                             "GetVehicleTimeInfo", {})['out']
        ck_data(timeinfo, {"UTCData": 10121, "TimeZone": 8, "SynchronizationStatus": 0, "politicalTimeZone": "Asia/Shanghai"})
        if timeinfo['UTCTime'] > 80000000: # 如果get接口在时区同步至之前获取到返回值，会拿到默认UTC时区，比上海时区多8h
            timeinfo['UTCTime'] -= 80000000
        # assert 6000 < timeinfo['UTCTime'] < 9000 # 从重启后到服务启动预计的时间范围
        assert 4000 < timeinfo['UTCTime'] < 8000 # s2s启动的时候独占从2s减少成1s,故校验范围平移1s;
        # 可能有event，也可能没有event，故不检测event

        # 用例步骤2
        self.partner.empty_all()
        self.partner.start_single_partner("GNSSService", "server", "GNSSService_HD")  # 此处启动是为了防止BGM来获取历史event进行了同步
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD)
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation",
                                       {"gnssInfo": self.partner.gnss_info})
        UTCTime = self.partner.ck_coming_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo", 
                                               {"info": {"UTCData": 150823, "TimeZone": 8, "SynchronizationStatus": 4,
                                                         "politicalTimeZone": "Asia/Shanghai"}})['info']['UTCTime']
        assert 101525000 < UTCTime < 101525299 # GNSS_HD发送NotifyGNSSInformation设置系统时间后，触发VehicleTimeInfo

        timeinfo = self.partner.send_request_and_return_resp(VEHICLETIME_SERVICE_CLIENT,
                                                             "GetVehicleTimeInfo", {})['out']
        ck_data(timeinfo, {"UTCData": 150823, "TimeZone": 8, "SynchronizationStatus": 4, "politicalTimeZone": "Asia/Shanghai"})
        assert 101525000 < timeinfo['UTCTime'] < 101525500
        
        # 用例步骤3
        self.partner.UTCDate = 150823
        self.partner.UTCTime = 101525000
        self.partner.empty_all(2)
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation",
                                       {"gnssInfo": self.partner.gnss_info})
        self.partner.ck_no_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo", timeout=2)  # 外部时钟源再次数据过来不会再次触发event
        timeinfo = self.partner.send_request_and_return_resp(VEHICLETIME_SERVICE_CLIENT,
                                                             "GetVehicleTimeInfo", {})['out']
        assert 101529000 < timeinfo['UTCTime'] < 101529999  # 随系统时间流逝，和计算偏差的新时钟数据无关
    
    @allure.title("启动后RTC授时->GNSS授时并触发通知网络时间和系统时间偏差")
    @pytest.mark.sanity
    @pytest.mark.failed
    def test_caseid_1984265(self): # TCAM不在线，BGM诊断重启
        # 用例步骤1
        self.pre_process(UTCTime=235920000)
        t1 = time.time()
        sleep(5)
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)  # 先停了服务，否则bgm启动后注册event，bootes会自动发送历史数据

        # 用例步骤2
        self.sd_tester.reset_ecu()
        self.partner.start_single_partner("GNSSService", "server", "GNSSService_HD")  # 只要重启了partner就会清历史数据
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD)
        self.partner.empty_all()
        self.partner.wait_for_service_reconnect(VEHICLETIME_SERVICE_CLIENT)
        UTCTime = self.partner.ck_coming_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo", 
                                            {"info": {"UTCData": 150823, "TimeZone": 8, "SynchronizationStatus": 2,
                                                      "politicalTimeZone": "Asia/Shanghai"}}, timeout=45)['info']['UTCTime'] # 设置系统时间
        t2 = time.time()
        assert t2 - t1 - 2 < (UTCTime - 235920000)/1000 < t2 - t1 + 2
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo", {},
                                              {"out": {"UTCData": 150823, "TimeZone": 8, "SynchronizationStatus": 2,
                                                      "politicalTimeZone": "Asia/Shanghai"}})
        
        self.partner.empty_all(1)  # 等待1s，因为设置系统时间，启动gptp也要耗时，设置系统时间后，下面再次触发才会计算偏差


        # 用例步骤3  # 拿到这次时间，去矫正RTC时间；如果启动后第一次授时就是GNSS，则会设置系统时间的同时去矫正RTC
        self.partner.UTCDate, self.partner.UTCTime = handle_utctime(150823, UTCTime, timedelta(seconds=15))
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation",
                                       {"gnssInfo": self.partner.gnss_info})
        self.partner.ck_no_event(VEHICLETIME_SERVICE_CLIENT, "NetAndSysTimeDeviation")
        
        # 用例步骤4  # 再次收到GNSS时间，去计算偏差
        self.partner.UTCDate, self.partner.UTCTime = handle_utctime(150823, UTCTime, timedelta(seconds=16))
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation",
                                       {"gnssInfo": self.partner.gnss_info})
        time1 = self.partner.ck_coming_event(VEHICLETIME_SERVICE_CLIENT, "NetAndSysTimeDeviation", {})["time"]
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetNetAndSysTimeDeviation", {},
                                              {"out": time1})
        assert 13700 < time1 < 14300  # 第3步偏差15s校正RTC时间，第4步才计算偏差，第4步发送的值与系统时间的流逝，差在16s - （empty_all的1s，ck_no_event的1s，即14s左右）
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo", 
                                  {"info": {"UTCData": 150823, "TimeZone": 8, "SynchronizationStatus": 4,
                                            "politicalTimeZone": "Asia/Shanghai"}})
        self.partner.empty_all()

        # 用例步骤5
        sleep(1)
        self.partner.UTCDate, self.partner.UTCTime = handle_utctime(150823, UTCTime, timedelta(minutes=1))
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation",
                                       {"gnssInfo": self.partner.gnss_info})
        self.partner.ck_no_event(VEHICLETIME_SERVICE_CLIENT, "NetAndSysTimeDeviation")
        self.partner.ck_no_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo")
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetNetAndSysTimeDeviation", {},
                                              {"out": time1})
        
        # 用例步骤6
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.sd_tester.reset_ecu()
        self.partner.empty_all()
        self.partner.wait_for_service_reconnect(VEHICLETIME_SERVICE_CLIENT)
        UTCTime2 = self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo", 
                                            {"info": {"UTCData": self.partner.UTCDate, "TimeZone": 8, "SynchronizationStatus": 2,
                                                      "politicalTimeZone": "Asia/Shanghai"}}, timeout=30)['info']['UTCTime']
        curr_time = time.time()
        exp_UTCDate, exp_UTCTime = handle_utctime(150823, 235920000, timedelta(seconds=int(curr_time - t1 + 15)))  # +15是因为上面GNSS授时给MCU的15s偏差
        assert  exp_UTCTime/1000 - 3 < UTCTime2/1000 < exp_UTCTime/1000 + 3
    
    @allure.title("时区信息记忆_接收到GNSS数据更新时区信息")
    @pytest.mark.sanity
    def test_caseid_1984267(self): # 时区记忆，时区变化后触发整车时间信息接口
        if GNSS_SERVICE_SERVER_HD not in self.partner.partner_infos:
            logger.info("当前GNSS服务未启动，重新启动")
            self.partner.start_single_partner("GNSSService", "server", "GNSSService_HD")
            self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD)
        self.partner.longitude = 60.0
        self.partner.latitude = 31
        self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation",
                                       {"gnssInfo": self.partner.gnss_info})
        sleep(1)
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo", {},
                                              {"out": {"TimeZone": 3}})
        self.partner.stop_single_partner(GNSS_SERVICE_SERVER_HD)
        self.sd_tester.reset_ecu()
        self.partner.empty_all()
        self.partner.wait_for_service_reconnect(VEHICLETIME_SERVICE_CLIENT)
        self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo", 
                                  {"info": {"TimeZone": 3}}, timeout=30)
        self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo", {},
                                              {"out": {"TimeZone": 3}})
        datas = [(126.6, 45.75, 9, "Asia/Harbin"), 
                 (120.4, 31.2, 8, "Asia/Shanghai"), 
                 (106.45, 29.56, 7, "Asia/Chongqing"), 
                 (87.68, 43.76, 6, "Asia/Urumqi"), 
                 (75.9, 39.5, 5, "Asia/Kashgar")] # zone为理论时区
        self.partner.start_single_partner("GNSSService", "server", "GNSSService_HD")
        self.partner.wait_for_service_reconnect(GNSS_SERVICE_SERVER_HD)
        for longitude, latitude, zone, politicalTimeZone in datas:
            self.partner.empty_all()
            self.partner.longitude = longitude
            self.partner.latitude = latitude
            self.partner.UTCTime += 100
            self.partner.send_event_notify(GNSS_SERVICE_SERVER_HD, "NotifyGNSSInformation",
                                        {"gnssInfo": self.partner.gnss_info})
            sleep(2)
            if zone == 9:
                self.partner.ck_s2s_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo", 
                                          {"info": {"TimeZone": 8, "politicalTimeZone": "Asia/Shanghai"}})
            else:
                self.partner.ck_no_event(VEHICLETIME_SERVICE_CLIENT, "VehicleTimeInfo")
            self.partner.send_request_and_ck_resp(VEHICLETIME_SERVICE_CLIENT, "GetVehicleTimeInfo", {},
                                              {"out": {"TimeZone": 8, "politicalTimeZone": "Asia/Shanghai"}})

