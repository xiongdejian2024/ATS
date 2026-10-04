#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
#两域服务连接可用时间压测

import json
import os
import zstandard as zstd
import statistics
import pytest
import allure
import sys
import time

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_cases.legacy.soa.case_helper.utils import get_lastest_log

test_times = 50


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
    "TailGateService": ["rvc"],
    "HighVoltageService": ["gb32960_service", "rvc"],
    "ChargeLidService": ["rvc"],
    "LightService": ["rvc"],
    "ClimateControlService": ["rvc"],
    "WindowAppService": ["rvc"],
    "ShieldWindowService": ["rvc"],
    "DoorService": ["rvc"]
}

# 舒适进出
critical_services = {
    "KeyService": ["rvc"],
    "PedalService": ["rvc"],
    "ChassisService": ["rvc", "xcall_service"],
    "SeatService": ["rvc", "xcall_service"],
    "SteerWheelService": ["rvc"],
    "CentralLockService": ["rvc"],
    "VehicleModeService": ["rvc","xcall_service"]
}

# s2s关键基础服务
S2S_critical_services = {
    "WTIService": [],
    "CarConfigService": ["gb32960_service", "vehicle_data_mi"],
    "WindowService": ["rvc"],
    "EntryService": [],
    "WiperService": [],
    "OuterRearViewService": ["rvc"],
    "LowVoltageService": [],
    "TyreService": [],
    "InterCommService": [],
    "BlueToothService": [],
    "CTDService": []
}

#s2s其他服务
S2S_other_services = {
    "TweeterService":[],
    "ReverseProxyService":[],
    "DrivingAssistService":[],
    "PassiveSafetyService":[],
    "TailWingService":[],
    "GloveBoxService":[],
    "HornService":[],
    "BonnetService":[],
    "GB32960Service":["gb32960_service"],
    "WirelessPhoneChargingService":[],
    "WTIAutoDriveService":[],
    "InnerRearViewService":[],
    "ErgonomicsService":[],
}

#s2s整车时间
S2S_services = {
    "VehicleTimeService": ["phc2sys"],
}


SOAApp = ["ConditionCheckServiceImp:", "ResetSOA:", "VehicleControlFaultServiceImp:", "HighVolApp:", "VehicleSetStatusService:"]

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
    for pro in info:
        for k,w in pro.items():
            try:
                if "|" in k:
                    data = ip.type_commands(f"/app/bin/zstdcat /log/jetlog_messages*|grep -E '(E s2sF:|E s2sTimer:)'|grep -Ein '({k})'", timeout=300)
                else:
                    data = ip.type_commands(f"/app/bin/zstdcat /log/jetlog_messages*|grep -E '(E s2sF:|E s2sTimer:)'|grep '{k}'", timeout=300)
                if k in data:
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
    number = ip.get_version().get("build_version")[7:-3]
    if 140 <= int(number) < 220:
        logger.info("BGM版本为140版本及以上")
        return 3.726
    elif int(number) <= 131:
        logger.info("BGM版本为131版本及以下")
        return 3.660
    else:
        return 3.4

def get_hibernation_exit_time():
    """
    镜像加载完成的单调时间
    """
    i = 2
    jetlog_messages = "/log/jetlog_messages"
    while i > 0:
        snapshot_time = ip.type_commands(f"/app/bin/zstdcat {jetlog_messages}|" + "grep 'hibernation exit'|awk '{print $8}'", timeout=10)
        try:
            once_time = snapshot_time.split('\n')[-1]
            logger.info(f"镜像结束时的单调时钟为{once_time}")
            return int(once_time.split(',')[2].strip())/1000000
        except Exception as e:
            logger.error(f"报错原因：{e}")
            data = ip.type_commands("ls -lh /log/jetlog_messages").split('\n')[0]
            logger.info(f"第{3-i}次查询镜像加载完成单调时间的日志：{data}")
            num = data.split('jetlog_messages -> ')[-1].split("/log/jetlog_messages")[-1].split('_')[0]
            if int(num) == 1:
                jetlog_messages = jetlog_messages
            else:
                jetlog_messages = jetlog_messages + str(int(num)-1) + "*"
            i -= 1
                
    else:
        return None

def get_server_conn_sucess_time(server, pro):
    """
    服务连接成功的单调时间
    """
    i = 2
    jetlog_bts = "/log/jetlog_bts"
    while i > 0:
        server_time = ip.type_commands(f"/app/bin/zstdcat {jetlog_bts}|grep 'cur-state:0'| grep '{server}'| grep {pro}|" + "awk '{print $8}'", timeout=10)
        try:
            once_time = int(server_time.split('\n')[-1].strip())/1000
            logger.info(f"服务成功连接时的单调时钟为{once_time}")
            return once_time
        except Exception as e:
            data = ip.type_commands("ls -lh /log/jetlog_bts").split('\n')[0]
            logger.info(f"第{3-i}次查询服务连接成功单调时间的日志：{data}")
            num = data.split('jetlog_bts -> ')[-1].split("/log/jetlog_bts")[-1].split('_')[0]
            if int(num) == 1:
                jetlog_bts = jetlog_bts
            else:
                jetlog_bts = jetlog_bts + str(int(num)-1) + "*"
            i -= 1
    else:
        assert False, f"本轮测试服务{server}连接进程{pro}失败，请线下排查！！"


def get_ServiceRun_end_time(server):
    """
    服务ServiceRun end时间
    server: 服务名称
    """
    ser = ""
    if server == 'VehicleTimeService':
        return 0.0
    elif server == 'WirelessPhoneChargingService':
        ser = 'wpc_service'
    elif server == 'HighVoltageService':
        ser = 'highvoltage_service'
    elif server == 'CTDService':
        ser = 'ctd_service'
    else:
        for i, char in enumerate(server.replace("Service", "")):
            if check_case(char):
                ser += ".*" + server[i:i+1].lower()
            else:
                ser += char
    logger.info(f"检测的服务: {ser}")
    i = 2
    jetlog_messages = "/log/jetlog_messages"
    while i > 0:
        end_time = ip.type_commands(f"/app/bin/zstdcat {jetlog_messages}|grep 'ServiceRun end'|grep {ser}" + "|awk '{print $2}'", timeout=10).split('\n')[-1].strip()
        logger.info(f"ServiceRun end时间戳为: {end_time}")
        if is_valid_time_format(end_time):
            end = float(end_time[-5:])
            return end
        else:
            data = ip.type_commands("ls -lh /log/jetlog_messages").split('\n')[0]
            logger.info(f"第{3-i}次查询镜像加载完成单调时间的日志：{data}")
            num = data.split('jetlog_messages -> ')[-1].split("/log/jetlog_messages")[-1].split('_')[0]
            jetlog_messages = jetlog_messages + str(int(num)-1) + "*"
            i -= 1
    else:
        assert False, (f"服务{server}的ServiceRun end时间检测不到，请线下排查！！")


def get_SetDataServiceReady_time(server):
    logger.info(f"检测的服务: {server}")
    i = 2
    jetlog_messages = "/log/jetlog_messages"
    while i > 0:
        end_time = ip.type_commands(f"/app/bin/zstdcat {jetlog_messages}|grep SetDataServiceReady|grep {server}" + "|awk '{print $10}'", timeout=10).split('\n')[-1].strip()
        logger.info(f"服务{server}的SetDataServiceReady时间戳为: {end_time}")
        if "time:" in end_time:
            end = float(end_time.split(':')[-1])/1000
            return end
        else:
            data = ip.type_commands("ls -lh /log/jetlog_messages").split('\n')[0]
            logger.info(f"第{3-i}次查询SetDataServiceReady时间戳的日志：{data}")
            num = data.split('jetlog_messages -> ')[-1].split("/log/jetlog_messages")[-1].split('_')[0]
            jetlog_messages = jetlog_messages + str(int(num)-1) + "*"
        i -= 1
    else:
        return None


def check_S2SService_Resume_time():
    data = ip.type_commands(f"/app/bin/zstdcat /log/jetlog_messages|grep 'S2SService Resume time'", timeout=10).split('\n')[-1]
    resume_time = data.split(":")[-1]
    logger.info(f"S2SService Resume time时间戳为: {resume_time}")
    return resume_time


def check_case(character):
    if character.isupper():
        return True
    else:
        return False

    
def get_read_storage_time(timeout=10):
    """
    获取读数据库的时间
    """
    s2d_pid_num = 0
    s2s_pid = ''
    ip.type_commands("rm /data/message_data", root_permission=True)
    cmd = '/app/bin/zstdcat /log/jetlog_messages > /data/message_data'
    ip.type_commands(cmd, root_permission=True, timeout=timeout)
    data = ip.type_commands("cat /data/message_data|grep 'ReadStorage start'", timeout=10).split('\n')
    for line in data:
        if line:
            line_data = [awk for awk in line.split(' ') if awk != ' ']
            try:
                if line_data and line_data[5] not in SOAApp:
                    s2s_pid = line_data[2]
                    logger.info(f"本轮读取数据库s2s进程的服务启动pid号为：{s2s_pid}")
                    break
            except IndexError:
                continue

    s2d_pid = ip.type_commands("cat /data/message_data|grep 'ReadStorage start'|awk '{print $3}'", timeout=10).split('\n')
    data_begin = []
    for i in range(len((s2d_pid))-2):
        if s2d_pid[i] != s2s_pid and s2d_pid[i+1] == s2s_pid:
            data_begin.append(i+1)
    if data_begin:
        s2d_pid_num = int(data_begin[-1])

    logger.info(f"本轮读取数据库开始位：{s2d_pid_num}")
    logger.info(f"本轮读取数据库s2s进程的服务启动pid号为：{s2s_pid}")

    start_time = ip.type_commands("cat /data/message_data|grep 'ReadStorage start'|awk '{print $2}'", timeout=10).split('\n')[s2d_pid_num]
    
    cmd = f"cat /data/message_data|grep {s2s_pid}" + "|grep 'ReadStorage end'|awk '{print $2}'"
    end_time = ip.type_commands(commands=cmd, timeout=10).split('\n')[-1]
    logger.info(f"读取数据库开始时间{start_time}")
    logger.info(f"读取数据库结束时间{end_time}")
    if is_valid_time_format(start_time) and is_valid_time_format(end_time):
        DB_time = float(end_time[7:]) - float(start_time[7:])
        return DB_time
    else:
        logger.info("jetlog_messages读取数据库时间获取有误")
        return 0.0

def execute_log(tcam):
    """
    处理之前的log，移动到*/log_backup/中
    """
    ip.type_commands("rm -rf /data/bgm_log_*;mkdir /log/log_backup;mkdir /log/log_presssure;mv /log/jetlog* /log/log_backup/")
    tcam.type_commands("rm -rf /mnt/sdcard/tcam_log_*;mkdir /mnt/sdcard/log_backup;mv /mnt/sdcard/log/jetlog* /mnt/sdcard/log_backup/")


@allure.feature("性能稳定性")
@allure.story("业务性能/服务启动和可用&BGM重启压测")
@pytest.mark.soa
class TestPerformanceConnTime(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        global ip
        ip = self.bgmcli
        self.tcam = TCAM_SSH()
        # 先处理日志
        execute_log(self.tcam)
        self.nucapp.tcam_power_off()
        time.sleep(30)
        self.nucapp.tcam_power_on()
        time.sleep(4*60)
        # 开启诊断
        self.sd_tester.tester_present()
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
        self.max_ServiceRun_end_con_time = {key: (0, 0) for key in remote_control_services.keys()}
        self.ServiceRun_end_max = {key: ("", 0) for key in range(1,test_times+1)}
        self.db_time = []
        self.S2S_resume_time = []

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
      
    def after_each_func(self, ecu):
        #case执行校验最近的一份日志的consume时间
        log_list = get_lastest_log("bts", 1)
        from datetime import datetime
        formatted_date = datetime.now().strftime("%Y-%m-%d")
        data = ''
        for log in log_list:
            data += self.bgmcli.type_commands(f"/app/bin/zstdcat /log/{log}|grep ' W BTS'|grep eid:|grep consume", timeout=60)
        if data:
            logger.error("===============================================================================================================================")
            for i in data.split('\n'):
                try:
                    data1 = i.split(' ')[9]
                    data2 = i.split(' ')[10].split(',')[0][:-2]
                    if data1 == 'consume' and int(data2) > 1200:
                        if f'{formatted_date} ' in i:
                            logger.error(f"{i}, 时间同步后阶段日志校验出现异常日志consume大于1200ms")
                        elif "2021-01-01 08:00" in i:
                            logger.error(f"{i}, 重启阶段日志校验出现异常日志consume大于1200ms")
                        else:
                            logger.error(f"{i}, 其他情况日志校验出现异常日志consume大于1200ms")
                except IndexError as err:
                    logger.error(f"{err}")
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.sd_tester.stop_tester_present()
        logger.info("="*50 + "读取数据库时间,0.0代表没有查到" + "="*50)
        for i in range(test_times):
            logger.info(f"第{i+1}次压测读取数据库耗时为{self.db_time[i]}")
        logger.info("="*50 + "SetDataServiceReady" + "="*50)
        for i in range(test_times):
            logger.info(f"第{i+1}次压测SetDataServiceReady为{self.S2S_resume_time[i]}ms")
        logger.info("="*50 + "域外进程连接最大连接耗时时间" + "="*50)
        for key in self.max_connect_time:
            ser_conn_times = self.max_connect_time[key]
            logger.info(f"最大连接耗时出现在第{ser_conn_times[0]}次，时间为{ser_conn_times[1]} ---- {key}")
        logger.info("="*50 + "SetDataServiceReady最大耗时时间" + "="*50)
        for key in self.max_ServiceRun_end_con_time:
            run_end_times = self.max_ServiceRun_end_con_time[key]
            logger.info(f"SetDataServiceReady最大耗时出现在第{run_end_times[0]}次，时间为{run_end_times[1]} ---- {key}")
        logger.info("="*50 + "每轮压测SetDataServiceReady最大耗时" + "="*50)
        avg = 0.0
        for key in range(1, test_times+1):
            run_time = self.ServiceRun_end_max[key]
            logger.info(f"第{key}次压测SetDataServiceReady最大耗时出现在{run_time[0]}服务，时间为{run_time[1]}s")
            avg += run_time[1]
        logger.info("="*50 + "每轮压测SetDataServiceReady最大耗时平均值" + "="*50)
        logger.info(f"{test_times}次压测SetDataServiceReady最大耗时平均值为{avg/test_times}")
        # 校验jetlog_message日志是否有Error
        check_bgm("s2s_fw.json")
        self.bgmcli.type_commands("mv /log/log_backup/* /log/")
        self.tcam.type_commands("mv /mnt/sdcard/log_backup/* /mnt/sdcard/log/")
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
    def test01_caseid_1892959_1980174(self, request):
        number = int(request.node.name.split('[')[1].split('-')[0])
        for key in remote_control_services.keys():
            self.connect_process_num[key].append([])
        #上下电解析日志
        self.sd_reboot_bgm()
        tmp_partners = [key for key in remote_control_services.keys()]
        logger.info("BGM上电")
        time.sleep(50)
        # 触发信号30s内持续跳变
        t = time.time()
        while time.time() - t <= 30:
            for i in range(2):
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScButtonMidRi1', i)
                self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', i)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', i)
                self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', i)
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', i)
                self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', i)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', i)
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', i)  
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr11, 'BookChargeSetResponse', i)
                self.ipdu.set(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmi', i)
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEMobDevSts', i)
                self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvBattUDc800', i)
                self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', i)
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmBsrmConnectivityFr03, 'ChrgrPileInfo', i)
                self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr01, 'BattIRaw', i)
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScRightButtonRi', i)
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', i)
                sleep(0.2)
        time.sleep(10) # bgm重启后90s等待swap off完成
        DB_time = get_read_storage_time(5)
        self.db_time.append(DB_time)
        resume_time = check_S2SService_Resume_time()
        self.S2S_resume_time.append(resume_time)
        reboot_time = get_reboot_to_snapshot_time()
        hibernation_exit_time = get_hibernation_exit_time()
        #解析服务连接时间
        while tmp_partners:
            for k,w in remote_control_services.items():
                #ServiceRun_end时间ServiceRun_end_time
                SetDataServiceReady_time = get_SetDataServiceReady_time(k)
                if SetDataServiceReady_time:
                    ServiceRun_end_time = round(reboot_time + SetDataServiceReady_time, 3)
                    self.ServiceRun_end_con_time[k].append(ServiceRun_end_time)
                #获取每轮压测的最大ServiceRun_end时间和服务
                if self.ServiceRun_end_max[number][1] < ServiceRun_end_time:
                    self.ServiceRun_end_max[number] = (k, ServiceRun_end_time)
                #获取每个服务的最大ServiceRun_end时间
                if self.max_ServiceRun_end_con_time[k][1] < ServiceRun_end_time:
                    self.max_ServiceRun_end_con_time[k] = (number, ServiceRun_end_time)
                #域外进程连接时间_process_time
                for process in w:
                    if process == "vehicle_data_mi":
                        # vehicle_data_mi进程在bgm和tcam端都有，所以需要特殊处理
                        tcam_pid = self.tcam.type_commands("ps -ef|grep vehicle_data_mi|grep -v grep|awk '{print $1}'").strip()
                        if tcam_pid:
                            conn_sucess_time = get_server_conn_sucess_time(k+":"+tcam_pid, process)
                            _process_time = round(conn_sucess_time - hibernation_exit_time, 3)
                    else:
                        conn_sucess_time = get_server_conn_sucess_time(k, process)
                        _process_time = round(conn_sucess_time - hibernation_exit_time, 3)
                    if _process_time:
                        self.connect_process_num[k][number].append(_process_time)
                        logger.info(f"服务{k}的Run end时间为:{ServiceRun_end_time},连接进程{process}的时间为{_process_time}")
                        con_time = round(reboot_time + _process_time, 3)
                        self.connect_times[k].append(con_time)
                        if self.max_connect_time[k][1] < con_time:
                            self.max_connect_time[k] = (number, con_time)
                    
                logger.info(f"第{number}次压测服务连接所有域外进程的时间为: {self.connect_times[k]}")
                tmp_partners.remove(k)
                logger.info(f"第{number}次压测BGM重启到服务ServiceRun end的时间为: {self.ServiceRun_end_con_time[k]}")
                
        logger.info("="*50 + "服务连接进程数" + "="*50)
        for k in remote_control_services.keys():
            logger.info(f"第{number}次压测服务连接进程数为{len(self.connect_process_num[k][number])} ---- {k}")
            logger.info(self.connect_process_num[k])
            # 校验每次测试的进程连接数是否一致
            if number >= 2:
                if len(self.connect_process_num[k][number]) != len(self.connect_process_num[k][number-1]):
                    assert False,f"第{number}次压测服务{k}连接的进程数与之前不一致"
            
        logger.info("="*50 + "服务可用时间" + "="*50)
        for k in remote_control_services.keys():
            ServiceRun_end_con_mean_time = {}
            if len(self.connect_times[k]) != 0:
                self.connect_mean_time[k] =  round(statistics.mean(self.connect_times[k]), 3)
                if len(self.ServiceRun_end_con_time[k]) != 0:
                    ServiceRun_end_con_mean_time[k] = round(statistics.mean(self.ServiceRun_end_con_time[k]), 3)
                    logger.info(f"第{number}次压测服务ServiceRun_end/服务连接的平均耗时为{ServiceRun_end_con_mean_time[k]}/{self.connect_mean_time[k]} ---- {k}")
                else:
                    logger.info(f"第{number}次压测服务ServiceRun_end/服务连接的平均耗时为None/{self.connect_mean_time[k]} ---- {k}")
            else:
                if len(self.ServiceRun_end_con_time[k]) != 0:
                    ServiceRun_end_con_mean_time[k] = round(statistics.mean(self.ServiceRun_end_con_time[k]), 3)
                    logger.info(f"第{number}次压测服务ServiceRun_end/出现服务未连接情况为{ServiceRun_end_con_mean_time[k]}/None  ---- {k}")                
                else:
                    logger.info(f"第{number}次压测服务ServiceRun_end/出现服务未连接情况为None/None  ---- {k}")
        #assert False
        # 备份BGM日志到/data下，TCAM日志到/mnt/sdcard下
        if test_times>=5 and number%5 == 0:
            # self.bgmcli.type_commands(f"tar -zcvf /data/bgm_log_{self.s_timestamp()}_{test_times}times_{self.num}.tar.gz /log/jetlog* &", timeout=3*60)
            # self.bgmcli.type_commands("\x03")
            self.bgmcli.type_commands("mv /log/jetlog* /log/log_presssure/", timeout=10)
        if test_times == number:
            self.tcam.type_commands(f"tar -zcvf /mnt/sdcard/tcam_log_{self.s_timestamp()}.tar.gz /mnt/sdcard/log/jetlog* &\\n") 
            self.bgmcli.type_commands(f"tar -zcvf /data/bgm_log_{self.s_timestamp()}_{test_times}times.tar.gz /log/log_presssure/jetlog*;rm /log/log_presssure/* &", timeout=3*60)
            
        time.sleep(2)



default_ccp_list = DataTypeHanding.hexstr_to_inlist(
    "A3018006FD030101A302090304020102858B06010004050203000001048C800C0101010102010202010216010701010100030102028089020301010302736E03010101010101010302020202020A010103820201010102020103010201800202020201800000008182118003010103020102020302800102010102010104010101010101010203010103020101830201020201012902010402038002820103040128030A800104010201020203820402810101020101130301010101010205020101000302020304020202010101020001010101010101010180030A0101040607070A0A07070A0A00000400000201010101010280030301020000000202020102020200010102000000010300000100008100000000000000000000000000000080000000000000000000000100010100000200000080000000008403010100000000020100000000000000000002018001020101010101020103020180018002020101010101050380020601030110000002030100000000000000000000000000000000000000000000000000000002000000000001010301000000000200000000000000000000000000000000000000000000000000010201000000000085040102020201020202040301020201028004030101020201030101010202020101020101010101030000000180020201010202010202020102010302020101010101010101000103010201010502020204010101010301010402010201010101020101010101010100000000000001020301010109030101010202020101030104010401010101010201030105020001010101010101010101010101010101010101010101010202010101010102010101010201000001010401000000010100000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001030202080100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001010201020102020101020101010101010201010201010101010202010201010101020202020202010202010202010201010101020101010102010101000102010101000101010101020202010101020201010101010102020102010101010101010001010101010101020101010101020101010101010101010101010101010101010101020201020101010101010100000101010101010101020101010101010101010202000101010101010202020101010100000000000000000000000000000000000000000000000000000000000000000000020202020202020101010101010101020101010101010202020202010002020101020102020201020001")
event_times = 20


@allure.feature("性能稳定性")
@allure.story("业务性能/服务启动和可用&BGM重启压测")
@pytest.mark.soa
class TestPerformanceToEvent(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # 开启诊断
        self.sd_tester.tester_present()
        self.partner = S2sBaseClass([("CarConfigService", "client"),
                                     ("DoorService","client"),
                                     ("KeyService", "client"),
                                     ("HighVoltageService","client"),
                                     ("ClimateControlService", "client"),
                                     ("TailGateService", "client")
                                     ])
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.event_time = []

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.tc_vin_list = self.write_vin(self.tc_config['vin'])
        self.write_ccp()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.empty_dk_data_queue()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.partner.empty_all(5)
      
    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        self.partner.empty_all()
        self.sd_tester.stop_tester_present()
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        for i in range(event_times):
            logger.info(f"第{i+1}次压测bgm重启后event上报耗时为:{self.event_time[i]}")
        super().after_class(self, ecu)

    def write_vin(self, vin_str):
        """写入vin码"""
        self.sd_tester.enter_extended_session()
        self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 1003 to get result")
        self.sd_tester.security_access_level_l3()
        self.sd_tester.write_vin(vin_str)
        self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 2EF190 to get result")
        return list(bytes(vin_str, encoding="ascii"))

    def write_ccp(self, ccp_list=default_ccp_list):
        self.sd_tester.write_multi_ccp({index + 1: ccp_list[index] for index in range(1556)})

    def all_door_open_close(self,swith):
        """
        @param swith: 表示四门open=0 or close=1
        """
        for door in ["drvr","pass","lere","rire"]:
            if swith == 0:
                (eval(f"self.io.{door}_door_open() "))
            else:
                (eval(f"self.io.{door}_door_close() "))

    @pytest.mark.smoke
    @pytest.mark.repeat(event_times)
    @allure.title("启动场景event上报时间校验")
    def test_caseid_1984902(self, request):
        number = int(request.node.name.split('[')[1].split('-')[0])
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorOpenerRiReSts", 4)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiReAntiPnch", 1)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TrOpenPosn', 0)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, 'TrRelsFailtoHMI', 0)
        # 当参数state的值有变化时，S2S会通过HVBatteryFaultValidity(BoolValidity state)通知给订阅方
        # HybErrIndcnReqTelltlBattTracCutOff=1 or HybErrIndcnReqTelltlBattTracFailr=1
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr19, 'HybErrIndcnReqTelltlBattTracCutOff', 1)
        # self.dk.set_cenlock_sts(3)
        self.dk.send_nfc_cmd()
        self.io.trunk_door_close()
        time.sleep(2)
        self.nucapp.bgm_power_off()
        sleep(3)
        self.nucapp.bgm_power_on()
        t1 = time.time()
        self.partner.wait_for_service_reconnect(CARCONFIG_SERVICE_CLIENT)

        # 通知VIN码event上报
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN", {"vin": {"vin": self.tc_vin_list}}, fuzz_match=False)
        # 通知右后电动门开关状态event上报
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorSts", {"sts":{"isAntiPinch": True}})
        # 通知数字钥匙连接信息event上报
        curr_status = [{"keyId": key_id0,
                        "type": 0, "isConnected": False, "zone": 0,
                        "battWarnSts": False}]
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyConnectedStatus", {"status": curr_status})
        # 通知高压电池故障状态event上报
        self.partner.ck_s2s_event(HIGHVOLTAGE_SERVICE_CLIENT, "HVBatteryFaultValidity", {"state": {"value": True, "validity": 0}})
        # 通知远程空调开启关闭状态event上报
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT,"RemotePowerStatus", {"status": 0})
        # 通知尾门的开启状态信息event上报
        self.partner.ck_s2s_event(TAILGATE_SERVICE_CLIENT, "TailGateOpenStatusInfo", {"info": {"position": 0, "angle": 0, "sts": 2}})
        # 所有event上报后的时间计算
        event_time = time.time() - t1
        logger.info(f"第{number}次压测bgm重启后event上报耗时为:{event_time}")
        self.event_time.append(event_time)


if __name__ == '__main__':
    pytest.main()
