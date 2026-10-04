#!/usr/bin/env python
# -*- encoding]: utf-8 -*-
#实车启动场景event事件上报时间压测

import pytest
import statistics
from xat_ecu.legacy.driver.ssh_interface import *
from xat_cases.legacy.soa.performance_stability.Real_vehicle_stability.test_service_available_time import get_cpu, get_mem
from xat_cases.legacy.soa.case_helper.test_real_vehicle_base import TestBase


TIMES = 100

INTERFACE_EVENT = {3764361480: ['HighVoltageService', 'ChargingInfo'], 
                   2576384672:['ChargeLidService','Status'],
                   3905050242:['KeyService','NotifyCarLocalTraceActiveStatus'],
                   2573719577:['LightService','NotifyTurnLampStatus'],
                   1603625267:['TailGateService','Status'],
                   2192928286:['WindowService','WindowPosition'],
                   2703728917:['ClimateControlService','RemotePowerStatus'],
                   156330547:['ClimateControlService','ClimateSystemStatus'],
                   1222908817:['SteerWheelService','Heat'],
                   186657022:['ClimateControlService','RemoteClimateHVStatus'],
                   3968326422:['ClimateControlService','NotifyACDefrostSts'],
                   914863885:['SeatService','FrntLeftSeatHeatVentStatus'],
                   801446018:['SeatService','RearLeftSeatHeatVentStatus'],
                   4217081053:['SeatService','FrntRightSeatHeatVentStatus'],
                   5114530:['SeatService','RearRightSeatHeatVentStatus'],
                   2140997147:['ChassisService','Gear'],
                   3393195226:['VehicleModeService','CarModeChanged'],
                   2273311786:['VehicleModeService','UsageModeChanged'],
                   2272577263:['TailGateService','OpenCloseStatus'],
                   1583234566:['CentralLockService','LockStatus'],
                   387472870:['DoorService','FrntLeftDoorSts'],
                   3603816579:['DoorService','FrntRightDoorSts'],
                   2842087236:['DoorService','RearLeftDoorSts'],
                   4048776321:['DoorService','RearRightDoorSts'],
                   2160738084:['SeatService','SeatOccupyStatus'],
                   3450210813:['ChargeLidService','ChargeLidPos'],
                   1110827564:['WTIService','TelltaleList'],
                   647865524:['WTIService','WarningMsgList'],
                   150883928:['CTDService','alarmInfo'],
                   2083373127:['PedalService','BrakePedalStatus'],
                   2668986389:['DoorService','DoorIceBreakActiveStatus'],
                   2786655799:['SeatService','FrntLeftSeatPosition'],
                   3674310866:['SteerWheelService','SteerWheelPositionChanged'],
                   3946618809:['CentralLockService','LockSuccessTriggerSource']

                }


class TestEvent(TestBase):
    def before_class(self, ecu):
        '''测试用例的前处理'''
        super().before_class(self, ecu)
        self.event_times = {key: [] for key in INTERFACE_EVENT.keys()}
        self.max_connect_time = {key: (0, 0) for key in INTERFACE_EVENT.keys()}
        self.mean_cpu = []
        self.mean_mem = []
        command_send(device_name='BGM', connect_type='obd', cmd='mkdir /log/log_back')

    def after_class(self, ecu):
        '''测试用例全部完成后的后处理'''
        command_send(device_name='BGM', connect_type='obd', cmd='mv /log/log_back/jetlog_* /log/')
        logger.info("="*50 + "所有event事件上报耗时" + "="*50)
        for k,w in INTERFACE_EVENT.items():
            logger.info(f'重启bgm域控{TIMES}次，获取到的时间次数{len(self.event_times[k])}，服务{w[0]}接口{w[1]}的event的发送时间列表：{self.event_times[k]}')
        logger.info("="*50 + "最大连接耗时" + "="*50)
        for k,w in INTERFACE_EVENT.items():
            ser_conn_times = self.max_connect_time[k]
            logger.info(f"服务名{w[0]}，接口名{w[1]}的最大连接耗时出现在第{ser_conn_times[0]}次，时间为{ser_conn_times[1]}")
        logger.info("="*50 + "cpu和内存的平均使用" + "="*50)
        for i in range(TIMES):         
            logger.info(f"第{i+1}次压测cpu的平均使用百分比为{self.mean_cpu[i]*100}%,内存的平均使用为{self.mean_mem[i]}K")
            if i == TIMES - 1:
                logger.info(f"本轮压测cpu的整体平均使用百分比为{round(statistics.mean(self.mean_cpu), 3)*100}%,内存的平均使用为{round(statistics.mean(self.mean_mem), 3)}K")
        
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        '''每个测试用例前置步骤'''
        #file_download(device_name='CDCQ',local_path='./', remote_path= ['/data/account/', connect_type='obd')
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def get_service_time(self, k):
        i = 3
        while i > 0:
            service_cmd = f"/app/bin/zstdcat /log/jetlog_bts|grep {k}|grep -Ein '(#7#|#6#)'"+ "|awk '{print $8}'"
            service_time = command_send(device_name='BGM', connect_type='obd', cmd=service_cmd)[-1].split('\n')[0]
            logger.info(f'服务接口发出event的单调时钟为{service_time}')
            if service_time:
                return service_time
            else:
                i -= 1
                time.sleep(5)

    @pytest.mark.repeat(TIMES)
    def test_caseid_1988185(self, request, connect_type='obd'):
        number = int(request.node.name.split('[')[1].split('-')[0])
        command_send(device_name='BGM', connect_type='obd', cmd='mv /log/jetlog_* /log/log_back/')
        self.sd_tester.send_data([0x11, 0x81])
        time.sleep(60)
        hibernation_cmd = "/app/bin/zstdcat /log/jetlog_messages|grep 'hibernation exit'|awk '{print $8}'"
        hibernation_time = command_send(device_name='BGM', connect_type=connect_type, cmd=hibernation_cmd)[-1].split('\n')[-1]
        logger.info(f'镜像结束的单调时钟为{hibernation_time}')
        for k,w in INTERFACE_EVENT.items():
            service_time = self.get_service_time(k)
            logger.info(f'服务{w[0]}的接口{w[1]}发出event的单调时钟为{service_time}')
            if service_time and hibernation_time:
                time_event = round(((int(service_time)/1000) - (int(hibernation_time.split(',')[2])/1000000) + 3.726), 3)
                logger.info(f'服务{w[0]}的接口{w[1]}发出event耗时{time_event}s')
                self.event_times[k].append(time_event)
                if self.max_connect_time[k][1] < time_event:
                            self.max_connect_time[k] = (number, time_event)
            # else:
            #     assert False,f"第{number}次压测服务{w[0]}的接口{w[1]}发出event时间为空"

        # 获取event上报平均事件
        logger.info("="*50 + "平均event事件上报的时间" + "="*50)
        for k,w in INTERFACE_EVENT.items():
            if len(self.event_times[k]) > 0:
                mean_time = round(statistics.mean(self.event_times[k]), 3)
                logger.info(f"第{number}次压测服务{w[0]}的接口{w[1]}发出event的平均时间为{mean_time}")
            else:
                logger.info(f"第{number}次压测服务{w[0]}的接口{w[1]}发出event的平均时间为空")

        # cpu和内存的使用
        mean_cpu = get_cpu(self.bgmcli)
        mean_mem = get_mem(self.bgmcli)
        self.mean_cpu.append(mean_cpu)
        self.mean_mem.append(mean_mem)

        # 校验s2s卡死问题和error日志
        try:
            data = command_send(device_name='BGM', connect_type=connect_type, cmd="/app/bin/zstdcat /log/jetlog_messages*|grep -Ein '( E s2s| E handy:|RT throttling activated)'", timeout=10)
            if ' E s2s' in data:
                assert False,f'检测到s2s有error日志{data}'
            elif ' E handy' in data:
                assert False,f'检测到socket绑定服务端的地址和端口有error日志{data}'
            elif 'RT throttling activated' in data:
                assert False,f'检测到s2s线程卡死的日志{data}'
            else:
                assert True,'没有Error日志'
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    pytest.main()


# pytest -vs performance_stability/Real_vehicle_stability/test_event_performance.py --disable_partner=true --bl_ver=v_2_0_0
