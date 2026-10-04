#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
#实车四域服务连接可用时间压测

import json
import os
import zstandard as zstd
import statistics
import pytest
import sys
import time

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.soa.case_helper.test_real_vehicle_base import TestBase
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.driver.ssh_interface import *


test_times = 100


def zst2txt(file_path, compressed_file):
    '''
    @desp: 日志文件的预处理，".zst"压缩文件
        依赖库: zstandard （pip install zstandard）
    '''
    dctx = zstd.ZstdDecompressor()
    with dctx.stream_reader(compressed_file) as reader:
        with open(file_path.replace('.zst', ''), 'wb') as output:
            while True:
                chunk = reader.read(16384)  # 16KB buffer size
                if not chunk:
                    break
                output.write(chunk)


def paser_file(file_path):
    files = os.listdir(file_path)
    data = []
    for file in files:
        if file.endswith(".zst"):
            with open(os.path.join(file_path, file), 'rb') as log_path:
                data.append(zst2txt(os.path.join(file_path, file), log_path).split("\n"))
    return data


# 远控
remote_control_services = {
    "TailGateService": ["pavaro", "car_service", "rvc"],
    "HighVoltageService": ["pavaro", "car_service", "power_service_app", "gb32960_service", "rvc"],
    "ChargeLidService": ["car_service", "rvc"],
    "LightService": ["pavaro", "car_input_servi", "car_service", "power_service_app", "lightservice", "rvc"],
    "ClimateControlService": ["pavaro", "car_service", "rvc"],
    "WindowAppService": ["car_service", "rvc"],
    "ShieldWindowService": ["rvc", "car_service"],
    "DoorService": ["pavaro", "car_service", "rvc"]
}

# 舒适进出
critical_services = {
    "KeyService": ["car_service", "rvc"],
    "PedalService": ["car_service"],
    "ChassisService": ["pavaro", "car_service", "rvc", "xcall_service"],
    "SeatService": ["pavaro", "car_service", "rvc", "xcall_service"],
    "SteerWheelService": ["pavaro", "car_input_servi", "car_service"],
    "CentralLockService": ["pavaro", "car_service", "rvc"],
    "VehicleModeService": ["pavaro", "car_service", "rvc","xcall_service"]
}

# s2s关键基础服务
S2S_critical_services = {
    "WTIService": ["car_service"],
    "CarConfigService": ["pavaro", "gb32960_service", "vehicle_data_mi", "car_service"],
    "WindowService": ["car_service", "rvc"],
    "EntryService": ["car_service"],
    "WiperService": ["pavaro", "power_service_app", "car_input_servi", "car_service"],
    "OuterRearViewService": ["pavaro","car_service"],
    "LowVoltageService": ["car_service"],
    "TyreService": ["pavaro", "car_service"],
    "InterCommService": [""],
    "BlueToothService": ["car_service"],
    "CTDService": ["pavaro", "car_service"]
}

#s2s其他服务
S2S_other_services = {
    "TweeterService":["car_service"],
    "ReverseProxyService":[""],
    "DrivingAssistService":["pavaro", "car_service"],
    "PassiveSafetyService":["car_service"],
    "TailWingService":["car_service"],
    "GloveBoxService":["car_service"],
    "HornService":["car_service"],
    "BonnetService":["pavaro", "car_service"],
    "GB32960Service":["gb32960_service"],
    "WirelessPhoneChargingService":["car_service"],
    "WTIAutoDriveService":["car_service"],
    "InnerRearViewService":["car_service"],
    "ErgonomicsService":["carcontrolservir", "account_servicear"],
}

#s2s整车时间
S2S_services = {
    "VehicleTimeService": ["pavaro", "time_service_server", "phc2sys", "rvc"],
}


def get_mem(bgmcli):
    cmd = "/app/bin/zstdcat /log/jetlog_messages|grep ' Mem :'|awk '{print $14}'"
    data = bgmcli.type_commands(cmd)
    if data:
        mem_list = [float(i[:-1]) for i in data.split('\n') if i!='']
        mean_mem = round(statistics.mean(mem_list), 3)
        return mean_mem
    

def get_cpu(bgmcli):
    cmd = "/app/bin/zstdcat /log/jetlog_messages|grep ' CPU :'|awk '{print $16}'"
    data = bgmcli.type_commands(cmd)
    if data:
        cpu_list = [(100.0 - float(i[:-1]))/100 for i in data.split('\n') if i!='']
        mean_cpu = round(statistics.mean(cpu_list), 3)
        return mean_cpu


def is_valid_time_format(time_str):
    import re
    pattern = r"\d{2}:\d{2}:\d{2}.\d{3}"
    if re.match(pattern, time_str):
        return True
    else:
        return False
    

def get_checkinfo(file):
    with open(os.path.join(project_root, "test_case/soa/performance_stability", file), 'r') as fd:
        data = json.load(fd)
    check_info = []
    for i in data["module"][0]["log"]:
        for k,w in i.items():
            if k == "logname":
                check_info.append({w:i['logcomment']})
    return check_info


def get_pid():
    pid_list = []
    for i in ["s2s_service", "SOAApp"]:
        pid = ip.type_commands(f"ps -ef|grep {i}|grep -v grep|" + "awk '{print $2}'", timeout=10).strip()
        if pid:
            pid_list.append(pid)
        else:
            assert False,f"{i}进程的pid获取失败"

    return "|".join(pid_list)


def check_bgm(file):
    info = get_checkinfo(file)
    fail_info = []
    ip = BGM_SSH(hostname="169.254.19.1")
    data = ip.type_commands("/app/bin/zstdcat /log/jetlog_messages*|grep -Ein '(E handy:|RT throttling activated)'", timeout=10)
    if ' E handy' in data:
        logger.info(data)
        fail_info.append("检测到socket绑定服务端的地址和端口失败")
    elif 'RT throttling activated' in data:
        logger.info(data)
        fail_info.append("检测到s2s线程卡死")
    else:
        for pro in info:
            for k,w in pro.items():
                try:
                    if "|" in k:
                        data = ip.type_commands(f"/app/bin/zstdcat /log/jetlog_messages|grep -E '(E s2sF:|E s2sTimer:)'|grep -Ein '({k})'", timeout=10)
                    else:
                        data = ip.type_commands(f"/app/bin/zstdcat /log/jetlog_messages|grep -E '(E s2sF:|E s2sTimer:)'|grep '{k}'", timeout=10)
                    if k in data and "/app/bin/zstdcat" not in data:
                        logger.info(data)
                        fail_info.append(w)
                except Exception as e:
                    logger.error(e)

    if len(fail_info) > 0:
        assert False,f"{fail_info}"


def get_reboot_to_snapshot_time():
    """
    从mcu启动到镜像开始加载的时间
    """
    i = 3
    while i >0:
        number = ip.get_version().get("build_version")[7:-3]
        if number:
            if int(number) >= 140:
                logger.info("BGM版本为140版本及以上")
                return 3.726
            else:
                logger.info("BGM版本为131版本及以下")
                return 3.660
        else:
            i -= 1


def get_snapshot_to_server_time(server, pro):
    """
    镜像加载完成到服务连接的时间
    """
    global jetlog_bts,jetlog_messages
    if pro == '':
        logger.info(f"服务{server}没有域外进程连接")
        return 0.0
    else:
        i = 3
        jetlog_bts = 'jetlog_bts'
        jetlog_messages = 'jetlog_messages'
        while i > 0:
            logger.info(f"第{4-i}次检测域外进程连接的log名: {jetlog_bts}, {jetlog_messages}")
            snapshot_data = ip.type_commands(f"/app/bin/zstdcat /log/{jetlog_messages}|grep 'hibernation exit'|" + "awk '{print $8}'", timeout=10)
            server_data = ip.type_commands(f"/app/bin/zstdcat /log/{jetlog_bts}|grep 'cur-state:0'| grep '{server}'| grep {pro}|" + "awk '{print $8}'", timeout=30)
            if snapshot_data and server_data:
                try:
                    snapshot_time = snapshot_data.split('\n')[-1].split(',')[2].strip()
                    server_time = server_data.split('\n')[-1].strip()
                    logger.info(f"镜像结束的单调时钟为{snapshot_time}")
                    logger.info(f"服务成功连接的单调时钟为{server_time}")
                    conn_time = round((int(server_time)/1000) - (int(snapshot_time)/1000000), 3)
                    logger.info(f"服务{server}连接进程{pro}耗时{conn_time}s")
                    return conn_time
                except Exception as e:
                    logger.info(e)
                    logger.info("获取镜像加载完成的时间或者服务连接的时间有误")
            elif snapshot_data and not server_data:
                time.sleep(1)
                i -= 1
                logger.info("======jetlog_bts没有检测到======")
                bts_now = ip.type_commands(f"ls /log/jetlog_bts* -lh")
                if "-> /log/jetlog_bts" in bts_now:
                    bts_num = bts_now.split('\n')[0].split("->")[-1].split('_')[1][3:]
                    if int(bts_num) > 1:
                        bts_name = "jetlog_bts" + str(int(bts_num)-1)
                        jetlog_bts = bts_name + "*"
            elif server_data and not snapshot_data:
                time.sleep(1)
                i -= 1
                logger.info("======jetlog_messages没有检测到======")
                messages_now = ip.type_commands(f"ls /log/jetlog_messages* -lh")
                if "-> /log/jetlog_messages" in messages_now:
                    messages_num = messages_now.split('\n')[0].split("->")[-1].split('_')[1][8:]
                    if int(messages_num) > 1:
                        messages_name = "jetlog_messages" + str(int(messages_num)-1)
                        jetlog_messages = messages_name + "*"
            else:
                time.sleep(1)
                i -= 1
                logger.info("======jetlog_bts和jetlog_messages均没有检测到======")
                bts_now = ip.type_commands(f"ls /log/jetlog_bts* -lh")
                if "-> /log/jetlog_bts" in bts_now:
                    bts_num = bts_now.split('\n')[0].split("->")[-1].split('_')[1][3:]
                    if int(bts_num) > 1:
                        bts_name = "jetlog_bts" + str(int(bts_num)-1)
                        jetlog_bts = bts_name + "*"
                messages_now = ip.type_commands(f"ls /log/jetlog_messages* -lh")
                if "-> /log/jetlog_messages" in messages_now:
                    messages_num = messages_now.split('\n')[0].split("->")[-1].split('_')[1][8:]
                    if int(messages_num) > 1:
                        messages_name = "jetlog_messages" + str(int(messages_num)-1)
                        jetlog_messages = messages_name + "*"
        else:
           f"服务{server}连接进程{pro}耗时检测失败"
           return 0.0
            

def get_ServiceRun_end_time(server):
    """
    服务ServiceRun end时间
    """
    ser = ""
    if server == 'VehicleTimeService':
        return 0.0
    elif server == 'WirelessPhoneChargingService':
        ser = 'wpc_service'
    elif server == 'HighVoltageService':
        ser = 'highvoltage_service'
    elif server == "CTDService":
        ser = "CTD"
    else:
        for i, char in enumerate(server.replace("Service", "")):
            if check_case(char):
                ser += ".*" + server[i:i+1].lower()
            else:
                ser += char
    logger.info(f"检测的服务: {ser}")
    i = 3
    jetlog_messages = 'jetlog_messages'
    while i > 0:
        logger.info(f"第{4-i}次检测ServiceRun end的log名: {jetlog_messages}")
        end_ = ip.type_commands(f"/app/bin/zstdcat /log/{jetlog_messages}|grep 'ServiceRun end'|grep {ser}" + "|awk '{print $2}'", timeout=10)
        if end_:
            end_time = end_.split('\n')[-1].strip()
            logger.info(f"ServiceRun end时间戳为: {end_time}")
            if is_valid_time_format(end_time):
                return float(end_time[-5:])
        else:
            i -= 1
            time.sleep(1)
            messages_now = ip.type_commands(f"ls /log/jetlog_messages* -lh")
            if "-> /log/jetlog_messages" in messages_now:
                messages_num = messages_now.split('\n')[0].split("->")[-1].split('_')[1][8:]
                if int(messages_num) > 1:
                    messages_name = "jetlog_messages" + str(int(messages_num)-1)
                    jetlog_messages = messages_name + "*"
    else:
        assert False,f"服务{server}的ServiceRun end时间检测不到，请线下修正"


def check_case(character):
    if character.isupper():
        return True
    else:
        return False

def get_read_storage_time(timeout=10):
    try:
        ip.type_commands("rm /data/message_data", root_permission=True)
        cmd = '/app/bin/zstdcat /log/jetlog_messages > /data/message_data'
        ip.type_commands(cmd, root_permission=True, timeout=timeout)
        start_time = ip.type_commands("cat /data/message_data|grep 'ReadStorage start'|awk '{print $2}'", timeout=10).split('\n')[0]
        s2d_pid = ip.type_commands("cat /data/message_data|grep 'ReadStorage start'|awk '{print $3}'", timeout=10).split('\n')[0]
        cmd = f"cat /data/message_data|grep {s2d_pid}" + "|grep 'ReadStorage end'|awk '{print $2}'"
        end_time = ip.type_commands(commands=cmd, timeout=10).split('\n')[-1]
        logger.info(f"读取数据库开始时间{start_time}")
        logger.info(f"读取数据库结束时间{end_time}")
        if is_valid_time_format(start_time) and is_valid_time_format(end_time):
            DB_time = float(end_time[7:]) - float(start_time[7:])
            return DB_time
        else:
            logger.info("jetlog_messages读取数据库时间获取有误")
            return 0.0
    except Exception as e:
        return 0.0


@pytest.mark.full
class TestPerformanceConnTime(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        global ip
        ip = self.bgmcli
        logger.info("查看BGM是否是S2D启动")
        self.reboot_time = get_reboot_to_snapshot_time()
        self.bgmcli.type_commands("mkdir /log/log_back;mv /log/jetlog_* /log/log_back/", timeout=10)
        # 初始化参数
        remote_control_services.update(critical_services)
        remote_control_services.update(S2S_critical_services)
        remote_control_services.update(S2S_other_services)
        remote_control_services.update(S2S_services)
        self.connect_times = {key: [] for key in remote_control_services.keys()}
        self.connect_mean_time = {key: [] for key in remote_control_services.keys()}
        self.max_connect_time = {key: (0, 0) for key in remote_control_services.keys()}
        self.connect_process_num = {key: [[0]] for key in remote_control_services.keys()}
        self.ServiceRun_end_con_time = {key: [] for key in remote_control_services.keys()}
        self.db_time = []
        self.mean_cpu = []
        self.mean_mem = []

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
      
    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.bgmcli.type_commands('mv /log/log_back/jetlog_* /log/')
        logger.info("="*50 + "读取数据库时间,0.0代表没有查到" + "="*50)
        for i in range(test_times):
            logger.info(f"第{i+1}次压测读取数据库耗时为{self.db_time[i]}")
        logger.info("="*50 + "最大连接耗时时间" + "="*50)
        for key in self.max_connect_time:
            ser_conn_times = self.max_connect_time[key]
            logger.info(f"最大连接耗时出现在第{ser_conn_times[0]}次，时间为{ser_conn_times[1]} ---- {key}")
        for i in range(test_times):         
            logger.info(f"第{i+1}次压测cpu的平均使用百分比为{round(self.mean_cpu[i], 3)*100}%,内存的平均使用为{self.mean_mem[i]}K")
            if i == test_times - 1:
                logger.info(f"本轮压测cpu的整体平均使用百分比为{round(statistics.mean(self.mean_cpu), 3)*100}%,内存的平均使用为{round(statistics.mean(self.mean_mem), 3)}K")
        
        super().after_class(self, ecu)

    def s_timestamp(self):
        """
        获取时间戳
        :return: str
        """
        return time.strftime("%Y%m%d%H%M%S", time.localtime())

    def sd_reboot_bgm(self):
        """
        诊断重启BGM
        """
        logger.info("诊断重启BGM")
        self.sd_tester.send_data([0x11, 0x81])

    @pytest.mark.smoke
    @pytest.mark.repeat(test_times)
    def test01_caseid_1913747(self, request):
        number = int(request.node.name.split('[')[1].split('-')[0])
        #上下电解析日志
        self.sd_reboot_bgm()
        tmp_partners = [key for key in remote_control_services.keys()]
        logger.info("BGM上电")
        time.sleep(40)
        DB_time = get_read_storage_time(5)
        self.db_time.append(DB_time)
        #解析服务连接时间
        while tmp_partners:
            for k,w in remote_control_services.items():
                #ServiceRun_end时间ServiceRun_end_time
                self.connect_process_num[k].append([])
                ServiceRun_end_time = get_ServiceRun_end_time(k)
                self.ServiceRun_end_con_time[k].append(round(self.reboot_time + ServiceRun_end_time, 3))
                #域外进程连接时间_process_time
                for process in w:
                    if process == "vehicle_data_mi":
                        # vehicle_data_mi进程在bgm和tcam端都有，所以需要特殊处理
                        cmd = "ps -ef| grep vehicle_data_mi| grep -v grep| awk '{print $1}'"
                        tcam_pid = command_send(device_name='TCAM', connect_type='obd', cmd=cmd)[-1]
                        if tcam_pid:
                            _process_time = get_snapshot_to_server_time(k+":"+tcam_pid, process)
                    else:
                        _process_time = get_snapshot_to_server_time(k, process)
                    if _process_time != 0.0:
                        self.connect_process_num[k][number].append(_process_time)
                        # process_time = max(_process_time, ServiceRun_end_time)
                        logger.info(f"服务{k}的Run end时间为:{ServiceRun_end_time},连接进程{process}的时间为{_process_time}")
                        con_time = round(self.reboot_time + _process_time, 3)
                        self.connect_times[k].append(con_time)
                        if self.max_connect_time[k][1] < con_time:
                            self.max_connect_time[k] = (number, con_time)
                logger.info(f"第{number}次压测服务连接所有域外进程的时间为: {self.connect_times[k]}")
                tmp_partners.remove(k)
                
        logger.info("="*50 + "服务连接进程数" + "="*50)
        for k in remote_control_services.keys():
            logger.info(f"第{number}次压测服务连接进程数为{len(self.connect_process_num[k][number])} ---- {k}")
            logger.info(self.connect_process_num[k][1:])
            # 校验每次测试的进程连接数是否一致
            if number >= 2:
                if len(self.connect_process_num[k][number]) != len(self.connect_process_num[k][number-1]):
                    assert False,f"第{number}次压测服务{k}连接的进程数与之前不一致"
            
        logger.info("="*50 + "服务可用时间" + "="*50)
        for k in remote_control_services.keys():
            if len(self.connect_times[k]) != 0:
                self.connect_mean_time[k] =  round(statistics.mean(self.connect_times[k]), 3)
                logger.info(f"第{number}次压测ServiceRun_end/服务连接的平均耗时为{self.ServiceRun_end_con_time[k][0]}/{self.connect_mean_time[k]} ---- {k}")
            else:
                logger.info(f"第{number}次出现服务未连接 ---- {k}")
                #assert False
        # cpu和内存的使用
        mean_cpu = get_cpu(self.bgmcli)
        mean_mem = get_mem(self.bgmcli)
        self.mean_cpu.append(mean_cpu)
        self.mean_mem.append(mean_mem)
        # 备份BGM日志到/data/目录
        if number == test_times:
            self.bgmcli.type_commands(f"rm /data/bgm_log_*;tar -zcvf /data/bgm_log_{self.s_timestamp()}_{test_times}times.tar.gz /log/jetlog* &\\n", timeout=10)
            command_send(device_name='TCAM', connect_type='obd', cmd=f"rm /mnt/sdcard/tcam_log_*;tar -zcvf /mnt/sdcard/tcam_log_{self.s_timestamp()}.tar.gz /mnt/sdcard/log/jetlog* &\\n")
        # 校验jetlog_message日志是否有Error
        check_bgm("s2s_fw.json")


if __name__ == '__main__':
    pytest.main()


# pytest -vs performance_stability/Real_vehicle_stability/test_service_available_time.py --disable_partner=true --bl_ver=v_2_0_0
