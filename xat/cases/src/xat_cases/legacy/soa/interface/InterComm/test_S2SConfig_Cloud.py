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
import socket
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding,int_to_4_bytes_list
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.api.config_center.configfile_utils import *
from xat_ecu.legacy.sdk.tcp_framework.tcp_communicate import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_cases.legacy.soa.interface.Infrastructure.test_CarConfigService import return_EnergyConsumptionData


def _convert_to_double_quotes(data):
    if isinstance(data, dict):
        return {_convert_to_double_quotes(key): _convert_to_double_quotes(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [_convert_to_double_quotes(item) for item in data]
    elif isinstance(data, str):
        return data.replace("'", '"')
    else:
        return data

def modify_json_data(file, key=None, Version=None, ConfigData=None, default_data=True):
    """
    修改json文件中的内容，并返回新的json数据
    Args:
        file: 需要修改的json文件名称
        key: 需要修改的key值
        Version: 需要修改的版本号
        ConfigData: 需要修改的配置数据
        default_data: 是否使用默认的配置数据
    """
    try:
        with open(os.path.join(project_root, f"test_case/soa/case_helper/ConfigCenter/{file}.json"), "r", encoding='utf8') as fd:
            data = json.load(fd)
            logger.info(f"读取的json数据为{data}, 类型是{type(data)}")
            if ConfigData:
                    if key:
                        for k_s,v_s in data[0]["S2SConfigData"].items():
                            if k_s == key:
                                if default_data:
                                    for k,v in ConfigData.items():
                                        if k in data[0]['S2SConfigData'][key].keys():
                                            data[0]['S2SConfigData'][key][k] = v
                                        else:
                                            data[0]['S2SConfigData'][key].update({k:v})
                                else:
                                    data[0]['S2SConfigData'] = {key:ConfigData}
                    else:
                        if default_data:
                            for k,v in ConfigData.items():
                                if k in data[0]['S2SConfigData'].keys():
                                    data[0]['S2SConfigData'][k] = v
                                else:
                                    data[0]['S2SConfigData'].update({k:v})
                        else:
                            data[0]['S2SConfigData'] = ConfigData
            if Version:
                data[0]['S2SConfigVersion'] = Version

            json_data = json.dumps(data, indent=4, ensure_ascii=False)
            
            logger.info(f"修改后的值{json_data}")
            return str(json_data).encode('utf-8')
        
    except FileNotFoundError:
        logger.error(f"文件{file}未找到。")
    except json.JSONDecodeError:
        logger.error(f"文件{file}内容不是有效的JSON格式。")
    except Exception as e:
        logger.error(f"处理JSON数据时发生错误：{e}")


def v2t_simulator_Configuration(socket, file, value, domain="BGM", s2sconfigver_error=False, parameter_error=False):
        pb_ver = "V1"
        name = "MarsOne"
        year = "2024"
        # domain = "TCAM"
        appname = "S2SConfig_" + file
        confname = file
        action = 0
        conftype = 0
        pushtype = 1
        SyncStrategy = 3     
        global Publishid_now
        Publishid_now += 1
        logger.info(f"当前publish_id={Publishid_now}")
        # 模拟云端下发配置文件
        cmd = ConfigMasterV2TCmd(pb_ver,name,year,domain,appname,confname,action,conftype,pushtype,SyncStrategy,value,True, Publishid_now)
        payload = cmd.return_v2t_cmd_bytes()
        logger.info(f"发送的master数据指令{payload}")
        logger.info(f"master字节长度{len(payload)/2}")
        cloudcmd = VehicleCloudCmd(pb_bytes=DataTypeHanding.to_bytes(payload))
        cloud_payload = cloudcmd.return_cmd_bytes()
        logger.info(f"发送的车云数据指令{cloud_payload}")
        logger.info(f"云端v2t指令字节长度{len(cloud_payload)/2}")
        ck_data = DataTypeHanding.hexstr_to_inlist("12345678") + int_to_4_bytes_list(int(len(cloud_payload)/2)) + DataTypeHanding.hexstr_to_inlist(cloud_payload)
        cloud_cmd = DataTypeHanding.intlist_to_hexstr(ck_data)
        logger.info(f"组包后发送的数据{cloud_cmd}")
        logger.info(f"组包后新字节长度{len(cloud_cmd)/2}")
        logger.info(f"转换后的字节数组{ck_data}")
        socket.send_data_to_server(ck_data)
        socket.listen_data_from_server()
        time.sleep(10)
        revc_data = socket.received_data
        RT_MASTER = RT_CONFIG = RT_APP_CHECK = RT_APPLY = False
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
                                
                elif "configStatusReport" in interface:
                    resp_data = ConfigStatusReport()
                    resp_data.ParseFromString(DataTypeHanding.to_bytes(DataTypeHanding.to_hexstr(report_data.body)))
                    logger.info(f'车端接收到配置后上报的信息{resp_data}')
                    for i in resp_data.Data:
                        if domain == i.Domain and appname == i.AppName:
                            logger.info(f'车端接收到配置后上报的StatusData {i.StatusData}')
                            logger.info(f'车端接收到配置后上报的StageType {i.StatusData[0].StageType}')
                            for j in i.StatusData:
                                if j.StageType == 1 and j.StatusType == 1: # 代表"RT_MASTER_RECEIVED"
                                    RT_MASTER = True
                                elif j.StageType == 2 and j.StatusType == 1: # 代表"RT_CONFIG_SERVER_RECEIVED"
                                    RT_CONFIG = True
                                    # 版本不匹配不会进入app check环节
                                    if s2sconfigver_error: 
                                        assert all([RT_MASTER, RT_CONFIG])
                                        return
                                elif j.StageType == 3: # 代表"RT_APP_CHECK"
                                    # 参数错误app解析失败
                                    if parameter_error: # 代表'ST_APP_PARSED_ERROR'
                                        assert all([RT_MASTER, RT_CONFIG])
                                        return 
                                    if (not parameter_error) and j.StatusType == 1: # 代表'ST_SUCCESS'
                                        RT_APP_CHECK = True
                                elif j.StageType == 4 and j.StatusType == 1: # 代表"RT_APPLY"
                                    RT_APPLY = True

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
        time.sleep(2)
        assert all([RT_MASTER, RT_CONFIG, RT_APP_CHECK, RT_APPLY])


def get_lasest_event_publishId(partner):
    globalvar_publishID = random.getrandbits(60)
    for event in list(partner.partner_infos["ConfigMasterService_client"].event_queue.queue):
        logger.info(f"event={event}")
        if event['function'] == "UpdateConfigDataNotifyEvent":
            raw_data = eval(event['args'])
            logger.info(f"打印当前返回值: UpdateConfigDataNotifyEvent={raw_data}")
            ecuName=raw_data["ecuName"]
            configFileName=raw_data["info"]["fileInfoList"][0]["configFileName"]
            logger.info(f"打印当前返回值: ecuName={ecuName}, configFileName={configFileName}")
            if raw_data["ecuName"].lower() == "bgm":
                publishid=raw_data["info"]["fileInfoList"][0]["publishID"]
                globalvar_publishID=max(int(publishid), globalvar_publishID)
                logger.info(f"打印当前返回值: publishid={publishid}, globalvar_publishID={globalvar_publishID}")
    
    return globalvar_publishID + 1


@allure.feature("SOA服务接口")
@allure.story("内部通信/S2SConfigCloud")
@pytest.mark.full
class TestCarConfigService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.tcam = TCAM_SSH()
        # 启动partner operator
        self.partner = S2sBaseClass([("CarConfigService", "client"),("ConfigMasterService", "client")])
        # 开启tcam的v2t模拟器
        self.bgmcli.type_commands("rm -rf /data/persistent/config_service/* ;rm -rf /data/persistent/config_master/*;rm -rf /data/config_service/S2SConfig_Cloud_CarConfig/*;sleep 5;shutdown -r")
        self.tcam.type_commands("mv /mnt/sdcard/jiduEM.sh /oemdata/bin/ ;reboot")
        time.sleep(280)
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.partner.method_default_timeout = 0.1
        self.file = "Cloud_CarConfig"
        global Publishid_now
        Publishid_now = get_lasest_event_publishId(self.partner)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
        time.sleep(5)         

    def after_each_func(self, ecu):
        self.socket.tcp_client.close()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        try:
            logger.info("恢复ccp和data")
            self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
            value = modify_json_data(self.file)
            v2t_simulator_Configuration(self.socket, self.file, value, s2sconfigver_error=True)
        except Exception as e:
            logger.info(e)
        finally:
            self.partner.stop_operators()
            self.socket.tcp_client.shutdown(socket.SHUT_RDWR)
            self.socket.tcp_client.close()
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
            time.sleep(280)
            super().after_class(self, ecu)


    @allure.title("服务CarConfigService_版本不匹配")
    def test_caseid_1989393(self):
        data = {"batteryCapacityMax":97.68,
        "cltcFullRange":660,
        "cltcEnergyComsumption":14.80,
        "wltpFullRange":557,
        "wltpEnergyComsumption":17.54,
        "epaFullRange": 599,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 128, 566: 16, 950: 1, 966: 0})
        value = modify_json_data(self.file, key="CCP3_128_CCP566_16_CCP950_1_CCP966_0", ConfigData=data, Version="3.0", default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value, s2sconfigver_error=True)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                                {"out": return_EnergyConsumptionData(97.68000030517578, 660, 14.800000190734863, 557, 17.540000915527344, 599, 19.0)})
       
    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围")
    @pytest.mark.smoke
    def test_caseid_1989395(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 128, 566: 16, 950: 1, 966: 0})
        value = modify_json_data(self.file, key="CCP3_128_CCP566_16_CCP950_1_CCP966_0", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})
        
    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在最小值")
    def test_caseid_1989396(self):
        data = {"batteryCapacityMax":0.001,
                "cltcFullRange":1,
                "cltcEnergyComsumption":5.001,
                "wltpFullRange":1,
                "wltpEnergyComsumption":5.001,
                "epaFullRange": 1,
                "epaEnergyComsumption":5.001}
        self.sd_tester.write_multi_ccp({3: 128, 566: 16, 950: 1, 966: 0})
        value = modify_json_data(self.file, key="CCP3_128_CCP566_16_CCP950_1_CCP966_0", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(0.001, 1, 5.001, 1, 5.001, 1, 5.001)})
        
    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在最大值")
    def test_caseid_1989406(self):
        data = {"batteryCapacityMax":299.99,
                "cltcFullRange":998,
                "cltcEnergyComsumption":29.999,
                "wltpFullRange":998,
                "wltpEnergyComsumption":29.999,
                "epaFullRange": 998,
                "epaEnergyComsumption":29.999}
        self.sd_tester.write_multi_ccp({3: 128, 566: 16, 950: 1, 966: 0})
        value = modify_json_data(self.file, key="CCP3_128_CCP566_16_CCP950_1_CCP966_0", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(299.99, 998, 29.999, 998, 29.999, 998, 29.999)})

    @allure.title("服务CarConfigService_版本匹配_参数全部存在_一个或以上参数超范围")
    def test_caseid_1989416(self):
        data = {"batteryCapacityMax":300.1,
                "cltcFullRange":1000,
                "cltcEnergyComsumption":30.1,
                "wltpFullRange":1000,
                "wltpEnergyComsumption":30.1,
                "epaFullRange": 1000,
                "epaEnergyComsumption":30.1}
        self.sd_tester.write_multi_ccp({3: 128, 566: 16, 950: 1, 966: 0})
        value = modify_json_data(self.file, key="CCP3_128_CCP566_16_CCP950_1_CCP966_0", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value, parameter_error=True)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                            {"out": return_EnergyConsumptionData(97.68000030517578, 660, 14.800000190734863, 557, 17.540000915527344, 599, 19.0)})

    @allure.title("服务CarConfigService_版本匹配_参数在有效范围_参数只有一个且正确")
    @pytest.mark.sanity
    def test_caseid_1989408(self):
        data = {"batteryCapacityMax":111.0,
                "cltcFullRange":300,
                "cltcEnergyComsumption":11.1,
                "wltpFullRange":300,
                "wltpEnergyComsumption":11.1,
                "epaFullRange": 300,
                "epaEnergyComsumption":11.111
                }
        self.sd_tester.write_multi_ccp({3: 128, 566: 16, 950: 1, 966: 0})
        value = modify_json_data(self.file, key="CCP3_128_CCP566_16_CCP950_1_CCP966_0", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(111.0, 300, 11.1, 300, 11.1, 300, 11.111)})
        # 写入CCP：CCP3_128_CCP566_16_CCP950_2_CCP966_-
        self.sd_tester.write_multi_ccp({3: 128, 566: 16, 950: 2})
        # 检测CCP：CCP3_128_CCP566_16_CCP950_2_CCP966_-是否为默认值
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {}, 
                                        {"out": return_EnergyConsumptionData(98.70, 770, 12.82, 650, 15.18,599,19.0)})
        value = modify_json_data(self.file, key="CCP3_128_CCP566_16_CCP950_2_CCP966_-", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(111.0, 300, 11.1, 300, 11.1, 300, 11.111)})
        # 再次检测第一次CCP的是否重置为默认值
        self.sd_tester.write_multi_ccp({3: 128, 566: 16, 950: 1, 966: 0})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {}, 
                                        {"out": return_EnergyConsumptionData(97.68, 660, 14.80, 557, 17.54, 599, 19.0)})


    @allure.title("服务CarConfigService_版本匹配_参数在有效范围_一个或以上参数名称有误")
    def test_caseid_1989409(self):
        data = {"batteryCapacityMaxXXX":11.0,
                "cltcFullRangeXXX":998,
                "cltcEnergyComsumptionXXX":29.0,
                "wltpFullRangeXXX":998,
                "wltpEnergyComsumptionXXX":29.9,
                "epaFullRangeXXX": 998,
                "epaEnergyComsumptionXXX":5.001}
        self.sd_tester.write_multi_ccp({3: 128, 566: 16, 950: 1, 966: 0})
        value = modify_json_data(self.file, key="CCP3_128_CCP566_16_CCP950_1_CCP966_0", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value, parameter_error=True)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                            {"out": return_EnergyConsumptionData(97.68000030517578, 660, 14.800000190734863, 557, 17.540000915527344, 599, 19.0)})


    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围_CCP3_128_CCP566_16_CCP950_2_CCP966_-")
    def test_caseid_1989581(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 128, 566: 16, 950: 2})
        value = modify_json_data(self.file, key="CCP3_128_CCP566_16_CCP950_2_CCP966_-", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})

    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围_CCP3_129_CCP566_23_CCP950_1_CCP966_0")
    def test_caseid_1989582(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 129, 566: 23, 950: 1, 966: 0})
        value = modify_json_data(self.file, key="CCP3_129_CCP566_23_CCP950_1_CCP966_0", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})

    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围_CCP3_129_CCP566_23_CCP950_2_CCP966_-")
    def test_caseid_1989583(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 129, 566: 23, 950: 2})
        value = modify_json_data(self.file, key="CCP3_129_CCP566_23_CCP950_2_CCP966_-", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})

    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围_CCP3_129_CCP566_16_CCP950_1_CCP966_0")
    def test_caseid_1989584(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 129, 566: 16, 950: 1, 966: 0})
        value = modify_json_data(self.file, key="CCP3_129_CCP566_16_CCP950_1_CCP966_0", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})

    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围_CCP3_129_CCP566_16_CCP950_2_CCP966_-")
    def test_caseid_1989585(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 129, 566: 16, 950: 2})
        value = modify_json_data(self.file, key="CCP3_129_CCP566_16_CCP950_2_CCP966_-", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})

    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围_CCP3_129_CCP566_24_CCP950_1_CCP966_2")
    def test_caseid_1989586(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 129, 566: 24, 950: 1, 966: 2})
        value = modify_json_data(self.file, key="CCP3_129_CCP566_24_CCP950_1_CCP966_2", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})


    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围_CCP3_128_CCP566_24_CCP950_1_CCP966_2")
    def test_caseid_1989587(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 128, 566: 24, 950: 1, 966: 2})
        value = modify_json_data(self.file, key="CCP3_128_CCP566_24_CCP950_1_CCP966_2", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})

    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围_CCP3_129_CCP566_25_CCP950_1_CCP966_2")
    def test_caseid_1989588(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 129, 566: 25, 950: 1, 966: 2})
        value = modify_json_data(self.file, key="CCP3_129_CCP566_25_CCP950_1_CCP966_2", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})

    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围_CCP3_129_CCP566_24_CCP950_2_CCP966_-")
    def test_caseid_1989589(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 129, 566: 24, 950: 2})
        value = modify_json_data(self.file, key="CCP3_129_CCP566_24_CCP950_2_CCP966_-", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})

    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围_CCP3_128_CCP566_24_CCP950_2_CCP966_-")
    def test_caseid_1989590(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 128, 566: 24, 950: 2})
        value = modify_json_data(self.file, key="CCP3_128_CCP566_24_CCP950_2_CCP966_-", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})

    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围_CCP3_129_CCP566_25_CCP950_2_CCP966_-")
    def test_caseid_1989591(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 129, 566: 25, 950: 2})
        value = modify_json_data(self.file, key="CCP3_129_CCP566_25_CCP950_2_CCP966_-", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})

    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围_CCP3_129_CCP566_16_CCP950_1_CCP966_1")
    def test_caseid_1989593(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 129, 566: 16, 950: 1, 966: 1})
        value = modify_json_data(self.file, key="CCP3_129_CCP566_16_CCP950_1_CCP966_1", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})

    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围_CCP3_128_CCP566_16_CCP950_1_CCP966_1")
    def test_caseid_1989594(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 128, 566: 16, 950: 1, 966: 1})
        value = modify_json_data(self.file, key="CCP3_128_CCP566_16_CCP950_1_CCP966_1", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})

    @allure.title("服务CarConfigService_版本匹配_参数全部存在_参数在有效范围_CCP3_129_CCP566_23_CCP950_1_CCP966_1")
    def test_caseid_1989595(self):
        data = {
        "batteryCapacityMax":299.68,
        "cltcFullRange":880,
        "cltcEnergyComsumption":19.80,
        "wltpFullRange":880,
        "wltpEnergyComsumption":19.54,
        "epaFullRange": 880,
        "epaEnergyComsumption":19.0}
        self.sd_tester.write_multi_ccp({3: 129, 566: 23, 950: 1, 966: 1})
        value = modify_json_data(self.file, key="CCP3_129_CCP566_23_CCP950_1_CCP966_1", ConfigData=data, default_data=False)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(299.68, 880, 19.80, 880, 19.54, 880, 19.0)})


###########################################################################################################################################
@allure.feature("SOA服务接口")
@allure.story("内部通信/S2SConfigCloud ")
@pytest.mark.full
class TestSuspensionService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.tcam = TCAM_SSH()
        # 启动partner operator
        self.partner = S2sBaseClass([("CarConfigService", "client"),("ConfigMasterService", "client")])
        # 开启tcam的v2t模拟器
        self.bgmcli.type_commands("rm -rf /data/persistent/config_service/* ;rm -rf /data/persistent/config_master/*;rm -rf /data/config_service/S2SConfig_Cloud_Suspension/*;sleep 5;shutdown -r")
        self.tcam.type_commands("mv /mnt/sdcard/jiduEM.sh /oemdata/bin/ ;reboot")
        time.sleep(280)
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.partner.method_default_timeout = 0.1
        self.file = "Cloud_Suspension"
        global Publishid_now
        Publishid_now = get_lasest_event_publishId(self.partner)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
        time.sleep(5)         

    def after_each_func(self, ecu):
        self.socket.tcp_client.close()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        try:
            logger.info("恢复ccp和data")
            self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
            value = modify_json_data(self.file)
            v2t_simulator_Configuration(self.socket, self.file, value)
        except Exception as e:
            logger.info(e)
        finally:
            self.partner.stop_operators()
            self.socket.tcp_client.shutdown(socket.SHUT_RDWR)
            self.socket.tcp_client.close()
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
            time.sleep(280)
            super().after_class(self, ecu)

    @allure.title("服务SuspensionService_版本不匹配")
    def test_caseid_1989410(self):
        value = modify_json_data(self.file, Version="4.0.0")
        v2t_simulator_Configuration(self.socket, self.file, value, s2sconfigver_error=True)
       
    @allure.title("服务SuspensionService_版本匹配_参数全部存在_参数在有效范围")
    @pytest.mark.smoke
    def test_caseid_1989411(self):
        data = {"SpeedDurationTime": 100,
                "OverrideDurationFactorTime": 100}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        
    @allure.title("服务SuspensionService_版本匹配_参数全部存在_参数在最小值")
    def test_caseid_1989412(self):
        data = {"SpeedDurationTime": 1,
                "OverrideDurationFactorTime": 1}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)

    @allure.title("服务SuspensionService_版本匹配_参数全部存在_参数在最大值")
    def test_caseid_1989413(self):
        data = {"SpeedDurationTime": 599,
                "OverrideDurationFactorTime": 599}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)

    @allure.title("服务SuspensionService_版本匹配_参数全部存在_一个或以上参数超范围")
    def test_caseid_1989407(self):
        data = {"SpeedDurationTime": 601,
                "OverrideDurationFactorTime": 601}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v})
            v2t_simulator_Configuration(self.socket, self.file, value, parameter_error=True)

    @allure.title("服务SuspensionService_版本匹配_参数在有效范围_参数只有一个且正确")
    @pytest.mark.sanity
    def test_caseid_1989414(self):
        data = {"SpeedDurationTime": 8,
                "OverrideDurationFactorTime": 8}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v}, default_data=False)
            v2t_simulator_Configuration(self.socket, self.file, value)
      
    @allure.title("服务SuspensionService_版本匹配_参数在有效范围_一个或以上参数名称有误")
    def test_caseid_1989415(self):
        data = {"SpeedDurationTimeXXX": 10,
                "OverrideDurationFactorTimeXXX": 10}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v})
            v2t_simulator_Configuration(self.socket, self.file, value, parameter_error=True)


###########################################################################################################################################
@allure.feature("SOA服务接口")
@allure.story("内部通信/S2SConfigCloud ")
@pytest.mark.full
class TestWindowService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.tcam = TCAM_SSH()
        # 启动partner operator
        self.partner = S2sBaseClass([("WindowService", "client"),("ConfigMasterService", "client")])
        # 开启tcam的v2t模拟器
        self.bgmcli.type_commands("rm -rf /data/persistent/config_service/* ;rm -rf /data/persistent/config_master/*;rm -rf /data/config_service/S2SConfig_Cloud_Window/*;sleep 5;shutdown -r")
        self.tcam.type_commands("mv /mnt/sdcard/jiduEM.sh /oemdata/bin/ ;reboot")
        time.sleep(280)
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.partner.method_default_timeout = 0.1
        self.file = "Cloud_Window"
        global Publishid_now
        Publishid_now = get_lasest_event_publishId(self.partner)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
        time.sleep(5)         

    def after_each_func(self, ecu):
        self.socket.tcp_client.close()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        try:
            logger.info("恢复ccp和data")
            self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
            value = modify_json_data(self.file)
            v2t_simulator_Configuration(self.socket, self.file, value)
        except Exception as e:
            logger.info(e)
        finally:
            self.partner.stop_operators()
            self.socket.tcp_client.shutdown(socket.SHUT_RDWR)
            self.socket.tcp_client.close()
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
            time.sleep(280)
            super().after_class(self, ecu)

    def check_window(self, WinMoveStsCheckTime, WinSetPosDelayTime):
        # 校验参数WinMoveStsCheckTime
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 0)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 20)
        # self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT,"GetWindowMoveInfo", {}, {"out":{"frontLeftMoveSts": 0}}, timeout=3, cycle_time=0.1)
        self.partner.send_request_and_ck_resp(WINDOW_SERVICE_CLIENT,"GetWindowMoveInfo", {}, {"out":{"frontLeftMoveSts": 1}}, timeout=WinMoveStsCheckTime+0.5)
        # 校验参数WinSetPosDelayTime
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition", {"windows": [{"id": 4, "position": 20}]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(WinSetPosDelayTime+3)
        self.bgm_eth_inter.ck_signal_values("WinOpenDrvrReq", [0, 6, 6, 6, 0, 0, 6, 6, 6, 0])
        self.bgm_eth_inter.ck_period_time("WinOpenDrvrReq", 0.04, 0.4, permit_fail_times=2)
        signal_items = self.bgm_eth_inter.get_signal_items("WinOpenDrvrReq")
        assert (WinSetPosDelayTime-0.05) <= signal_items[5][1] - signal_items[0][1] <= (WinSetPosDelayTime+0.05)
    
    @allure.title("服务WindowService_版本不匹配")
    def test_caseid_1989417(self):
        value = modify_json_data(self.file, Version="1.0.0")
        v2t_simulator_Configuration(self.socket, self.file, value, s2sconfigver_error=True)
        self.check_window(0.5, 1)
       
    @allure.title("服务WindowService_版本匹配_参数全部存在_参数在有效范围")
    @pytest.mark.smoke
    def test_caseid_1989418(self):
        value = modify_json_data(self.file)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.check_window(0.5, 1)

    @allure.title("服务WindowService_版本匹配_参数全部存在_参数在最小值")
    def test_caseid_1989419(self):
        data = { "WinMoveStsCheckTime" : 100,
                "WinSetPosDelayTime" : 500}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.check_window(0.1, 0.5)

    @allure.title("服务WindowService_版本匹配_参数全部存在_参数在最大值")
    def test_caseid_1989420(self):
        data = { "WinMoveStsCheckTime" : 900,
                "WinSetPosDelayTime" : 2900}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.check_window(0.9, 2.9)

    @allure.title("服务WindowService_版本匹配_参数全部存在_一个或以上参数超范围")
    def test_caseid_1989421(self):
        data = { "WinMoveStsCheckTime" : 1001,
                "WinSetPosDelayTime" : 3001}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v})
            v2t_simulator_Configuration(self.socket, self.file, value, parameter_error=True)
            if k == "WinSetPosDelayTime":
                self.check_window(0.5, 1)

    @allure.title("服务WindowService_版本匹配_参数在有效范围_参数只有一个且正确")
    @pytest.mark.sanity
    def test_caseid_1989422(self):
        data = { "WinMoveStsCheckTime" : 100,
                "WinSetPosDelayTime" : 600}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v}, default_data=False)
            v2t_simulator_Configuration(self.socket, self.file, value)
            if k == "WinSetPosDelayTime":
                self.check_window(0.5, 0.6)
      
    @allure.title("服务WindowService_版本匹配_参数在有效范围_一个或以上参数名称有误")
    def test_caseid_1989423(self):
        data = { "WinMoveStsCheckTimeXXX" : 1,
                "WinSetPosDelayTimeXXX" : 1}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v})
            v2t_simulator_Configuration(self.socket, self.file, value, parameter_error=True)
            if k == "WinSetPosDelayTimeXXX":
                self.check_window(0.5, 1)

###########################################################################################################################################
@allure.feature("SOA服务接口")
@allure.story("内部通信/S2SConfigCloud ")
@pytest.mark.full
class TestClimateControlService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.tcam = TCAM_SSH()
        # 启动partner operator
        self.partner = S2sBaseClass([("ClimateControlService", "client"),("ConfigMasterService", "client")])
        # 开启tcam的v2t模拟器
        self.bgmcli.type_commands("rm -rf /data/persistent/config_service/* ;rm -rf /data/persistent/config_master/*;rm -rf /data/config_service/S2SConfig_Cloud_ClimateControl/*;sleep 5;shutdown -r")
        self.tcam.type_commands("mv /mnt/sdcard/jiduEM.sh /oemdata/bin/ ;reboot")
        time.sleep(280)
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.partner.method_default_timeout = 0.1
        self.file = "Cloud_ClimateControl"
        global Publishid_now
        Publishid_now = get_lasest_event_publishId(self.partner)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
        time.sleep(5)         

    def after_each_func(self, ecu):
        self.socket.tcp_client.close()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        try:
            logger.info("恢复ccp和data")
            self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
            value = modify_json_data(self.file)
            v2t_simulator_Configuration(self.socket, self.file, value)
        except Exception as e:
            logger.info(e)
        finally:
            self.partner.stop_operators()
            self.socket.tcp_client.shutdown(socket.SHUT_RDWR)
            self.socket.tcp_client.close()
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
            time.sleep(280)
            super().after_class(self, ecu)

    def check_Climate(self,CircTrWorkVal, CircTrTimerStartVal, CircTrTimerEndVal, CircTrDuraSecs, FragranceDebounceSecs):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FrntHvacBlowerSts', 1)
        time.sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 2)
        time.sleep(1)
        # 如果进入内循环模式，且ResrvdSigForECM2>=85，需要发送自动循环模式的信号，但仍提供内循环状态
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', CircTrWorkVal)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        time.sleep(2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1)
        # 在此期间（未发生2），如果ResrvdSigForECM2<75, 则起一个10min计时器
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', CircTrTimerStartVal) 
        time.sleep(2)
        # 如果计时10min结束，满足ResrvdSigForECM2<80，则发送内循环模式信号（退出逻辑1）；如果计时期间满足了ResrvdSigForECM2>=80，将计时器清零并在ResrvdSigForECM2<75时重新开始计时10min直至结束（此时未退出逻辑1
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', CircTrTimerEndVal)
        time.sleep(10)
        # 在此期间（未发生2），如果ResrvdSigForECM2<75，则起一个10min计时器
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', CircTrTimerStartVal-1) 
        j = CircTrDuraSecs//100
        if CircTrDuraSecs >= 100:
            for i in range(j):
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1)
                time.sleep(100)
        time.sleep(CircTrDuraSecs%100)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 2)
        # 验证香氛计时器
        self.partner.empty_all(0.5)
        for A in range(1, 6):
            logger.info(f"信号AirFragCh{A}AvlTi发送默认值")
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, f"AirFragCh{A}AvlTi", 0)
        for B in range(1, 6):
            logger.info(f"信号AirFragCh{B}AvlTi发送{180}")
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, f"AirFragCh{B}AvlTi", 180)
        time.sleep(FragranceDebounceSecs-1)
        self.partner.empty_all() # 第一个信号发送之后的倒数第二秒
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[0, 0, 0, 0, 0]}})
        time.sleep(1) # 最后一秒
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180,180,180,180,180]}})

    @allure.title("服务ClimateControlService_版本不匹配")
    def test_caseid_1989424(self):
        value = modify_json_data(self.file, Version=["1.0.0"])
        v2t_simulator_Configuration(self.socket, self.file, value, s2sconfigver_error=True)
        self.check_Climate(85, 75, 80, 600, 7)
       
    @allure.title("服务ClimateControlService_版本匹配_参数全部存在_参数在有效范围")
    @pytest.mark.smoke
    def test_caseid_1989425(self):
        data = {
            "CircTrWorkVal": 88,
            "CircTrTimerStartVal": 60,
            "CircTrTimerEndVal": 70,
            "CircTrDuraSecs": 101,
            "FragranceDebounceSecs": 3
        }
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.check_Climate(88, 60, 70, 101, 3)

    @allure.title("服务ClimateControlService_版本匹配_参数全部存在_参数在最小值")
    def test_caseid_1989426(self):
        data = {"CircTrWorkVal": 10,
                "CircTrTimerStartVal": 2,
                "CircTrTimerEndVal": 5,
                "CircTrDuraSecs": 1,
                "FragranceDebounceSecs": 1}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.check_Climate(10, 2, 5, 1, 1)

    @allure.title("服务ClimateControlService_版本匹配_参数全部存在_参数在最大值")
    def test_caseid_1989427(self):
        data = {"CircTrWorkVal": 99,
                "CircTrTimerStartVal": 90,
                "CircTrTimerEndVal": 95,
                "CircTrDuraSecs": 5999,
                "FragranceDebounceSecs": 19}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.check_Climate(99, 90, 95, 5999, 19)

    @allure.title("服务ClimateControlService_版本匹配_参数全部存在_一个或以上参数超范围")
    def test_caseid_1989428(self):
        data = {"CircTrWorkVal": 101,
                "CircTrTimerStartVal": 101,
                "CircTrTimerEndVal": 101,
                "CircTrDuraSecs": 6001,
                "FragranceDebounceSecs": 21}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v})
            v2t_simulator_Configuration(self.socket, self.file, value, parameter_error=True)

    @allure.title("服务ClimateControlService_版本匹配_参数在有效范围_参数只有一个且正确")
    @pytest.mark.sanity
    def test_caseid_1989429(self):
        data = {"CircTrWorkVal": 83,
                "CircTrTimerStartVal": 30,
                "CircTrTimerEndVal": 77,
                "CircTrDuraSecs": 10,
                "FragranceDebounceSecs": 10}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v}, default_data=False)
            v2t_simulator_Configuration(self.socket, self.file, value)
            if k == "CircTrWorkVal":
                self.check_Climate(83, 75, 80, 600, 7)
            elif k == "CircTrTimerStartVal":
                self.check_Climate(85, 30, 80, 600, 7)
            elif k == "CircTrTimerEndVal":
                self.check_Climate(85, 75, 77, 600, 7)
            elif k == "CircTrDuraSecs":
                self.check_Climate(85, 75, 80, 10, 7)
            elif k == "FragranceDebounceSecs":
                self.check_Climate(85, 75, 80, 600, 10)

    @allure.title("服务ClimateControlService_版本匹配_参数在有效范围_一个或以上参数名称有误")
    def test_caseid_198942(self):
        data = {"CircTrWorkValXXX": 11,
                "CircTrTimerStartValXXX": 11,
                "CircTrTimerEndValXXX": 11,
                "CircTrDuraSecsXXX": 11,
                "FragranceDebounceSecsXXX": 11}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v})
            v2t_simulator_Configuration(self.socket, self.file, value, parameter_error=True)


###########################################################################################################################################
@allure.feature("SOA服务接口")
@allure.story("内部通信/S2SConfigCloud ")
@pytest.mark.full
class TestSeatService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.tcam = TCAM_SSH()
        # 启动partner operator
        self.partner = S2sBaseClass([("SeatService", "client"),("ConfigMasterService", "client")])
        # 开启tcam的v2t模拟器
        self.bgmcli.type_commands("rm -rf /data/persistent/config_service/* ;rm -rf /data/persistent/config_master/*;rm -rf /data/config_service/S2SConfig_Cloud_Seat/*;sleep 5;shutdown -r")
        self.tcam.type_commands("mv /mnt/sdcard/jiduEM.sh /oemdata/bin/ ;reboot")
        time.sleep(280)
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.partner.method_default_timeout = 0.1
        self.file = "Cloud_Seat"
        global Publishid_now
        Publishid_now = get_lasest_event_publishId(self.partner)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
        time.sleep(5)         

    def after_each_func(self, ecu):
        self.socket.tcp_client.close()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        try:
            logger.info("恢复ccp和data")
            self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
            value = modify_json_data(self.file)
            v2t_simulator_Configuration(self.socket, self.file, value)
        except Exception as e:
            logger.info(e)
        finally:
            self.partner.stop_operators()
            self.socket.tcp_client.shutdown(socket.SHUT_RDWR)
            self.socket.tcp_client.close()
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
            time.sleep(280)
            super().after_class(self, ecu)

    def set_four_seat_occupt(self,A,B,C,D):
        ###"""设置副驾 左后 后中 后右 1/2代表占位 0 代表未占位"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', D)
        time.sleep(0.5)
    
    #设置座椅占位，一次有且只有一个占位
    def set_four_seat_occupt_onlyone(self,seatid):
        if seatid == 0:
            self.io.driver_seat_present()
            self.set_four_seat_occupt(0,0,0,0)
        elif seatid == 1:
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(1,0,0,0)
        elif seatid == 2:
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,1,0,0)
        elif seatid == 3:
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,1,0)
        else:
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,1)

    def set_four_Door_open_onlyone(self,doorid):
        if doorid == 0:
            self.set_four_Door_close()
            self.io.drvr_door_open()
        elif doorid == 1:
            self.set_four_Door_close()
            self.io.pass_door_open()
        elif doorid == 2:
            self.set_four_Door_close()
            self.io.lere_door_open()
        elif doorid == 3:
            self.set_four_Door_close()
            self.io.rire_door_open()

    def set_four_Door_close(self):
        self.io.drvr_door_close()
        self.io.pass_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()

    def check_Seat(self, UserInVehicleDebTimeSecs):
        # 修改配置后功能验证
        self.io.driver_seat_present()
        self.set_four_seat_occupt_onlyone(0)
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                            {"personSts":{"userInVehicleStatus":True}},
                            "GetVehicleInsidePersonSts", {})
        self.set_four_Door_open_onlyone(0)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.ck_coming_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                            {"personSts":{"userInVehicleStatus":False}}, "GetVehicleInsidePersonSts", {},timeout=UserInVehicleDebTimeSecs,deviation=0.999)

    @allure.title("服务SeatService_版本不匹配")
    def test_caseid_1989431(self):
        value = modify_json_data(self.file, Version="3.0.1")
        v2t_simulator_Configuration(self.socket, self.file, value, s2sconfigver_error=True)
        self.check_Seat(3)
       
    @allure.title("服务SeatService_版本匹配_参数全部存在_参数在有效范围")
    @pytest.mark.smoke
    def test_caseid_1989432(self):
        data = {"UserInVehicleDebTimeSecs": 6}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.check_Seat(6)
        

    @allure.title("服务SeatService_版本匹配_参数全部存在_参数在最小值")
    def test_caseid_1989433(self):
        data = {"UserInVehicleDebTimeSecs": 1}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.check_Seat(1)

    @allure.title("服务SeatService_版本匹配_参数全部存在_参数在最大值")
    def test_caseid_1989434(self):
        data = {"UserInVehicleDebTimeSecs": 9}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.check_Seat(9)

    @allure.title("服务SeatService_版本匹配_参数全部存在_一个或以上参数超范围")
    def test_caseid_1989435(self):
        data = {"UserInVehicleDebTimeSecs": 11}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v})
            v2t_simulator_Configuration(self.socket, self.file, value, parameter_error=True)
            
            self.check_Seat(3)

    @allure.title("服务SeatService_版本匹配_参数在有效范围_参数只有一个且正确")
    @pytest.mark.sanity
    def test_caseid_1989436(self):
        data = {"UserInVehicleDebTimeSecs": 6}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v}, default_data=False)
            v2t_simulator_Configuration(self.socket, self.file, value)
            
            self.check_Seat(6)

    @allure.title("服务SeatService_版本匹配_参数在有效范围_一个或以上参数名称有误")
    def test_caseid_1989437(self):
        data = {"UserInVehicleDebTimeSecsXXX": 2}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v})
            v2t_simulator_Configuration(self.socket, self.file, value, parameter_error=True)
            
            self.check_Seat(3)

            


###########################################################################################################################################
@allure.feature("SOA服务接口")
@allure.story("内部通信/S2SConfigCloud ")
class TestCentralLockService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.tcam = TCAM_SSH()
        # 启动partner operator
        self.partner = S2sBaseClass([("CentralLockService", "client"),("ConfigMasterService", "client")])
        # 开启tcam的v2t模拟器
        self.bgmcli.type_commands("rm -rf /data/persistent/config_*;rm -rf /data/config_service/rvs/*;shutdown -r")
        self.tcam.type_commands("mv /mnt/sdcard/jiduEM.sh /oemdata/bin/ ;reboot")
        time.sleep(280)
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.partner.method_default_timeout = 0.1
        self.file = "cloud_centrallock"
        global Publishid_now
        Publishid_now = get_lasest_event_publishId(self.partner)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
        time.sleep(5)         

    def after_each_func(self, ecu):
        self.socket.tcp_client.close()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.partner.stop_operators()
        logger.info("恢复ccp和data")
        self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
        value = modify_json_data(self.file)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.socket.tcp_client.close()
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
        time.sleep(280)
        super().after_class(self, ecu)

    @allure.title("服务CentralLockService_版本不匹配")
    def test_caseid_121212(self):
        value = modify_json_data(self.file, Version="3.0")
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData")
       
    @allure.title("服务CentralLockService_版本匹配_参数全部存在_参数在有效范围")
    def test_caseid_121212(self):
        value = modify_json_data(self.file)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42)})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                              {"out": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42)})
        
    @allure.title("服务CentralLockService_版本匹配_参数全部存在_参数在最小值")
    def test_caseid_121212(self):
        data = {"ClsDoorAndLockTimerSecs": 1,
                "LockFindKeyTimerSecs": 1}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(0.0, 0, 5.0, 0, 5.0)})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                              {"out": return_EnergyConsumptionData(0.0, 0, 5.0, 0, 5.0)})

    @allure.title("服务CentralLockService_版本匹配_参数全部存在_参数在最大值")
    def test_caseid_121212(self):
        data = {"ClsDoorAndLockTimerSecs": 59,
                "LockFindKeyTimerSecs": 9}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(300.0, 999, 30.0, 999, 30.0)})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                              {"out": return_EnergyConsumptionData(300.0, 999, 30.0, 999, 30.0)})

    @allure.title("服务CentralLockService_版本匹配_参数全部存在_一个或以上参数超范围")
    def test_caseid_121212(self):
        data = {"ClsDoorAndLockTimerSecs": 61,
                "LockFindKeyTimerSecs": 11}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v})
            v2t_simulator_Configuration(self.socket, self.file, value)
            self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData")
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                                {"out": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42)})

    @allure.title("服务CentralLockService_版本匹配_参数在有效范围_参数只有一个且正确")
    def test_caseid_121212(self):
        data = {"ClsDoorAndLockTimerSecs": 44,
                "LockFindKeyTimerSecs": 4}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v}, default_data=False)
            v2t_simulator_Configuration(self.socket, self.file, value)
            self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(11.0, 720, 13.57, 595, 16.42)})
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                                {"out": return_EnergyConsumptionData(11.0, 720, 13.57, 595, 16.42)})
        
    @allure.title("服务CentralLockService_版本匹配_参数在有效范围_一个或以上参数名称有误")
    def test_caseid_121212(self):
        data = {"ClsDoorAndLockTimerSecsXXX": 55,
                "LockFindKeyTimerSecsXXX": 5}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v})
            v2t_simulator_Configuration(self.socket, self.file, value)
            self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData")
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                                {"out": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42)})



###########################################################################################################################################
@allure.feature("SOA服务接口")
@allure.story("内部通信/S2SConfigCloud ")
class TestDoorService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.tcam = TCAM_SSH()
        # 开启tcam的v2t模拟器
        # self.bgmcli.type_commands("rm -rf /data/persistent/config_*;rm -rf /data/config_service/rvs/*;shutdown -r")
        # self.tcam.type_commands("mv /mnt/sdcard/jiduEM.sh /oemdata/bin/ ;reboot")
        # time.sleep(280)
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        # 启动partner operator
        self.partner = S2sBaseClass([("DoorService", "client"),("ConfigMasterService", "client")])
        self.partner.method_default_timeout = 0.1
        self.file = "cloud_door"
        global Publishid_now
        Publishid_now = get_lasest_event_publishId(self.partner)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
        time.sleep(5)         

    def after_each_func(self, ecu):
        self.socket.tcp_client.close()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.partner.stop_operators()
        # 恢复tcam环境
        # while True:
        #     self.tcam.type_commands("mv /oemdata/bin/jiduEM.sh /mnt/sdcard/")
        #     data = self.tcam.type_commands("ls /oemdata/bin/")
        #     if "jiduEM.sh" not in data:
        #         logger.info("配置文件清除成功")
        #         self.tcam.type_commands("reboot")
        #         break
        #     else:
        #         time.sleep(2)
        #         logger.info("等待清除配置文件")
        # time.sleep(280)
        super().after_class(self, ecu)

    @allure.title("服务DoorService_版本不匹配")
    def test_caseid_121212(self):
        value = modify_json_data(self.file, Version="1.0.0")
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData")
       
    @allure.title("服务DoorService_版本匹配_参数全部存在_参数在有效范围")
    def test_caseid_121212(self):
        value = modify_json_data(self.file)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42)})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                              {"out": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42)})
        
    @allure.title("服务DoorService_版本匹配_参数全部存在_参数在最小值")
    def test_caseid_121212(self):
        data = {"DoorOpenWarnDelayTime": 1}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(0.0, 0, 5.0, 0, 5.0)})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                              {"out": return_EnergyConsumptionData(0.0, 0, 5.0, 0, 5.0)})

    @allure.title("服务DoorService_版本匹配_参数全部存在_参数在最大值")
    def test_caseid_121212(self):
        data = {"DoorOpenWarnDelayTime": 999}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(300.0, 999, 30.0, 999, 30.0)})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                              {"out": return_EnergyConsumptionData(300.0, 999, 30.0, 999, 30.0)})

    @allure.title("服务DoorService_版本匹配_参数全部存在_一个或以上参数超范围")
    def test_caseid_121212(self):
        data = {"DoorOpenWarnDelayTime": 1001}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v})
            v2t_simulator_Configuration(self.socket, self.file, value)
            self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData")
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                                {"out": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42)})

    @allure.title("服务DoorService_版本匹配_参数在有效范围_参数只有一个且正确")
    def test_caseid_121212(self):
        data = {"DoorOpenWarnDelayTime": 255}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v}, default_data=False)
            v2t_simulator_Configuration(self.socket, self.file, value)
            self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(11.0, 720, 13.57, 595, 16.42)})
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                                {"out": return_EnergyConsumptionData(11.0, 720, 13.57, 595, 16.42)})
        
    @allure.title("服务DoorService_版本匹配_参数在有效范围_一个或以上参数名称有误")
    def test_caseid_121212(self):
        data = {"DoorOpenWarnDelayTimeXXX": 277}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k,v})
            v2t_simulator_Configuration(self.socket, self.file, value)
            self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData")
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                                {"out": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42)})



###########################################################################################################################################
@allure.feature("SOA服务接口")
@allure.story("内部通信/S2SConfigCloud ")
@pytest.mark.full
class TestWTIService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.tcam = TCAM_SSH()
        # 启动partner operator
        self.partner = S2sBaseClass([("WTIService", "client"),("ConfigMasterService", "client")])
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        # 开启tcam的v2t模拟器
        self.bgmcli.type_commands("rm -rf /data/persistent/config_service/* ;rm -rf /data/persistent/config_master/*;rm -rf /data/config_service/S2SConfig_Cloud_WTI/*;sleep 5;shutdown -r")
        self.tcam.type_commands("mv /mnt/sdcard/jiduEM.sh /oemdata/bin/ ;reboot")
        time.sleep(280)
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.partner.method_default_timeout = 0.1
        self.file = "Cloud_WTI"
        global Publishid_now
        Publishid_now = get_lasest_event_publishId(self.partner)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', self.dk.last_sync_time_entity)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', self.dk.last_sync_time_ble)       
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.ipdu.set_vehspd(0)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        time.sleep(5)         

    def after_each_func(self, ecu):
        self.socket.tcp_client.close()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        try:
            logger.info("恢复ccp和data")
            self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
            value = modify_json_data(self.file)
            v2t_simulator_Configuration(self.socket, self.file, value)
        except Exception as e:
            logger.info(e)
        finally:
            self.partner.stop_operators()
            self.socket.tcp_client.shutdown(socket.SHUT_RDWR)
            self.socket.tcp_client.close()
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
            time.sleep(280)
            super().after_class(self, ecu)

    def boon_all_open_close(self, swith):
        '''前舱盖开关状态 swith=0 开  swith=1 关 '''
        if swith == 0:
            self.io.hood_door1_open()
            self.io.hood_door2_open()
        else:
            self.io.hood_door1_close()
            self.io.hood_door2_open()
        time.sleep(1)
    
    def set_Launch_Mode_Operation_Reminder_pre1(self, bonnet=1, doorsts=[0, 0, 0, 0, 0], angle=0.0, epb=9, bltsts=0, bltst1=1):
        ''' 弹射起步引导提示信息 '''
        self.boon_all_open_close(bonnet) # 1=关闭 status.sts=1; 0=打开 status.sts=0
        self.dk.set_door_sts(doorsts)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) # SteerWheelInfo.info.isvalid=True
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', angle) # 方向盘转角 SteerWheelInfo.info.angle
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', epb) # EPB功能运行状态 EPBOperationStatu.state
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', bltsts)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', bltst1)

    def set_Launch_Mode_Operation_Reminder_pre2(self, gear=3, status=random.choice([3, 4]), fault=0, brk=11.5, acc=96.0, road=0.0, info=0, sleeptime=1):
        ''' 弹射起步引导提示信息 '''
        self.sd_tester.change_usage_mode(random.choice([11, 13])) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', random.choice([0, 1]))
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear) # gear
        dict={0:1, 1:2, 2:3, 3:4, 4:0, 5:5} # status:信号值
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg', fault)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  dict[status]) # LaunchMode.info.status
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', brk) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', acc) 
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr11, 'RoadInclnRoadIncln', road)
        time.sleep(sleeptime)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Launch Mode Operation Reminder","info":str(info)}]}, timeout=3)     
        self.partner.empty_all()

    def check_WTI(self, RoadInclnRoadInclnTriger, RoadInclnRoadInclnCancel, AccrPedlRatAccrPedlRatTriger, AccrPedlRatAccrPedlRatCancel):
        hint = "Launch Mode Operation Reminder"  
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=1)          
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 11.0)    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', AccrPedlRatAccrPedlRatTriger)                           
        self.partner.ck_wti_coming_warning_and_resp(hint, 7, timeout=2) # 进入 信号持续时间超过0.5s      
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', AccrPedlRatAccrPedlRatCancel+0.1)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=2) # 退出 acc > 95.0, 持续时间超过0.5s 
        time.sleep(2)
        self.set_Launch_Mode_Operation_Reminder_pre1()
        self.set_Launch_Mode_Operation_Reminder_pre2(status=0)  
        dict={0:[RoadInclnRoadInclnTriger+0.001, -(RoadInclnRoadInclnTriger+0.001)],1:[RoadInclnRoadInclnTriger-0.001, -(RoadInclnRoadInclnTriger-0.001)], 2:[RoadInclnRoadInclnCancel-0.001, -(RoadInclnRoadInclnCancel-0.01), 0]}
        for i in range(len(dict[0])):
            for j in range(len(dict[1])):
                for k in range(len(dict[2])):
                    logger.info(f"打印当前值 i={i}, {dict[0][i]}, 触发")
                    self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr11, 'RoadInclnRoadIncln', dict[0][i]) 
                    self.partner.ck_wti_warning_and_resp(hint, 1)  
                    logger.info(f"打印当前值 j={j}, {dict[1][j]}, 维持")
                    self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr11, 'RoadInclnRoadIncln', dict[1][j]) 
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, 1)   
                    logger.info(f"打印当前值 k={k}, {dict[2][k]}, 退出")
                    self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr11, 'RoadInclnRoadIncln', dict[2][k])      
                    self.partner.ck_wti_warning_and_resp(hint, 0)  

    @allure.title("服务WTIService_版本不匹配")
    def test_caseid_1989452(self):
        value = modify_json_data(self.file, Version="3.1.0")
        v2t_simulator_Configuration(self.socket, self.file, value, s2sconfigver_error=True)
        self.check_WTI(0.05, 0.039, 90, 95)
       
    @allure.title("服务WTIService_版本匹配_参数全部存在_参数在有效范围")
    @pytest.mark.smoke
    def test_caseid_1989453(self):
        data = {"RoadInclnRoadInclnTriger" : 0.5,
                "RoadInclnRoadInclnCancel" : 0.33,
                "AccrPedlRatAccrPedlRatTriger" : 50,
                "AccrPedlRatAccrPedlRatCancel" : 60}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.check_WTI(0.5, 0.33, 50, 60)

    @allure.title("服务WTIService_版本匹配_参数全部存在_参数在最小值")
    def test_caseid_1989454(self):
        data = {"RoadInclnRoadInclnTriger" : 0.1,
                "RoadInclnRoadInclnCancel" : 0.01,
                "AccrPedlRatAccrPedlRatTriger" : 1,
                "AccrPedlRatAccrPedlRatCancel" : 2}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.check_WTI(0.1, 0.01, 1, 2)

    @allure.title("服务WTIService_版本匹配_参数全部存在_参数在最大值")
    def test_caseid_1989455(self):
        data = {"RoadInclnRoadInclnTriger" : 0.99,
                "RoadInclnRoadInclnCancel" : 0.899,
                "AccrPedlRatAccrPedlRatTriger" : 88,
                "AccrPedlRatAccrPedlRatCancel" : 99}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.check_WTI(0.99, 0.899, 88, 99)
    
    @allure.title("服务WTIService_版本匹配_参数全部存在_一个或以上参数超范围")
    def test_caseid_1989456(self):
        data = {"RoadInclnRoadInclnTriger" : 1.001,
                "RoadInclnRoadInclnCancel" : 1.001,
                "AccrPedlRatAccrPedlRatTriger" : 101,
                "AccrPedlRatAccrPedlRatCancel" : 101}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v})
            v2t_simulator_Configuration(self.socket, self.file, value, parameter_error=True)
            
            self.check_WTI(0.05, 0.039, 90, 95)

    @allure.title("服务WTIService_版本匹配_参数在有效范围_参数只有一个且正确")
    @pytest.mark.sanity
    def test_caseid_1989457(self):
        data = {"RoadInclnRoadInclnTriger" : 0.043,
                "RoadInclnRoadInclnCancel" : 0.033,
                "AccrPedlRatAccrPedlRatTriger" : 70,
                "AccrPedlRatAccrPedlRatCancel" : 99}
        for k, v in data.items():
            self.partner.empty_all(1)
            value = modify_json_data(self.file, ConfigData={k:v}, default_data=False)
            v2t_simulator_Configuration(self.socket, self.file, value)

            if k == "RoadInclnRoadInclnTriger":
                self.check_WTI(0.043, 0.039, 90, 95)
            elif k == "RoadInclnRoadInclnCancel":
                self.check_WTI(0.05, 0.033, 90, 95)
            elif k == "AccrPedlRatAccrPedlRatTriger":
                self.check_WTI(0.05, 0.039, 70, 95)
            else:
                self.check_WTI(0.05, 0.039, 90, 99)

    @allure.title("服务WTIService_版本匹配_参数在有效范围_一个或以上参数名称有误")
    def test_caseid_1989458(self):
        data = {"RoadInclnRoadInclnTrigerXXX" : 0.099,
                "RoadInclnRoadInclnCancelXXX" : 0.099,
                "AccrPedlRatAccrPedlRatTrigerXXX" : 99,
                "AccrPedlRatAccrPedlRatCancelXXX" : 99}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v}, default_data=False)
            v2t_simulator_Configuration(self.socket, self.file, value, parameter_error=True)
            
            self.check_WTI(0.05, 0.039, 90, 95)
            

###########################################################################################################################################
@allure.feature("SOA服务接口")
@allure.story("内部通信/S2SConfigCloud ")
class TestWindowAppService(TestBase):
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
        self.partner = S2sBaseClass([("WindowAppService", "client"),("ConfigMasterService", "client")])
        self.partner.method_default_timeout = 0.1
        self.file = "cloud_windowapp"
        global Publishid_now
        Publishid_now = get_lasest_event_publishId(self.partner)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.socket = SocketClient("172.16.5.21", random.randint(1000, 9999), "172.16.5.31", 5678)
        time.sleep(5)         

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
        time.sleep(280)
        super().after_class(self, ecu)

    @allure.title("服务WindowAppService_版本不匹配")
    def test_caseid_121212(self):
        value = modify_json_data(self.file, Version="2.0.0")
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData")
       
    @allure.title("服务WindowAppService_版本匹配_参数全部存在_参数在有效范围")
    def test_caseid_121212(self):
        value = modify_json_data(self.file)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42)})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                              {"out": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42)})
        
    @allure.title("服务WindowAppService_版本匹配_参数全部存在_参数在最小值")
    def test_caseid_121212(self):
        data = {"WaitWindowShortDelayTimeSecs" : 1,
                "WaitOtherWindowShortDelayTimeSecs" : 1,
                "WindowActionDelayTime" : 1,
                "WinFrntShoPosn" : 1,
                "WinRearShoPosn": 1}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(0.0, 0, 5.0, 0, 5.0)})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                              {"out": return_EnergyConsumptionData(0.0, 0, 5.0, 0, 5.0)})

    @allure.title("服务WindowAppService_版本匹配_参数全部存在_参数在最大值")
    def test_caseid_121212(self):
        data = {"WaitWindowShortDelayTimeSecs" : 9,
                "WaitOtherWindowShortDelayTimeSecs" : 9,
                "WindowActionDelayTime" : 999,
                "WinFrntShoPosn" : 99,
                "WinRearShoPosn": 99}
        value = modify_json_data(self.file, ConfigData=data)
        v2t_simulator_Configuration(self.socket, self.file, value)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(300.0, 999, 30.0, 999, 30.0)})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                              {"out": return_EnergyConsumptionData(300.0, 999, 30.0, 999, 30.0)})

    @allure.title("服务WindowAppService_版本匹配_参数全部存在_一个或以上参数超范围")
    def test_caseid_121212(self):
        data = {"WaitWindowShortDelayTimeSecs" : 11,
                "WaitOtherWindowShortDelayTimeSecs" : 11,
                "WindowActionDelayTime" : 1001,
                "WinFrntShoPosn" : 101,
                "WinRearShoPosn": 101}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v})
            v2t_simulator_Configuration(self.socket, self.file, value)
            self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData")
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                                {"out": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42)})

    @allure.title("服务WindowAppService_版本匹配_参数在有效范围_参数只有一个且正确")
    def test_caseid_121212(self):
        data = {"WaitWindowShortDelayTimeSecs" : 5,
                "WaitOtherWindowShortDelayTimeSecs" : 5,
                "WindowActionDelayTime" : 555,
                "WinFrntShoPosn" : 55,
                "WinRearShoPosn": 55}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k:v}, default_data=False)
            v2t_simulator_Configuration(self.socket, self.file, value)
            self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                        {"data": return_EnergyConsumptionData(11.0, 720, 13.57, 595, 16.42)})
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                                {"out": return_EnergyConsumptionData(11.0, 720, 13.57, 595, 16.42)})
        
    @allure.title("服务WindowAppService_版本匹配_参数在有效范围_一个或以上参数名称有误")
    def test_caseid_121212(self):
        data = {"WaitWindowShortDelayTimeSecsXXX" : 7,
                "WaitOtherWindowShortDelayTimeSecsXXX" : 7,
                "WindowActionDelayTimeXXX" : 777,
                "WinFrntShoPosnXXX" : 77,
                "WinRearShoPosnXXX": 77}
        for k, v in data.items():
            value = modify_json_data(self.file, ConfigData={k,v})
            v2t_simulator_Configuration(self.socket, self.file, value)
            self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData")
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                                {"out": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42)})








