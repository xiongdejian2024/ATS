#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_ConfigMasterService.py
@Time: 2024/02/23 11:00
@Author: lei.tao
@Description: Test SOA service about ConfigMaster
"""
import os,sys
import allure
import pytest
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding,int_to_4_bytes_list
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.api.config_center.configfile_utils import *
from xat_ecu.legacy.sdk.tcp_framework.tcp_communicate import *
from xat_ecu.legacy.driver.ssh_interface import command_send
CONFIGMASTER_SERVICE_CLIENT = "ConfigMasterService_client"


@allure.feature("SOA服务接口")
@allure.story("互联服务/ConfigMasterService")
@pytest.mark.tcam
@pytest.mark.full
class TestConfigMasterService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.tcam = TCAM_SSH()
        # 开启tcam的v2t模拟器
        self.bgmcli.type_commands("rm -rf /data/persistent/config_*;rm -rf /data/config_service/rvs/*;shutdown -r")
        self.tcam.type_commands("mv /mnt/sdcard/jiduEM.sh /oemdata/bin/ ;reboot")
        time.sleep(280)
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        # 启动partner operator
        self.partner = S2sBaseClass([("ConfigMasterService", "client")])
        self.partner.method_default_timeout = 0.1

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)

    def after_each_func(self, ecu):
        self.socket.tcp_client.close()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.partner.stop_operators()
        # 恢复tcam环境
        while True:
            self.tcam.type_commands("mv /oemdata/bin/jiduEM.sh /mnt/sdcard/")
            data = self.tcam.type_commands("ls /oemdata/bin/")
            if "jiduEM.sh" not in data:
                logger.info("配置文件清除成功")
                self.tcam.type_commands("reboot")
                break
            else:
                time.sleep(2)
                logger.info("等待清除配置文件")
        time.sleep(180)
        super().after_class(self, ecu)

    def v2t_simulator_Configuration(self, domain, appname):
        pb_ver = "V1"
        name = "MarsOne"
        year = "2024"
        # domain = "TCAM"
        # appname = "rvc"
        confname = "key_value_tab_config"
        action = 0
        conftype = 0
        pushtype = 1
        SyncStrategy = 3

        with open(os.path.join(project_root, f"test_case/soa/case_helper/ConfigCenter/{appname}.json"), "r", encoding='utf8') as fd:
            value = str.encode(fd.read().replace('\n', '').replace(' ', ''))
            logger.info(value)

        # 模拟云端下发配置文件
        cmd = ConfigMasterV2TCmd(pb_ver,name,year,domain,appname,confname,action,conftype,pushtype,SyncStrategy,value,True)
        payload = cmd.return_v2t_cmd_bytes()
        logger.info(f"发送的master数据指令{payload}")
        logger.info(f"master字节长度{len(payload)/2}")
        cloudcmd = VehicleCloudCmd(pb_bytes=DataTypeHanding.to_bytes(payload))
        cloud_payload = cloudcmd.return_cmd_bytes()
        logger.info(f"发送的车云数据指令{cloud_payload}")
        logger.info(f"云端v2t指令字节长度{len(cloud_payload)/2}")
        ck_data = DataTypeHanding.hexstr_to_inlist("12345678") + int_to_4_bytes_list(int(len(cloud_payload)/2)) + DataTypeHanding.hexstr_to_inlist(cloud_payload)
        cloud_cmd = DataTypeHanding.intlist_to_hexstr(ck_data)
        logger.info(f"发送的数据{cloud_cmd}")
        logger.info(f"组包后新字节长度{len(cloud_cmd)/2}")
        logger.info(f"转换后的字节数组{ck_data}")
        self.socket.send_data_to_server(ck_data)
        self.socket.listen_data_from_server()
        time.sleep(10)
        revc_data = self.socket.received_data
        while True:
            if "12345678" == revc_data[:8]:
                logger.info(f"接收到的字节串{revc_data}")
                logger.info(revc_data[8:16])
                data_len = DataTypeHanding.to_int(DataTypeHanding.hexstr_to_inlist(revc_data[8:16]))
                data = revc_data[16:(16+data_len*2)]
                logger.info(f"接收的data为{data}")
                report_data = VehicleCloudInvoke()
                report_data.ParseFromString(DataTypeHanding.to_bytes(data))
                logger.info(f"接收到云端的header信息{report_data.header}")
                logger.info(f"接收到云端的body信息{report_data.body}")
                interface = report_data.header.reqTarget.api

                if "checkConfigVersion" in interface:
                    resp_data = NotifyData()
                    resp_data.ParseFromString(DataTypeHanding.to_bytes(DataTypeHanding.to_hexstr(report_data.body)))
                    logger.info(f'车端主动上报的应用信息{resp_data.Detail}')
                    for i in resp_data.Detail:
                        if domain == i.Domain and appname == i.AppName:
                            for j in i.StatusData:
                                if j.StageType == "RT_MASTER_RECEIVED":
                                    assert j.StatusType == 'ST_SUCCESS'
                                elif j.StageType == "RT_CONFIG_SERVER_RECEIVED":
                                    assert j.StatusType == 'ST_SUCCESS'

                elif "configStatusReport" in interface:
                    resp_data = ConfigStatusReport()
                    resp_data.ParseFromString(DataTypeHanding.to_bytes(DataTypeHanding.to_hexstr(report_data.body)))
                    logger.info(f'车端接收到配置后上报的信息{resp_data}')
                    for i in resp_data.Data:
                        if domain == i.Domain and appname == i.AppName:
                            for j in i.StatusData:
                                if j.StageType == "RT_MASTER_RECEIVED":
                                    assert j.StatusType == 'ST_SUCCESS'
                                elif j.StageType == "RT_CONFIG_SERVER_RECEIVED":
                                    assert j.StatusMessage == 'ok'
                                    assert j.StatusType == 'ST_SUCCESS'

                elif "syncServiceEvent" in interface:
                    event = ServiceEventReq()
                    event.ParseFromString(DataTypeHanding.to_bytes(DataTypeHanding.to_hexstr(report_data.body)))
                    logger.info(f'接收到车端的event信息{event.events}')

                elif "TspAppConfigSet" in interface:
                    resp = ConfSyncDataResp()
                    resp.ParseFromString(DataTypeHanding.to_bytes(DataTypeHanding.to_hexstr(report_data.body)))
                    logger.info(f'接收到车端的响应信息{resp.Details}')
                    for i in resp.Details:
                        assert i.Status == 1
                        assert i.StatusMessage == "success"
                revc_data = revc_data[(16+data_len*2):]
            else:
                break
        self.partner.ck_s2s_event(CONFIGMASTER_SERVICE_CLIENT, "ConfigDataNotify", {"ecuName": domain,"info": {"ecuName": domain}})
        time.sleep(10)

    @pytest.mark.smoke
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    @allure.title("通知bgm域ConfigServer端的appName: rvs配置文件变更")
    def test_caseid_1985472(self):
        self.v2t_simulator_Configuration("BGM", "rvs")

    @pytest.mark.sanity
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    @allure.title("通知tcam域ConfigServer端的appName: rvc配置文件变更")
    def test_caseid_1985475(self):
        self.v2t_simulator_Configuration("TCAM", "rvc")

    @allure.title("通知cdc域ConfigServer端的appName: cdc_log_config配置文件变更")
    def test_caseid_1985473(self):
        self.v2t_simulator_Configuration("CDC", "cdc_log_config")

    @allure.title("通知acu域ConfigServer端的appName: log_upload_acu配置文件变更")
    def test_caseid_1985474(self):
        self.v2t_simulator_Configuration("ACU", "log_upload_acu")

    @allure.title("通知acu域ConfigServer端的appName: aeb_fusion_shadow配置文件变更")
    def test_caseid_1987655(self):
        """
        遗漏复盘，应用：影子模式，检测server端是否可以一直收到指令
        """
        self.v2t_simulator_Configuration("ACU", "aeb_fusion_shadow")

    @allure.title("获取App配置文件内容")
    def test_caseid_1984705(self):
        logger.info("获取存在应用gb32960的信息")
        self.partner.send_request_and_ck_resp(CONFIGMASTER_SERVICE_CLIENT, "GetAppConfig", {"ecuName": "TCAM", "appName":"rvc"}, {"out":{"ecuName": "TCAM", "fileInfoList":[{"appName":"rvc","configFileName":"key_value_tab_config","action":0,"fileType":"Json","pushType":1,"strategy":3}]}})
        logger.info("获取不存在应用cdd的信息")
        self.partner.send_request_and_ck_resp(CONFIGMASTER_SERVICE_CLIENT, "GetAppConfig", {"ecuName": "TCAM", "appName":"cdd"}, {"out":{"ecuName": "TCAM", "fileInfoList":[]}})
    
    @allure.title("获取App配置版本号列表")
    def test_caseid_1984706(self):                                                                
        self.partner.send_request_and_ck_resp(CONFIGMASTER_SERVICE_CLIENT, "GetEcuAppsVersion", {"ecuName": "TCAM"}, {"out":{"isEmpty":False,"ecuName":"TCAM","appVersionList":[{"appName":"rvc","configFileName":"key_value_tab_config"}]}})
        # self.partner.send_request_and_return_resp(CONFIGMASTER_SERVICE_CLIENT, "AllConfigsClearNotify", {"action": True})
        # self.partner.send_request_and_ck_resp(CONFIGMASTER_SERVICE_CLIENT, "GetEcuAppsVersion", {"ecuName": "TCAM"}, {"out":{"isEmpty":False,"ecuName":"TCAM","appVersionList":[{"appName":"rvc","configFileName":"key_value_tab_config"}]}})

    @allure.title("模拟云端下发bgm端配置文件查看返回状态(成功)")
    def test_caseid_1984717(self):
        self.partner.send_request_and_ck_resp(CONFIGMASTER_SERVICE_CLIENT, "SendConfigStatusToTsp", {"info": {"configReportDataList":[{"ecuName":"BGM","appName":"bootesdataconnect","configFileName":"soa.config","reportData":[{"reportType":4,"statusType":1025,"statusMessage":"kAppApply","appIndex":0}]}]}}, {"out":True})
        self.partner.send_request_and_ck_resp(CONFIGMASTER_SERVICE_CLIENT, "SendConfigStatusToTsp", {"info": {"configReportDataList":[{"ecuName":"BGM","appName":"rvs","configFileName":"key_value_tab_config","reportData":[{"reportType":2,"statusType":642,"statusMessage":"ok","appIndex":0}]}]}}, {"out":True})

    @allure.title("模拟云端下发tcam端配置文件查看返回状态(成功)")
    def test_caseid_1984771(self):
        self.partner.send_request_and_ck_resp(CONFIGMASTER_SERVICE_CLIENT, "SendConfigStatusToTsp", {"info": {"configReportDataList":[{"ecuName":"TCAM","appName":"gb32960","configFileName":"key_value_tab_config","reportData":[{"reportType":4,"statusType":1025,"statusMessage":"kAppApply","appIndex":0}]}]}}, {"out":True})
        self.partner.send_request_and_ck_resp(CONFIGMASTER_SERVICE_CLIENT, "SendConfigStatusToTsp", {"info": {"configReportDataList":[{"ecuName":"TCAM","appName":"rvc","configFileName":"key_value_tab_config","reportData":[{"reportType":2,"statusType":642,"statusMessage":"ok","appIndex":0}]}]}}, {"out":True})

    @allure.title("模拟云端下发cdc端配置文件查看返回状态(成功)")
    def test_caseid_1984772(self):
        self.partner.send_request_and_ck_resp(CONFIGMASTER_SERVICE_CLIENT, "SendConfigStatusToTsp", {"info": {"configReportDataList":[{"ecuName":"CDC","appName":"cdc_log_config","configFileName":"key_value_tab_config","reportData":[{"reportType":2,"statusType":642,"statusMessage":"ok","appIndex":0}]}]}}, {"out":True})

    @allure.title("模拟云端下发acu端配置文件查看返回状态(成功)")
    def test_caseid_1984773(self):
        self.partner.send_request_and_ck_resp(CONFIGMASTER_SERVICE_CLIENT, "SendConfigStatusToTsp", {"info": {"configReportDataList":[{"ecuName":"ACU","appName":"cdc_log_config","configFileName":"key_value_tab_config","reportData":[{"reportType":2,"statusType":642,"statusMessage":"ok","appIndex":0}]}]}}, {"out":True})
