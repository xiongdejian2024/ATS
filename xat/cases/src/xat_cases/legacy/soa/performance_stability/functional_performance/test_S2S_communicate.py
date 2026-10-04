# -*- coding: utf-8 -*-
"""
@File        : test_service.py
@Author      : tao.cheng_ext@jiduatuo.com
@Time        : 2023/08/1 18:00 PM
@Description : Test SOA for S2S_Performance
"""

import allure
import pytest
import os
import subprocess
import sys
import time
import copy
import threading
import statistics
from time import sleep

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_cases.legacy.soa.case_helper.parse_excel import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from concurrent.futures import ThreadPoolExecutor
from xat_cases.legacy.soa.case_helper.utils import update_tosun,recover_tosun


partner = None
sd_test = None
end_time = None
global file_can
file_can = os.path.join(project_root, "test_case/soa/Can.asc")

@allure.feature("性能稳定性")
@allure.story("业务性能/S2S通信性能")
@pytest.mark.env
class Test_env(object):
    @pytest.mark.full
    @allure.title("上下行信号环境准备")
    def test_caseid_001(self):
        # 处理更新tosun文件
        update_tosun()


@allure.feature("性能稳定性")
@allure.story("业务性能/S2S通信性能")
@pytest.mark.soa
class Testperformance(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([
            ("HighVoltageService", "client"),("CentralLockService", "client"),
            ("VehicleSetStatusService", "client"),
            ("ChassisService", "client"), ("DoorService", "client"), ("WindowService", "client"),
            ("SteerWheelService", "client"),
            ("ClimateControlService", "client"), ("ShieldWindowService", "client"), ("ChargeLidService", "client"),
            ("OuterRearViewService", "client"),
            ("TailGateService", "client"), ("ConditionCheckService", "client"), ("WindowAppService", "client"),
            ("TailWingService", "client"),
            ("CarConfigService", "client"), ("VehicleModeService", "client"),
            ("WirelessPhoneChargingService", "client"), ("WiperService", "client"),
            ("SeatService", "client")])
        self.run_flag = False
        self.partner.method_default_timeout = 30 #高负载不考虑接口调用超时

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.sd_tester.tester_present()
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.backbonefr_vddmbackbonefr03_gearlvrindcn_gearlvrindcn2_parkindcn()
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 0)
        sleep(1)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.sd_tester.stop_tester_present()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        os.system("""ps -ef|grep -i tail|awk '{printf $2"\n"}'|xargs kill -9;ps -ef|grep -i tail""")
        # 恢复tosun文件
        recover_tosun()
        super().after_class(self, ecu)

    def gaoya_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetBatteryHeating",
                                             {"type": 5, "on": False, "value": 0})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetEnergyRecoveryLevel", {"level": 2})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetEnergyRecoveryCmd", {"isOn": False})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetAveragePowerConsume", {"power": 90.0})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetBatteryHeating",
                                             {"type": 5, "on": True, "value": -40})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetEnergyRecoveryLevel", {"level": 1})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetEnergyRecoveryCmd", {"isOn": True})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetAveragePowerConsume", {"power": 50.0})
            sleep(0.15)

    def vehicleset_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": False})
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False})
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": True})
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True})
            sleep(0.15)

    def chassis_request(self):
        """发送request请求"""

        while self.run_flag:
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": False})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetTorqueMode", {"mode": 2})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetTorqueMode", {"mode": 1})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 2})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "EPBOperation", {"operate": 0})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAutoHold", {"on": False})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": True})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetTorqueMode", {"mode": 0})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetTorqueMode", {"mode": 2})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 3})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "EPBOperation", {"operate": 1})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAutoHold", {"on": True})
            sleep(0.15)

    def Door_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition',
                                             {"doors": [{"id": 0, "pos": 0}, {"id": 1, "pos": 10},
                                                        {"id": 2, "pos": 0}, {"id": 3, "pos": 10}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPositionMax', {"doors": [{"id": 0, "pos": 10},
                                                                                               {"id": 1, "pos": 10},
                                                                                               {"id": 2, "pos": 10},
                                                                                               {"id": 3, "pos": 10}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition',
                                             {"doors": [{"id": 0, "pos": 50}, {"id": 1, "pos": 50},
                                                        {"id": 2, "pos": 50}, {"id": 3, "pos": 50}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPositionMax', {"doors": [{"id": 0, "pos": 100},
                                                                                               {"id": 1, "pos": 100},
                                                                                               {"id": 2, "pos": 100},
                                                                                               {"id": 3, "pos": 100}]})
            sleep(0.15)

    def climate_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature',
                                             {"zoneId": 3, "value": 25.5})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetFragranceType',
                                             {'fragrance': [{'channel': 1, 'ratio': 30}]})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature',
                                             {"zoneId": 3, "value": 22.5})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetFragranceType',
                                             {'fragrance': [{'channel': 1, 'ratio': 100}]})
            sleep(0.15)

    def shieldwindow_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat", {"heat": {"id": 2, "status": 0}})
            self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat",
                                             {"heat": {"id": 1, "status": 0}})
            self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat",
                                             {"heat": {"id": 1, "status": 1}})
            self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat", {"heat": {"id": 2, "status": 1}})
            sleep(0.15)

    def window_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Close", {"windows": [0, 1, 2, 3]})
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition",
                                             {"windows": [{"id": 0, "position": 20},
                                                          {"id": 1, "position": 20},
                                                          {"id": 2, "position": 20},
                                                          {"id": 3, "position": 20}]})
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Open", {"windows": [0, 1, 2, 3]})
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition",
                                             {"windows": [{"id": 0, "position": 50},
                                                          {"id": 1, "position": 50},
                                                          {"id": 2, "position": 50},
                                                          {"id": 3, "position": 50}]})
            sleep(0.15)

    def outerview_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {
                "params": [{"viewId": 1, "horizontalAngle": 50, "verticalAngle": 100}]})
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, 'SetAutoFoldUnfold',
                                             {"params": [{"id": 2, "isOn": False}]})
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {
                "params": [{"viewId": 1, "horizontalAngle": 100, "verticalAngle": 100}]})
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, 'SetAutoFoldUnfold',
                                             {"params": [{"id": 2, "isOn": True}]})
            sleep(0.15)

    def tailgate_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(TAILGATE_SERVICE_CLIENT, "SetTailGate", {"cmd": 1})
            self.partner.send_method_request(TAILGATE_SERVICE_CLIENT, "SetTailGate", {"cmd": 0})
            self.partner.send_method_request(TAILGATE_SERVICE_CLIENT, "Open", {})
            self.partner.send_method_request(TAILGATE_SERVICE_CLIENT, "Close", {})
            sleep(0.15)

    def get_timestamp(self):
        # 获取can报文开始的时间戳
        data = os.popen(f"cat {file_can}|grep --line-buffered 'date'").read()
        date_str = data.replace('date ', '').replace('\n', '')
        timestamp = time.mktime(time.strptime(date_str, "%a %b %d %H:%M:%S %Y"))
        return timestamp
    
    def get_newfile_timestamp(self):
        try:
            file = os.path.join(os.getcwd(), "tosun_asc_product_time")
            with open(file, "r") as f:
                timestamp = f.readlines()
                return timestamp[0]
        except Exception as e:
            logger.info(f"获取时间戳异常,有误差{e}")
            return self.get_timestamp()

    def tosun_check(self, can_bus, can_id, from_str, to_str, iter_total=400):
        # 校验报文
        cmd = f'tail -F {file_can}|grep --line-buffered " {can_bus} "|grep --line-buffered " {can_id}  "'
        logger.info(f"cmd==>>>{cmd}")
        iter_num = 0
        last_line = ""
        global end_time
        from_str_new = from_str.split(' ')[-1][-1]
        to_str_new = to_str.split(' ')[-1][-1]
        logger.info(f"from开始信号位为:{from_str_new}, to结束信号位为:{to_str_new}")
        t0 = time.time()
        try:
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, text=True) as pro:
                while iter_num < iter_total:
                    line = pro.stdout.readline().strip().split(" ")
                    logger.info(f"line==>>{line}")

                    if iter_num == 0:
                        last_line = line
                        logger.info(f"last_line:{last_line}")
                        
                    curr_line = line
                    logger.info(f"第{iter_num+1}次执行from开始信号位为:{last_line}")
                    if curr_line[-4][-1] == to_str_new and last_line[-4][-1] == from_str_new:
                        end_time = float(curr_line[0])
                        logger.info(f"{end_time}")
                        logger.info("执行成功，程序退出")
                        break
                    else:
                        last_line = curr_line
                    if time.time()-t0 > 5:
                        logger.info("超时5s，执行失败，程序退出")
                        break
                
                    iter_num = iter_num + 1
                else:
                    logger.info("执行失败，程序退出")
        except Exception as e:
            logger.error(f"执行过程中发生错误: {e}")


    def candump_check(self, can_bus, can_id, from_str, to_str, iter_total=4000):
        """
        通过candump命令来获取帧报文发生跳变时刻的时间戳，捕获到的时间戳保存在全局变量 end_time 中，捕获失败 end_time 为None
        can_bus: 例如can4
        can_id：帧报文ID
        from_str：跳变前字符串
        to_str：跳变后字符串
        iter_total：捕获次数，默认400次
        """
        cmd = f'candump -ta {can_bus},{can_id}:7FF'
        logger.info(cmd)

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')

        iter_num = 0
        last_line = ""
        global end_time
        start_time = time.time()
        end_time = None

        while p.poll() is None:
            if iter_num > iter_total:
                p.terminate()
                p.wait()
                # os.killpg(p.pid, signal.SIGTERM)
                logger.info("执行失败，程序退出")
                break
            line = p.stdout.readline()
            line = line.strip()
            if line:
                # print('Subprogram output[{}]: [{}]'.format(iter_num, line))
                if iter_num == 0:
                    logger.info(f"last_line:{last_line}")
                    last_line = line
                curr_line = line
                # logger.info(f"curr_line:{curr_line}")
                # logger.info(f"{line}")
                if to_str not in last_line and to_str in curr_line:
                    end_time = float(curr_line.split(" ")[0][1:-2])
                    logger.info(f"{end_time}")
                    if end_time > start_time:
                        p.terminate()
                        p.wait()
                        logger.info("执行成功，程序退出")
                else:
                    last_line = curr_line
            iter_num = iter_num + 1
    
    # @pytest.mark.full
    # def test_caseid_000(self):
    #     sleep(2)

    @allure.title("架构基础_高负载_上行")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1703490?projectId=46')
    @pytest.mark.pressure
    def test_caseid_111714(self):
        with allure.step("HIghvoltageService上行"):
            self.ipdu.pause_all_bus_send()
            # self.busapp.bus_dict["backbonefr"].stop_flexray()
            self.ipdu.send_pdu("propulsioncan", 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
            sleep(2)
            list_result = []

            def average(list1):
                return sum(list1) / len(list1)

            for T in range(10000):
                logger.info(f"第{T + 1}次压测")
                self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvSysRlyStsHvSysRlySts', 0)  # 20ms
                self.partner.empty_all(2)
                self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvSysRlyStsHvSysRlySts', 2)
                time1 = time.time()
                try:
                    self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "hvActiveSts", {"sts": 2}, timeout=1)  # event
                except Exception:
                    break
                time2 = time.time()
                timer = time2 - time1
                logger.info(f"时间差={timer}")
                list_result.append(timer)
                sleep(2)
            logger.info(f"before:{list_result}")
            logger.info(f"压测累计次数: {len(list_result)}")
            D = average(list_result)
            logger.info(f"before平均值为:{D}")

            list_result.sort()
            logger.info(f"after:{list_result[:-1]}")
            D1 = round(average(list_result[:-1])*1000, 3)
            D2 = round(min(list_result[:-1])*1000, 3)
            D3 = round(max(list_result[:-1])*1000, 3)
            logger.info(f"After_sort_removeMAX_平均值为:{D1}ms")
            logger.info(f"After_sort_removeMAX_最大值为:{D3}ms")
            logger.info(f"After_sort_removeMAX_最小值为:{D2}ms")
            self.ipdu.resume_all_bus_send()
            with allure.step(f"After_sort_removeMAX测试结果:"):
                pass
            with allure.step(f"平均值为:{D1}ms"):
                pass
            with allure.step(f"最大值为:{D3}ms"):
                pass
            with allure.step(f"最小值为:{D2}ms"):
                pass

    @allure.title("架构基础_低负载_上行")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1703490?projectId=46')
    @pytest.mark.full
    def test_caseid_111715(self):
        with allure.step("HIghvoltageService上行"):
            self.ipdu.send_pdu("propulsioncan", 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
            sleep(2)
            self.ipdu.set_random_signal_thread_start("bodycan", 10000, 0.01)
            list_result = []

            def average(list1):
                return sum(list1) / len(list1)

            for T in range(100):
                logger.info(f"第{T + 1}次压测")
                self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvSysRlyStsHvSysRlySts', 0)  # 20ms
                self.partner.empty_all(2)
                self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvSysRlyStsHvSysRlySts', 2)
                time1 = time.time()
                sleep(1)
                try:
                    self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "hvActiveSts", {"sts": 2}, timeout=3)  # event
                    time2 = time.time()
                    timer = time2 - time1 - 1
                    logger.info(f"时间差={timer}")
                    list_result.append(timer)
                    sleep(2)
                except Exception:
                    break
                    logger.info(f"this_time_Not_Notify")
            logger.info(f"before:{list_result}")
            logger.info(f"压测累计次数: {len(list_result)}")
            D = average(list_result)
            logger.info(f"before平均值为:{D}")
            list_result.sort()
            logger.info(f"after:{list_result[:-1]}")
            D1 = round(average(list_result[:-1])*1000, 3)
            D2 = round(min(list_result[:-1])*1000, 3)
            D3 = round(max(list_result[:-1])*1000, 3)
            logger.info(f"After_sort_removeMAX_平均值为:{D1}ms")
            logger.info(f"After_sort_removeMAX_最大值为:{D3}ms")
            logger.info(f"After_sort_removeMAX_最小值为:{D2}ms")
            self.ipdu.set_random_signal_thread_all_stop()

    # 框架性能问题，暂未修复，改为repeat重试
    @allure.title("校验服务上下线场景的上行数据event事件")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1703490?projectId=46')
    @pytest.mark.full
    @pytest.mark.repeat(100)
    def test_caseid_1985316(self):
        with allure.step("服务上下线场景HIghvoltageService上行"):
            self.ipdu.set_random_signal_thread_start("bodycan", 100, 0.05)
            self.ipdu.send_pdu("propulsioncan", 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
            self.bgm_power_off_and_on(timeout=0)
            self.partner.wait_for_service_reconnect(HIGHVOLTAGE_SERVICE_CLIENT)
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvSysRlyStsHvSysRlySts', 0)  # 20ms
            self.partner.empty_all(0.05)
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvSysRlyStsHvSysRlySts', 2)
            self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "hvActiveSts", {"sts": 2}, timeout=4)  # event

            self.ipdu.set_random_signal_thread_all_stop()

    @allure.title("整车控制_高负载_下行")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1703490?projectId=46')
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @pytest.mark.pressure
    def test_caseid_111716(self):
        with allure.step("SeatService下行"):
            list_result = []
            self.run_flag = True
            t0 = self.get_newfile_timestamp()
            def average(list1):
                if not isinstance(list1, list) or len(list1) == 0:
                    return 0
                return sum(list1) / len(list1)

            with ThreadPoolExecutor(max_workers=8) as pool:
            # 提交任务到线程池
                futures = [
                    pool.submit(self.gaoya_request),
                    pool.submit(self.vehicleset_request),
                    pool.submit(self.chassis_request),
                    pool.submit(self.climate_request),
                    pool.submit(self.shieldwindow_request),
                    pool.submit(self.window_request),
                    pool.submit(self.outerview_request),
                    pool.submit(self.tailgate_request)
                ]

                def get_result(future):
                    try:
                        result = future.result()  # 尝试获取结果
                        logger.info(f"函数{future}运行的结果为{result}")
                    except Exception as e:
                        # 记录异常信息，防止程序崩溃
                        logger.info(f"Task generated an exception: {e}")

                # 为所有future添加回调函数
                for future in futures:
                    future.add_done_callback(get_result)
                    logger.info('-------主线程-------')

                for T in range(8000):
                    logger.info(f"第{T + 1}次压测")
                    th1 = threading.Thread(target=self.tosun_check,
                                           args=("1", "357", "8 00 00 00 00 03", "8 00 00 00 00 02", 100))
                    self.stop_event = threading.Event()
                    th1.setDaemon(True)
                    th1.start()

                    self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingLevel",
                                                     {"params": [{"id": 0, "uint8Info": 3}]})
                    self.partner.empty_all(2)
                    time1 = time.time()
                    self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingLevel",
                                                     {"params": [{"id": 0, "uint8Info": 2}]})
                    
                    while time.time() - time1 < 5 and self.run_flag == True:
                        if end_time:
                            timer = end_time + float(t0) - time1  # 时间相减
                            if timer > 0.0:
                                logger.info(f"时间差={timer}")
                                self.stop_event.set()
                                try:
                                    th1.join()
                                except KeyboardInterrupt:
                                    if th1.is_alive():
                                        os.kill(th1.ident, th1.SIGTERM)
                                list_result.append(timer)
                                break
                    else:
                        logger.info(f"第{T + 1}次this_time_NotFind")
                        assert False
                self.run_flag = False
                self.partner.empty_all(2)
                logger.info(f"压测累计次数: {len(list_result)}")
                D = average(list_result)
                logger.info(f"before平均值为:{D}")
                logger.info(f"before:{list_result}")
                list_result.sort()
                logger.info(f"after:{list_result[:-1]}")
                D1 = round(average(list_result[:-1])*1000, 3)
                D2 = round(min(list_result[:-1])*1000, 3)
                D3 = round(max(list_result[:-1])*1000, 3)
                logger.info(f"After_sort_removeMAX_平均值为:{D1}ms")
                logger.info(f"After_sort_removeMAX_最大值为:{D3}ms")
                logger.info(f"After_sort_removeMAX_最小值为:{D2}ms")

                with allure.step(f"After_sort_removeMAX测试结果:"):
                    pass
                with allure.step(f"平均值为:{D1}ms"):
                    pass
                with allure.step(f"最大值为:{D3}ms"):
                    pass
                with allure.step(f"最小值为:{D2}ms"):
                    pass
                    
    @allure.title("整车控制_低负载_下行")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1703490?projectId=46')
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @pytest.mark.full
    def test_caseid_111717(self):
        with allure.step("SeatService下行"):
            self.ipdu.pause_all_bus_send()
            sleep(1)
            list_result = []
            t0 = self.get_newfile_timestamp()
            def average(list1):
                if not isinstance(list1, list) or len(list1) == 0:
                    return 0
                return sum(list1) / len(list1)

            for T in range(100):
                logger.info(f"第{T + 1}次压测")
                th1 = threading.Thread(target=self.tosun_check,
                                       args=("1", "357", "8 00 00 00 00 03", "8 00 00 00 00 02", 100))
                self.stop_event = threading.Event()
                th1.setDaemon(True)
                th1.start()
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingLevel",
                                                 {"params": [{"id": 0, "uint8Info": 3}]})
                self.partner.empty_all(2)
                time1 = time.time()
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingLevel",
                                                 {"params": [{"id": 0, "uint8Info": 2}]})
                
                while time.time() - time1 < 5:
                        if end_time:
                            timer = end_time + float(t0) - time1  # 时间相减
                            if timer > 0.0:
                                logger.info(f"时间差={timer}")
                                self.stop_event.set()
                                th1.join(1)
                                list_result.append(timer)
                                break
                else:
                    logger.info(f"第{T + 1}次this_time_NotFind")

            logger.info(f"压测累计次数: {len(list_result)}")
            D = average(list_result)
            logger.info(f"before平均值为:{D}")
            logger.info(f"before:{list_result}")
            list_result.sort()
            logger.info(f"after:{list_result[:-1]}")
            D1 = round(average(list_result[:-1])*1000, 3)
            D2 = round(min(list_result[:-1])*1000, 3)
            D3 = round(max(list_result[:-1])*1000, 3)
            logger.info(f"After_sort_removeMAX_平均值为:{D1}ms")
            logger.info(f"After_sort_removeMAX_最大值为:{D3}ms")
            logger.info(f"After_sort_removeMAX_最小值为:{D2}ms")
            self.ipdu.resume_all_bus_send()


remote_control_critical_services = ["TailGateService", "HighVoltageService", "ChargeLidService",
                                    "KeyService", "LightService", "SeatService",
                                    "ClimateControlService", "WindowAppService", "ShieldWindowService",
                                    "CentralLockService", "DoorService"]
S2S_critical_services = ["WTIService", "VehicleModeService", "CarConfigService",
                         "WindowService", "ChassisService", "EntryService",
                         "WiperService", "OuterRearViewService", "LowVoltageService",
                         "SteerWheelService", "PedalService", "TyreService", "VehicleTimeService"]


# @allure.feature("专项测试")
# @allure.story("S2S性能测试")
# class TestS2SPerformance(TestBase):

#     def before_class(self, ecu):
#         """测试用例的前处理"""
#         super().before_class(self, ecu)
#         logger.info("查看BGM是否是S2D启动")
#         num = self.bgmcli.type_commands("cat /sys/power/sys_resumed")
#         if num.strip() == "1":
#             logger.info("bgm是S2D启动")
#             self.bgmcli.type_commands("rm -rf /log/jetlog*")
#         else:
#             exit("bgm不是S2D启动, 请线下修正后再运行")
#         partner_process_check()
#         self.clients = [tuple([partner_member, 'client']) for partner_member in
#                         remote_control_critical_services + S2S_critical_services] + [tuple([partner_member, 'client_1'])
#                                                                                      for partner_member in
#                                                                                      remote_control_critical_services + S2S_critical_services]
#         self.partner = S2sBaseClass(self.clients +
#                                     [("LCAService", "server"),
#                                      ("ACUInfoService", "server"),
#                                      ("ANPWTIService", "server"),
#                                      ("RPAAPAService", "server"),
#                                      ("AVPService", "server"),
#                                      ("SLAMMapService", "server"),
#                                      ("BACUService", "server"),
#                                      ("FCTAService", "server"),
#                                      ("RCWService", "server"),
#                                      ("AEBRService", "server"),
#                                      ("ACCService", "server"),
#                                      ("RCTAService", "server"),
#                                      ("DOWService", "server"),
#                                      ("SensorCalibrationService", "server"),
#                                      ("LKAService", "server"),
#                                      ("TLAService", "server"),
#                                      ("SensorSelfCleanService", "server"),
#                                      ("ACUFaultInfoService", "server"),
#                                      ("FrontBackupCamera", "server"),
#                                      ("CMSFService", "server"),
#                                      ("SASService", "server"),
#                                      ("ADASMainService", "server"),
#                                      ("AutoHighBeamControlService", "server"),
#                                      ("AEBService", "server"),
#                                      ("FCWService", "server"),
#                                      ("AutoGearShiftService", "server"),
#                                      ("APIService", "server"),
#                                      ("ANPMRCService", "server"),
#                                      ("WTIAutoDriveService", "client"),
#                                      ("BonnetService", "client"),
#                                      ("PassiveSafetyService", "client"),
#                                      ("DrivingAssistService", "client"),
#                                      ("GloveBoxService", "client"),
#                                      ("HornService", "client"),
#                                      ("InnerRearViewService", "client"),
#                                      ("TailWingService", "client"),
#                                      ], logger_flag=True)
#         self.ipdu.start_all_time_control()
#         self.busapp.start_all_cyclic_msg()

#     def after_class(self, ecu):
#         """测试用例全部完成后的后处理"""
#         self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
#         self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
#         self.partner.stop_operators()
#         super().after_class(self, ecu)

#     def before_each_func(self, ecu):
#         """每个测试用例前置步骤"""
#         super().before_each_func(ecu, start=False)
#         self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#         self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#         self.ipdu.backbonefr_vddmbackbonefr03_gearlvrindcn_gearlvrindcn2_parkindcn()
#         self.partner.empty_all(1)

#     def after_each_func(self, ecu):
#         super().after_each_func(ecu, start=False)
    
    
#     def s_timestamp(self):
#         """
#         获取时间戳
#         :return: str
#         """
#         return time.strftime("%Y%m%d%H%M%S", time.localtime())


#     @allure.title("BGM关键服务可用时间")
#     @pytest.mark.full
#     @pytest.mark.restart
#     def test_caseid_188741(self):
#         bgmssh = BGM_SSH(hostname="169.254.19.1")
#         bgmssh.type_commands("ls -l /log")
#         test_times = 50
#         case_services = ["_".join(list(partner_member)) for partner_member in self.clients]
#         online_times = {key: [] for key in case_services}
#         start_times = {key: [] for key in case_services}
#         connect_times = {key: [] for key in case_services}
#         max_online_time = {key: (0, 0) for key in case_services}
#         max_connect_time = {key: (0, 0) for key in case_services}
#         max_start_time = {key: (0, 0) for key in case_services}
#         sleep(5)

#         def print_infos(test_num):
#             for partner_key in case_services:
#                 online_mean_time = round(statistics.mean(online_times[partner_key]), 3)
#                 start_mean_time = round(statistics.mean(start_times[partner_key]), 3)
#                 connect_time = round(statistics.mean(connect_times[partner_key]), 3)
#                 logger.info(
#                     f"{test_num}次压测服务可用时间平均值：{start_mean_time}({online_mean_time}), 连接耗时均值：{connect_time} --- {partner_key}")

#         for number in range(1, test_times + 1):
#             self.ipdu.pause_all_bus_send()
#             self.nucapp.bgm_power_off()
#             sleep(7)
#             self.partner.empty_all()
#             tmp_partners = copy.deepcopy(case_services)
#             self.nucapp.bgm_power_on()
#             self.ipdu.resume_all_bus_send()
#             st = time.time()
#             logger.info(f"BGM上电:{st}")

#             while time.time() - st < 20 and tmp_partners:
#                 for partner_name in tmp_partners:
#                     if self.partner.partner_infos[partner_name].event_list:
#                         event = self.partner.partner_infos[partner_name].event_list.pop()
#                         if event['function'] == 'ServiceStatus':
#                             raw_data = eval(event['args'])
#                             timestamp = round(event['timestamp'] - st, 3)
#                             if raw_data['state'] == 'ONLINE':  # S2S服务上线
#                                 online_times[partner_name].append(timestamp)
#                                 if timestamp > max_online_time[partner_name][1]:
#                                     max_online_time[partner_name] = (number, timestamp)
#                             elif raw_data['state'] == 'START':  # bootes服务连接完成
#                                 start_times[partner_name].append(timestamp)
#                                 if timestamp > max_start_time[partner_name][1]:
#                                     max_start_time[partner_name] = (number, timestamp)
#                         if len(online_times[partner_name]) == len(start_times[partner_name]) == number:
#                             connect_time = round(
#                                 start_times[partner_name][number - 1] - online_times[partner_name][number - 1], 3)
#                             connect_times[partner_name].append(connect_time)
#                             if connect_time > max_connect_time[partner_name][1]:
#                                 max_connect_time[partner_name] = (number, connect_time)
#                             tmp_partners.remove(partner_name)
#                             break
#             else:
#                 logger.info(f"第{number}次出现{tmp_partners}未连接")
#                 if tmp_partners:
#                     assert False, "有服务未成功连接"
#             # 增加STD启动成功的判断 cat /sys/power/sys_resumed=1
#             if number != test_times:
#                 print_infos(number)
#             # 备份BGM日志到/data/目录
#             if number == test_times//2:
#                 self.bgmcli.type_commands(f"tar -cvzf /data/log_{self.s_timestamp()}_前{number}次日志.tar.gz /log/jetlog*")
#                 time.sleep(10)
#                 # self.bgmcli.type_commands("rm -rf /log/jetlog*")
#             elif number == test_times:
#                 self.bgmcli.type_commands(f"tar -cvzf /data/log_{self.s_timestamp()}_后{test_times - (test_times//2)}次日志.tar.gz /log/jetlog*")
#         sleep(2)

#         for partner_key in self.partner.partner_infos:
#             self.partner.partner_infos[partner_key].running = False
#         sleep(2)
#         print_infos(test_times)
#         for partner_key in max_online_time:
#             online = max_online_time[partner_key]
#             start = max_start_time[partner_key]
#             connect = max_connect_time[partner_key]
#             logger.info(
#                 f"最大上线为第{online[0]}次耗时{online[1]}, 最大可用为第{start[0]}次耗时{start[1]}，最大连接为第{connect[0]}次耗时{connect[1]}---{partner_key}")
#         logger.info(online_times)
#         logger.info(start_times)
#         logger.info(connect_times)




# @allure.feature("专项测试")
# @allure.story("S2S性能测试")
# class TestS2SPerformance2(TestBase):

#     def before_class(self, ecu):
#         """测试用例的前处理"""
#         super().before_class(self, ecu)
#         partner_process_check()
#         self.partner = S2sBaseClass(
#             [KEY_SERVICE_CLIENT, LIGHT_SERVICE_CLIENT, SEAT_SERVICE_CLIENT, HIGHVOLTAGE_SERVICE_CLIENT,
#              INNERREARVIEW_SERVICE_CLIENT, OUTERREARVIEW_SERVICE_CLIENT, TAILWING_SERVICE_CLIENT, TYRE_SERVICE_CLIENT,
#              WIPER_SERVICE_CLIENT, STEERWHEEL_SERVICE_CLIENT, CHASSIS_SERVICE_CLIENT, DOOR_SERVICE_CLIENT,CLIMATECONTROL_SERVICE_CLIENT])
#         self.ipdu.start_all_time_control()
#         self.busapp.start_all_cyclic_msg()

#     def after_class(self, ecu):
#         """测试用例全部完成后的后处理"""
#         self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
#         self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
#         self.partner.stop_operators()
#         super().after_class(self, ecu)

#     def before_each_func(self, ecu):
#         """每个测试用例前置步骤"""
#         super().before_each_func(ecu, start=False)
#         self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#         self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#         self.ipdu.backbonefr_vddmbackbonefr03_gearlvrindcn_gearlvrindcn2_parkindcn()
#         self.partner.empty_all(1)

#     def after_each_func(self, ecu):
#         super().after_each_func(ecu, start=False)

#     @allure.title("BGM首次下线默认配置")
#     @allure.title("1943420 获取后视镜自动折叠设置状态_首次下线默认值; 1943418 获取后视镜下翻状态_首次下线默认值; 1943417 获取外后视镜角度_首次下线默认值")
#     @allure.title("1943416 获取后视镜加热状态_首次下线默认值; 1943415 获取外后视镜折叠状态_首次下线默认值; 1943413  获取内后视镜自动防眩目功能开启关闭状态_首次下线默认值")
#     @allure.title("1943410 获取ESC运动模式状态_首次下线默认值; 1943409 获取陡坡缓降开关状态_首次下线默认值; 1943407  GetConfigInfo获取配置信息_首次下线默认值")
#     @allure.title("1959958 获取电动门开启模式, 默认1 auto")
#     @pytest.mark.full
#     @pytest.mark.restart
#     def test_caseid_1943420_1943418_1943417_1943416_1943415_1943413_1943410_1943409_1943407_1959958_1979951(self):
#         # 删除数据库
#         bgmssh = BGM_SSH()
#         bgmssh.type_commands("sudo rm -rf /data/s2s_service/s2s_service.db3", root_permission=True)
#         sleep(1)
#         bgmssh.type_commands("ls -l /data/s2s_service")
#         sleep(5)
#         self.ipdu.pause_all_bus_send()  # 停掉总线
#         self.nucapp.bgm_power_off()
#         sleep(7)
#         self.partner.empty_all()
#         self.nucapp.bgm_power_on()
#         self.partner.wait_for_service_reconnect(LIGHT_SERVICE_CLIENT)
#         # 获取远光灯开关按键状态
#         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 0})
#         # 获取内灯模式（礼貌灯）,默认2 Auto
#         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 2})
#         # 获取外灯模式，默认1 Auto
#         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 1})
#         # 获取外灯FollowMeHome时长, 默认0
#         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFollowMeHomeTime", {}, {"out": 0})
#         # 获取智能氛围灯功能禁用状态, 获取普通氛围灯功能禁用状态
#         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetLightInhibitSts", {"type": [25, 35]},
#                                               {"out": [{"type": 25, "inhibitSts": False},
#                                                        {"type": 35, "inhibitSts": False}]})
#         # 获取座椅自动加热开关状态 GetAutoHeating, 启动后默认发0=False
#         self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetAutoHeating", {"seats": [12]},
#                                               {"out": [{"id": 0, "isOn": False}, {"id": 1, "isOn": False},
#                                                        {"id": 4, "isOn": False}, {"id": 6, "isOn": False}]})
#         # 获取座椅自动通风开关状态 GetAutoVenting, 启动后默认发0=False
#         self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetAutoVenting", {"seats": [12]},
#                                               {"out": [{"id": 0, "isOn": False}, {"id": 1, "isOn": False},
#                                                        {"id": 4, "isOn": False}, {"id": 6, "isOn": False}]})
#         # 获取座椅按摩设置状态 GetMassageConf，启动后默认发0
#         self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetMassageConf", {"seats": [12]},
#                                               {"out": [{"id": 0, "conf": {"isOn": False, "type": 0, "intensity": 0}},
#                                                        {"id": 1, "conf": {"isOn": False, "type": 0, "intensity": 0}}]})
#         # 获取座椅通风加热状态 GetSeatHeatVentStatus, 默认ventTime值为59
#         self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
#                                               {"out": [{"id": 0, "status": {"ventTime": 59, "heatTime": 59}},
#                                                        {"id": 1, "status": {"ventTime": 59, "heatTime": 59}},
#                                                        {"id": 4, "status": {"ventTime": 59, "heatTime": 59}},
#                                                        {"id": 6, "status": {"ventTime": 59, "heatTime": 59}}]})
#         # 获取座椅系统状态 GetSeatSysStatus，默认值
#         self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatSysStatus", {"seats": [12]},
#                                               {"out": [{"id": 0, "status": {"massageType": 0, "massageIntensity": 0}},
#                                                        {"id": 1, "status": {"massageType": 0, "massageIntensity": 0}}]})
#         # 获取能耗信息  todo: 是首次下线还是每次上电
#         self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetPowerConsumptionInfo", {},
#                                               {'out': {'outputEnergy': 0.0, 'recoveryEnergy': 0.0}})
#         # 获取估算的平均电耗
#         self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetAveragePowerConsume", {},
#                                               {"out": 256})
#         # 获取表显续航里程，type无记忆值的默认值为0
#         self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetRange", {},
#                                               {"out": {"type": 0, "CLTCRange": 0XFFFF, "estimatedRange": 0XFFFF}})
#         # 获取内后视镜自动防眩目功能开启关闭状态，默认ison
#         self.partner.send_request_and_ck_resp(INNERREARVIEW_SERVICE_CLIENT, "GetAutoBlidingProof", {}, {"out": True})
#         # 获取外后视镜折叠状态
#         self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, "GetViewFoldStatus", {"views": [2]},
#                                               {"out": [{"id": 0, "foldStatus": 0, "clientId": 255},
#                                                        {"id": 1, "foldStatus": 0, "clientId": 255}]})
#         # 获取后视镜加热状态
#         self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetHeat', {"views": [2]},
#                                               {"out": [{"id": 2, "isOn": False}]})
#         # 获取外后视镜角度
#         self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views": [2]},
#                                               {"out": [{"viewId": 0, "horizontalAngle": 0, "verticalAngle": 0},
#                                                        {"viewId": 1, "horizontalAngle": 0, "verticalAngle": 0}]})
#         # 获取后视镜下翻状态
#         self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewTiltStatus', {"views": [2]},
#                                               {"out": [{"id": 0, "tiltStatus": 0},
#                                                        {"id": 1, "tiltStatus": 0}]})
#         # 获取后视镜自动折叠设置状态
#         self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetAutoFoldUnfold', {"views": [2]},
#                                               {"out": [{"id": 0, "isOn": True},
#                                                        {"id": 1, "isOn": True}]})
#         # 获取尾翼禁用状态, 默认false
#         self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailwingInhibit', {}, {"out": False})
#         # 获取尾翼模式, 默认Off
#         self.partner.send_request_and_ck_resp(TAILWING_SERVICE_CLIENT, 'GetTailwingMode', {}, {"out": 0})
#         # 获取胎压信息
#         self.partner.send_request_and_ck_resp(TYRE_SERVICE_CLIENT, "GetPressure", {"tyres": [4]},
#                                               {"out": [{"id": 0, "pressure": 350.115},
#                                                        {"id": 1, "pressure": 350.115},
#                                                        {"id": 2, "pressure": 350.115},
#                                                        {"id": 3, "pressure": 350.115}
#                                                        ]})
#         # 获取胎温信息
#         self.partner.send_request_and_ck_resp(TYRE_SERVICE_CLIENT, "GetTemperature", {"tyres": [4]},
#                                               {"out": [{"id": 0, "temperature": 205},
#                                                        {"id": 1, "temperature": 205},
#                                                        {"id": 2, "temperature": 205},
#                                                        {"id": 3, "temperature": 205},
#                                                        ]})
#         # 获取轮胎相关信息
#         self.partner.send_request_and_ck_resp(TYRE_SERVICE_CLIENT, "GetTyreInfo", {"tyres": [4]},
#                                               {"out": [{"id": i,
#                                                         "pressure": 350.115,
#                                                         "temperature": 205,
#                                                         "fault": [0]} for i in range(4)
#                                                        ]
#                                                })
#         # 获取雨刮禁用状态
#         self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
#                                               {"out": {"id": 0, "MoveInhibit": False, "WashInhibit": False}},
#                                               timeout=3)
#         # 获取雨刮模式, 默认auto，6
#         self.partner.send_method_request(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
#                                          {"out": {"id": 0, "mode": 6}})

#         # 获取方向盘自动加热开关状态, 默认false
#         self.partner.send_request_and_ck_resp(STEERWHEEL_SERVICE_CLIENT, "GetAutoHeat", {}, {"out": False})

#         # GetConfigInfo_未配置时默认值
#         self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetConfigInfo", {},
#                                               {"out": [{"key": 0, "value": 0}, {"key": 1, "value": 0},
#                                                        {"key": 3, "value": 0}, {"key": 4, "value": 0},
#                                                        {"key": 5, "value": 0}]})
#         # 获取ESC运动模式状态.默认False
#         self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetEscSportModeStatus", {}, {"out": False})
#         # 获取陡坡缓降开关状态, 默认False
#         self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetHDCOn", {}, {"out": False})
#         # 获取D档自动关门设置状态，默认空列表
#         self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetAutoCloseTrigger", {}, {"out": []}) # todo:
#         # 获取电动门风抖消除开关状态，默认False
#         self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetWindElimination", {"doors": [4]},
#                                               {"out": [{"id": 4, "on": False}]})
#         # 获取电动门开启模式, 默认1 auto
#         self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorMode",
#                                               {"doors": [4]},
#                                               {"out": [{"id": 0, "mode": 1}, {"id": 1, "mode": 1}, {"id": 2, "mode": 1},
#                                                        {"id": 3, "mode": 1}]})
#         #获取空调首次下线设置
#         self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {},
#                                               {"out":{"acStatus": True, "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22,
#                                                        "windSpeedFirRow": 12, "windSpeedSecRow":12,"airModeDriver":{"isWindModeAuto":True}, 
#                                                        "airModePassenger":{"isWindModeAuto":True}, 
#                                                 "airModeSecRow":{"isWindModeAuto":True},"firstRowPowerStatus": True,"secondRowPowerStatus": True}})
#         self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {},{"out":1})
#         self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":8},{"out":True})
#         self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":9},{"out":True})
#         self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":10},{"out":True})
#         self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":11},{"out":True})
#         self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":12},{"out":True})
#         self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {},{"out":{"level": 0,"channel":0,"ratio":[0,0,0,0,0]}})
#         self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetOutletStatus",{}, {"out":{"driverVentStatus":{"mode":0, "leftHorizontal":50,
#                                                                                 "leftVertical":50, "rightHorizontal":50,"rightVertical":50},
#                                                                                "passVentStatus": {"mode":0, "leftHorizontal":50,"leftVertical":50,"rightHorizontal":50,"rightVertical":50},
#                                                                                "secRowVentStatus":{"mode": 0,"leftHorizontal":50,"leftVertical":50,"rightHorizontal":50,"rightVertical":50}}})
#         self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {},{"out":2})

# -*- coding: utf-8 -*-
        
@allure.feature("性能稳定性")
@allure.story("业务性能/S2S通信性能")
@pytest.mark.soa
class TestSeatService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        sleep(1)
        self.partner = S2sBaseClass([("SeatService", "client"),
                                     ("LowVoltageService", "client"),
                                     ("ChassisService", "client"),
                                     ("BonnetService", "client")])
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()

        self.io_obj = self.io.io_obj
        self.sd_tester.tester_present()
        sleep(2)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSt1',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSts',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSt1',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSts',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSt1',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSts',0)
        self.io.set_four_door_close()
        sleep(1)
        self.set_vehicle_speed(0.0)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        sleep(1)
        # self.Shift_Gear(2)
        self.partner.empty_all()
        logger.info("case开始运行*************************************************************")
    
    def after_each_func(self, ecu):
        # todo 停止抓包
        logger.info("case开始结束*************************************************************")
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)
 
    def after_class(self, ecu):
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        super().after_class(self, ecu)
    
    def set_vehicle_speed(self,X):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', X)
        sleep(1)

    def Shift_Gear(self, X):
        """0代表P挡 2代表N挡 3代表D挡 1代表R挡"""
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', X)
        sleep(1)
        
    def boon_all_open_close(self, swith):
        if swith == 0:
            self.io.hood_door1_open()
            self.io.hood_door2_open()
        else:
            self.io.hood_door1_close()
            self.io.hood_door2_open()
        sleep(1)

    def check_sig(self, X):
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [12]}, {"out": [{"statusValidity": X}]})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{}, {"out":{"validity": X}}) 
        self.partner.send_request_and_ck_resp(LOWVLORAGE_SERVICE_CLIENT, "GetLVFaultValidity", {}, {"out":[{"value":{"faultId": 0, "faultMsg":""},"faultIdValidity": X}]})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetOpenCloseStatusValidity', {}, {"out": {"validity": X}})

    @pytest.mark.repeat(10)
    @allure.title("S2S信号超时判定")
    def test_caseid_1984533(self):
        self.boon_all_open_close(0)
        self.bgm_power_off_and_on(0)
        # bgm重启后先加载镜像，再加载vlan和mount，最后再启动应用，比如S2S，启动后15s内不做信号超时监控和处理，15s以后再做信号超时监控和处理（因BGM性能问题，为避免误报信号超时故障）
        # 加载镜像、vlan和mount耗时统计: https://jiduauto.feishu.cn/wiki/C8i2wDB6xiGOcCkdCVwcKsW7nve?theme=FOLLOW_SYSTEM&contentTheme=DARK&table=tblqVr9smLwmwReL&view=vewpHre1RK
        # 默认1.4为: 3.727+0.836
        # GetBeltStatusValidity等接口有2s的超时
        time1 = time.time()
        time2 = 0
        i = 10
        self.partner.wait_for_service_reconnect(SEAT_SERVICE_CLIENT)
        self.ipdu.pause_bus_send("backbonefr")
        while time.time() - time1 <= (3.727+0.836+15.0):
            self.check_sig(0)
            time.sleep(1) #误差
        else:
            while i > 0:
                i -= 1
                time.sleep(1) #误差
                try:
                    self.check_sig(4)
                    time2 = time.time()
                    logger.info(f"从bgm重启到信号丢失的时间:{time2-time1}")
                    break
                except:
                    pass
        if time2:
            assert (3.727+0.836+15.0) <= (time2-time1) <= (3.727+0.836+15.0+2.0+2.0),"带功能安全的信号超时15s后未检测到"
        self.ipdu.resume_bus_send("backbonefr")
        sleep(3)