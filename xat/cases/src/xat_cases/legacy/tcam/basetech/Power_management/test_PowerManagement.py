#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
import copy
import random
import time
from copy import deepcopy

import allure
import pytest
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.constants.config_data import *
from datetime import datetime
import time
from xat_ecu.api.constants.gb32960_data import *
import json


@allure.feature("TCAM BaseTech/互联服务/电源管理")
class TestPowerManagement(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

        lis = ["VehicleModeService_server", "FotaMasterService_server",
               "VehicleSetStatusService_server", "GB32960Service_server",
               "HighVoltageService_server", "VehicleTimeService_server",
               "CarConfigService_server", "ConfigMasterService_server", "RtcAlarmService_client"]
        self.soa.update(lis)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.bus_comm.resume_all_bus_send()
        self.io.tcam_power_on()
        # self.io.tcam_kl15_down()
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.bus_comm.set_car_mode_to_tcam(CarMode.NORMAL)
        # 每一轮都是 默认值
        self.power_config = deepcopy(power_config_data)
        sleep(3)

    def after_each_func(self, ecu):
        # 恢复发送报文
        self.bus_comm.resume_all_bus_send()
        self.io.tcam_kl15_up()
        self.io.tcam_kl15_up()
        self.io.tcam_power_on()
        sleep(10)  # 等待tcam 唤醒
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        # # 结束后 都恢复默认值
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(power_config_data), app_name="power",
                                                      publish_id=int(time.time()))
        sleep(3)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.io.tcam_power_on()
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.notify_OutputState(on=False)
        # self.mix.stop_get_request_and_send_response_to_tcam_thread()

    def set_power_config_value(self, key_name, key_value):
        '''
         修改  power_config_data 值  每次更改都会记录；重新为self.power_config 赋值则可以去除之前的修改
        @param key_name:
        @param key_value:
        @return:
        '''

        for item in self.power_config:
            for item_key, item_lis in item.items():
                if item_key == "value":
                    for item2 in item_lis:
                        if item2.get("key") == key_name:
                            logger.info(f"{key_name}原始值=={item2.get('value')}")
                            item2["value"] = key_value
                            logger.info(f"设置{key_name}=={key_value}")
                            logger.info(f"self.power_config={self.power_config}")
                            return
        logger.error(f"未找到{key_name} 字段")
        assert 0, f"未找到{key_name} 字段"

    def tcam_is_normal(self, timeout=1):
        '''
        判断在 timeout 时间内 tcam是否变为 Normal模式
        @param timeout: 默认是1秒  至少获取一次
        @return:
        '''

        flag, temp = self.check_tcam_power_status(1, timeout)
        assert flag, "tcam 不是normal 状态"

    def tcam_is_standby(self, timeout=1):
        '''
        判断在 timeout 时间内 tcam是否变为 standby 模式
        @param timeout: 默认是1秒  至少获取一次
        @return:
        '''

        flag, temp = self.check_tcam_power_status(2, timeout)
        assert flag, "tcam 不是 standby 状态"

    def get_timestamp_list(self, string, start_time, end_time):
        '''

        @param string:
        @param start_time: 开始时间 ms
        @param end_time: 结束时间戳 ms
        @return:
        '''
        ret_msg_list = string.split("\n")
        logger.info(f"ret_msg_list={ret_msg_list}")
        time_list = [item[:23] for item in ret_msg_list]
        value_list = []
        for item in time_list:
            datetime_list = item.split(".")
            datetime_str = datetime_list[0]
            # 将字符串转换为datetime对象
            dt_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            # 将datetime对象转换为时间戳
            timestamp1 = int(time.mktime(dt_obj.timetuple())) * 1000

            timestamp2 = int(datetime_list[1])
            timestamp = timestamp1 + timestamp2
            if start_time < timestamp < end_time:
                value_list.append(timestamp)
        logger.info(f"value_list 满足条件有{len(value_list)}个 {value_list}")
        return value_list

    def check_cycle(self, data_list, cycle, buff=1500):
        '''
        @param data_list:
        @param cycle:  s
        @param buff: 偏差 ms
        @return:
        '''
        if len(data_list) == 1:
            assert 0, "只有一组数据"
        flag = True
        for i in range(1, len(data_list)):
            t1 = data_list[i - 1]
            t2 = data_list[i]
            tmp = t2 - t1
            time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t1 / 1000)))
            time2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t2 / 1000)))
            logger.info(f"t1={t1}对应 {time1}")
            logger.info(f"t2={t2}对应 {time2}")
            logger.info(f"时间差t2 - t1={(t2 - t1) / 1000} s")

            logger.info(f"误差为{abs(tmp - cycle * 1000) / 1000} s")
            if abs(tmp - cycle * 1000) > buff:
                flag = False
        assert flag, f"周期不是{cycle}s"

    def check_lcfg_mqtt_time(self, mqtt_time: int):
        '''
        @param mqtt_time: MQTT heartbeat的周期（两次heartbeat间时间） 0~9999second	120second
                0：没有heartbeat功能
                1-30：取30
                31-9999：取实际配置值
        @return:
        '''
        self.updata_tcam_data({"Lcfg_TimerLowUsageModes": 0, "Lcfg_TimerMQTTHbInterval": mqtt_time})
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
        self.waite_singl_tcam_sleep(35)
        t = time.time()
        start_time = int(t * 1000) + 2
        # 开始时间
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t + 2)))
        logger.info(f"开始时间={otherStyleTime}")
        if mqtt_time == 0:
            cycle = 60
        else:
            cycle = 30 if mqtt_time <= 30 else mqtt_time
        logger.info(f"延时{cycle * 5}s")
        sleep(cycle * 5)
        t2 = time.time()
        end_time = int(t2 * 1000) - 2
        # 开始时间
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t2 - 2)))
        logger.info(f"结束时间={otherStyleTime}")
        # 唤醒TCAM  取日志
        self.io.tcam_kl15_up()
        # 等待tcam唤醒
        self.tcam_is_normal(35)
        commands = 'cd /mnt/sdcard/log; /oemapp/bin/zstdcat jetlog_messages | grep -i "nvdTestAlarm_Timer_Hander alarm , wake up!"'
        ret_msg = self.ssh.type_commands(DeviceName.TCAM, commands=commands, timeout=60)
        data_lis = self.get_timestamp_list(ret_msg, start_time, end_time)
        if cycle == 0:
            assert len(data_lis) <= 1, "mqtt_time==0 时候 不应该有心跳"
        else:
            self.check_cycle(data_lis, cycle=cycle)

    def check_tcam_normal_to_backup_under_carmode(self, car_mode: CarMode):
        '''

        @param car_mode:
        @return:
        '''
        self.updata_tcam_data({"Lcfg_TimerLowUsageModes": 30})
        self.bus_comm.set_car_mode_to_tcam(car_mode)
        with allure.step(f"断开tcam的 kl15"):
            self.io.tcam_kl15_down()
        with allure.step(f"停止发送报文"):
            self.bus_comm.pause_all_bus_send()
        with allure.step(f"TCAM 下电"):
            self.io.tcam_power_off()
        try:
            flag, temp = self.check_tcam_power_status(6, timeout=15)
            Flag = flag
        except Exception as e:
            logger.error(str(e))
            temp = str(e)
            Flag = False
        with allure.step(f"TCAM 上电"):
            self.io.tcam_power_on()
        logger.info("延时180秒等tcam上电")
        sleep(3 * 60)
        assert Flag, temp

    def updata_tcam_data(self, name_value_dic):
        '''
        更新参数配置
        @param name_value_dic: {"Lcfg_TimerLowUsageModes": 0}
        @return:
        '''
        self.tcam_is_normal(3)
        for name, value in name_value_dic.items():
            with allure.step(f"设置{name}={value}"):
                self.set_power_config_value(name, value)
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.power_config), app_name="power",
                                                      publish_id=int(time.time()))
        logger.info("下发配置成功")
        sleep(5)
        self.tcam_is_normal(3)

    def check_tcam_power_status(self, value, timeout=50):
        '''

        @param value:
        @param timeout:
        @return:  true  ，状态变化的时间
        '''

        # timeout = 3 * 60
        status_dic = {
            2: "standby",
            1: "Normal",
            6: "BuBatt"
        }
        flag = False
        temp = 0
        string = f"开始等待{timeout}秒上报 {status_dic.get(value)}"
        with allure.step(string):
            logger.info(string)
        t1 = time.time()
        while time.time() - t1 < timeout:
            data = self.tsp.get_tcam_power_status()
            logger.info(f"PowerStatus={data}")
            if data['powerStatus'] == value:
                temp = time.time() - t1
                string = f"tcam 经过{temp}s 变为{status_dic.get(value)}"
                with allure.step(string):
                    logger.info(string)
                flag = True
                break
            sleep(1)
        else:
            string = f"经过{timeout}秒超时, tcam 状态没有上报{status_dic.get(value)}"
            with allure.step(string):
                logger.error(string)
        return flag, temp

    def waite_singl_tcam_sleep(self, configTime=30, timeout=None):
        '''
        等待 单域 tcam 休眠  通过赛博坦平台获取tcam 状态来判断是不是休眠
        @param timeout: 超时时间
        @param timeTemp: 实际需要的时间 单位秒
        @return:
        '''
        if timeout is None:
            timeout = configTime + 30
        with allure.step(f"断开tcam的 kl15"):
            self.io.tcam_kl15_down()
        with allure.step(f"停止发送报文"):
            logger.info(f"停止发报文")
            # sleep(2)
            self.bus_comm.pause_all_bus_send()

        logger.info(f"下发的配置时间为{configTime}秒")
        flag, temp = self.check_tcam_power_status(2, timeout)
        if flag:
            string = f"经过{temp}秒 tcam 变为 standby,实际需要{configTime}左右"
            with allure.step(string):
                logger.info(string)
            # 偏差两秒
            # assert abs(timeTemp - temp) < 2, string
        else:
            string = f"超过{timeout}秒 未收到tcam 上报 Standby"
            with allure.step(string):
                logger.info(string)
                assert 0, string

    @pytest.mark.smoke
    @allure.title("TCAM standby模式下，给TCAM 发送网络管理报文，TCAM 变为normal 状态")
    def test_caseid_1978498(self):
        self.updata_tcam_data({"Lcfg_TimerLowUsageModes": 30})
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
        self.waite_singl_tcam_sleep(60)
        with allure.step(f"connectivitycanfd发送 0x533 网络管理报文唤醒"):
            self.bus_comm.ipdu.add_msg("connectivitycanfd", 0x533, [0x33, 0x40, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff])
            self.bus_comm.send_pdu("connectivitycanfd", 0x533, [0x33, 0x40, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff],
                                   cycle_time=20)
        self.tcam_is_normal(60)

    @pytest.mark.smoke
    @allure.title("Standby_to_Normal_by_IP：使用远控指令给TCAM下发送远控解闭锁指，电源模式从 Standby 切换为 normal")
    def test_caseid_1978496(self):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
        self.waite_singl_tcam_sleep(60)
        with allure.step(f"发送远控接闭锁指令，查看电源模式是否切换为Normal模式"):
            self.tsp.rvc_lock_control(1)
            # self.tsp.rvc_lock_control(0)
        self.tcam_is_normal(60)

    @pytest.mark.smoke
    @allure.title("Standby_to_Normal_by_RTC：设置2min RTC定时任务，电源模式从 Standby 切换为 normal")
    def test_caseid_1978494(self):
        self.tcam_is_normal(6 * 60)
        self.soa.send_SetBookEvent_req(ser_name="HighVoltageAppService", sch_time=300)
        self.waite_singl_tcam_sleep(180)
        self.tcam_is_normal(6 * 60)

    @pytest.mark.smoke
    @allure.title("设置UsageMode=ABANDONED,断掉kl15,停止发送网络管理报文，tcam进入Standby 模式")
    def test_caseid_1978493(self):
        self.updata_tcam_data({"Lcfg_TimerLowUsageModes": 30})
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
        self.waite_singl_tcam_sleep(configTime=30)

    @pytest.mark.sanity
    @allure.title("Normal_to_Backup_carmode_normal")
    def test_caseid_1978491(self):
        self.check_tcam_normal_to_backup_under_carmode(CarMode.NORMAL)

    @pytest.mark.sanity
    @allure.title("Normal_to_Backup_carmode_dyno")
    def test_caseid_1978489(self):
        self.check_tcam_normal_to_backup_under_carmode(CarMode.DYNO)

    @pytest.mark.sanity
    @allure.title("Normal_to_Backup_carmode_crash")
    def test_caseid_1978490(self):
        self.check_tcam_normal_to_backup_under_carmode(CarMode.CRASH)

    @pytest.mark.sanity
    @allure.title("Config_Lcfg_TimerLowUsageModes_0")
    def test_caseid_1978483(self):
        self.updata_tcam_data({"Lcfg_TimerLowUsageModes": 0})
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
        self.waite_singl_tcam_sleep(configTime=0)

    @pytest.mark.sanity
    @allure.title("Config_Lcfg_TimerLowUsageModes_30")
    def test_caseid_1978482(self):
        self.updata_tcam_data({"Lcfg_TimerLowUsageModes": 30})
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
        self.waite_singl_tcam_sleep(configTime=30)
        #

    @pytest.mark.sanity
    @allure.title("Config_Lcfg_TimerLowUsageModes_999")
    def test_caseid_1978481(self):
        self.updata_tcam_data({"Lcfg_TimerLowUsageModes": 999})
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
        self.waite_singl_tcam_sleep(configTime=999)
        # 1978481

    # @pytest.mark.sanity
    # @allure.title("Config_Lcfg_TimerLowUsageModes_N")
    # def test_caseid_1978480000(self):
    #     t = random.randint(31, 300)
    #     logger.info(f"设置Lcfg_TimerLowUsageModes={t}")
    #     self.updata_tcam_data({"Lcfg_TimerLowUsageModes": t})
    #     self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
    #     self.waite_singl_tcam_sleep(configTime=t)

    @pytest.mark.sanity
    @allure.title("Config_Lcfg_TimerMQTTHbInterval_0")
    def test_caseid_1978474(self):
        self.check_lcfg_mqtt_time(0)

    @pytest.mark.sanity
    @allure.title("Config_Lcfg_TimerMQTTHbInterval_1")
    def test_caseid_1978473(self):
        self.check_lcfg_mqtt_time(1)

    @pytest.mark.sanity
    @allure.title("Config_Lcfg_TimerMQTTHbInterval_20")
    def test_caseid_1978472(self):
        self.check_lcfg_mqtt_time(20)

    @pytest.mark.sanity
    @allure.title("Config_Lcfg_TimerMQTTHbInterval_30")
    def test_caseid_1978471(self):
        self.check_lcfg_mqtt_time(30)

    @pytest.mark.sanity
    @allure.title("Config_Lcfg_TimerMQTTHbInterval_31")
    def test_caseid_1978470(self):
        self.check_lcfg_mqtt_time(31)

    @pytest.mark.sanity
    @allure.title("Config_Lcfg_TimerMQTTHbInterval_120")
    def test_caseid_1978469(self):
        self.check_lcfg_mqtt_time(120)

    @pytest.mark.sanity
    @allure.title("Config_Lcfg_TimerMQTTHbInterval_300")
    def test_caseid_1978468(self):
        # 时间过长 本应9999 设置 300
        self.check_lcfg_mqtt_time(300)

    # @pytest.mark.full
    # @allure.title("Config_Lcfg_TimerMQTTHbInterval_9999")
    # def test_caseid_1978468(self):
    #     # 时间过长
    #     self.check_lcfg_mqtt_time(9999)

    @pytest.mark.smoke
    @allure.title("TCAM standby模式下，给TCAM 发送应用报文，TCAM 变为normal 状态")
    def test_caseid_100444(self):
        self.updata_tcam_data({"Lcfg_TimerLowUsageModes": 30})
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
        self.waite_singl_tcam_sleep(60)

        self.bus_comm.resume_ecu_send("connectivitycanfd", "BGM")
        self.tcam_is_normal(60)

    @pytest.mark.Sanity
    @allure.title("tcam 在normal状态下 断电进入备电模式")
    def test_caseid_100251(self):
        self.io.tcam_kl15_up()
        self.tcam_is_normal(60)
        self.io.tcam_power_off()
        flag, temp = self.check_tcam_power_status(6, 20)
        self.io.tcam_power_on()
        logger.info("等待tcam 启动 延时 3min")
        sleep(3 * 60)
        assert flag, "tcam 未进入备电模式"

    @pytest.mark.full
    @allure.title("tcam 在standby模式下断电 不会进入备电模式")
    def test_caseid_1978486(self):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
        self.waite_singl_tcam_sleep(60)
        self.io.tcam_power_off()
        flag, temp = self.check_tcam_power_status(6, 20)
        self.io.tcam_kl15_up()
        self.io.tcam_power_on()
        logger.info("等待tcam 启动 延时 3min")
        sleep(3 * 60)
        assert not flag, "tcam 未进入备电模式"

    @pytest.mark.full
    @allure.title("休眠唤醒网络状态压力测试")
    def test_caseid_1985775(self):
        self.waite_singl_tcam_sleep(60)
        with allure.step(f"connectivitycanfd发送 0x533 网络管理报文唤醒"):
            self.bus_comm.ipdu.add_msg("connectivitycanfd", 0x533, [0x33, 0x40, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00])
            self.bus_comm.send_pdu("connectivitycanfd", 0x533, [0x33, 0x40, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00],
                                   cycle_time=20)
        self.tcam_is_normal(60)
        self.io.tcam_power_on()
        self.bus_comm.resume_all_bus_send()
        t = time.time()
        ret_msg = ""
        while time.time() - t < 33:
            ret_msg = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig', timeout=30)
            logger.info(f"获取的tcam 网卡信息为{ret_msg}")
            if "rmnet_data0" in ret_msg and "rmnet_data1" in ret_msg:
                string = f"耗时{time.time() - t}秒 获取到两个网卡"
                with allure.step(string):
                    logger.info(string)
                break
            sleep(2)
        else:
            string = f"耗时{time.time() - t}秒 未同时获取获取到rmnet_data0 和rmnet_data1 网卡"
            with allure.step(string):
                logger.error(string)
            assert "rmnet_data0" in ret_msg, "rmnet_data0 网卡不存在"
            assert "rmnet_data1" in ret_msg, "rmnet_data1 网卡不存在"


#  pytest basetech/Power_management/test_PowerManagement.py --disable_env=true -k test_caseid_1978482
