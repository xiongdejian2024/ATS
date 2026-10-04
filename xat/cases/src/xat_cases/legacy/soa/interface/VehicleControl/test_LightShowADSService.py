# -*- coding: utf-8 -*-
"""
@File        : test_soa_lightservice.py
@Author      : peipei.yang_ext@jiduatuo.com
@Time        : 2024/03/26 15:00 PM
@Description : Test s2s interface about rctalarm function
"""

import pytest
import openpyxl
from time import sleep
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
# from test_case.bgm.digital_key.test_digital_key_baseclass import DigitalKey
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.common.logger import logger


def readJsonGetInfo(file_path,num):
    frmaeNum = 0
    signalValueList = [[] for _ in range(num)]
    stopFrameList = []
    tempList = [[] for _ in range(num)]
    with open(file_path) as json_file:
        data = json.load(json_file)
        jsonValue = data['arry']
        frmaeNum = len(jsonValue)
        #i 为每一帧数据

        for i in range(len(jsonValue)):
            existSignal = []
            k = 0
            for j in range(len(jsonValue[i])):
                if len(jsonValue[i]) == num:
                    signalValueList[list(jsonValue[i][j].values())[0]].append(list(jsonValue[i][j].values())[1])        
                    tempList[list(jsonValue[i][j].values())[0]] = list(jsonValue[i][j].values())[1]
                #当前帧json中没有写全，未写的按上帧进行赋值
                elif list(jsonValue[i][j].values())[0] != -1  :
                    logger.info(f"----i={i}--")
                    k += 1
                    signalValueList[list(jsonValue[i][j].values())[0]].append(list(jsonValue[i][j].values())[1])
                    tempList[list(jsonValue[i][j].values())[0]] = list(jsonValue[i][j].values())[1] 
                      
                    if list(jsonValue[i][j].values())[0] not in existSignal:
                            existSignal.append(list(jsonValue[i][j].values())[0])
                    if k == len(jsonValue[i]):
                        print("k=",str(k))
                        for x in range(num) :
                            if x not in existSignal:
                                print("x",str(x))
                                signalValueList[x].append(tempList[x])
                # -1帧
                elif len(jsonValue[i]) == 1:  
                    stopFrameList.append(i)                       
    return(signalValueList,frmaeNum,stopFrameList)     
  
def extract_continuous_numbers(nums):
    result = []
    if len(nums) != 0:
        temp = []
        for i in range(len(nums)-1):
            if nums[i+1] - nums[i] == 1:
                temp.append(nums[i])
            else:
                temp.append(nums[i])
                result.append(temp)
                temp = []
        temp.append(nums[-1])
        result.append(temp)
    return result

@allure.feature("SOA服务接口")
@allure.story("整车控制/LightShowADSService")
@pytest.mark.adsls
class TestLightShowADSService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        partner_process_check()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.vehicle_type = ecu.tc_config['veh_type']#修改车辆配置
        logger.info(f"打印车辆配置{self.vehicle_type}")
        if self.vehicle_type == "mars1":
            self.sd_tester.write_single_ccp(950, 1)#指定车型marsone
            self.json_path = os.path.join(os.getcwd(), "case_helper/config/marsone_json")
        elif self.vehicle_type == "venus":
            self.sd_tester.write_single_ccp(950, 2)
            self.json_path = os.path.join(os.getcwd(), "case_helper/config/venus_json")
        else:
            assert False 

        #self.set_gear("GearN")
        self.nucapp.bgm_diag_line_down()
        
        # 启动partner operator
        self.partner = S2sBaseClass([("LightService", "client"),
                                     ("ChassisService", "client")])
        self.partner.method_default_timeout = 0.1
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.sd_tester.write_single_ccp(950, 2)
        sleep(1)

    def before_each_func(self, ecu):
        self.sd_tester.tester_present()
        self.set_gear("GearN")
        self.set_gear("GearP")
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 35, "inhibitSts": False}]})#普通氛围灯不禁用
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 25, "inhibitSts": False}]})#智能氛围灯不禁用
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 0}) #外灯模式关闭
        #轮眉灯状态
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntWheelLampLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntWheelLampRi', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReWheelLampLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReWheelLampRi', 0)
        #AI灯状态
        self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY1', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY2', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY3', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY4', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY1', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY2', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY3', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY4', 0)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 0)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'IntrBriSts', 0)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                            {"lights": [{"light": {"type": 33, "zoneId": 12}, "mode": 0,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                            {"lights": [{"light": {"type": 33, "zoneId": 13}, "mode": 0,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                            {"lights": [{"light": {"type": 33, "zoneId": 14}, "mode": 0,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}]})
        self.partner.empty_all()
        super().before_each_func(ecu, start=False)
        

    def after_each_func(self, ecu):
        self.sd_tester.stop_tester_present()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.nucapp.bgm_diag_line_up()
        self.partner.stop_operators()
        super().after_class(self, ecu)
        
    def set_gear(self, gear):
        """设置档位"""
        map = {"GearP": 0, "GearN": 2, "GearR": 1, "GearD": 3}
        self.dk.set_chassis_service_gear(gear)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetGear", {}, {"out": map[gear]}, timeout=1.5)
        logger.info(f"set_gear:{gear} success")

    def ck_frame_period(self ,siganlName,stopFrameList,periodTime,deviationValue):
        #stopFrameList 需要通过extract_continuous_numbers转换成类似于[[1], [3, 4], [6], [9], [14, 15, 16], [19]]
        if len(stopFrameList) == 0:
            self.bgm_eth_inter.ck_period_time(siganlName,period=periodTime, deviation=deviationValue)
        else:
            #连续停帧的长度
            temp = 0
            for i in range(len(stopFrameList)):
                temp += len(stopFrameList[i])
                startFrame = stopFrameList[i][0]
                stopFrame = stopFrameList[i][len(stopFrameList[i])-1]
                #length = len(stopFrameList)
                # frameInterval =self.bgm_eth_inter.get_signal_items(siganlName)[1][stopFrame-temp+1] - self.bgm_eth_inter.get_signal_items[1][stopFrame-temp]
                frameInterval =self.bgm_eth_inter.get_signal_items(siganlName)[stopFrame-temp+1][1] - self.bgm_eth_inter.get_signal_items(siganlName)[stopFrame-temp][1]
                logger.info(f"frameInterval={frameInterval}")#打印周期
                #assert(frameInterval)
                assert abs(float(frameInterval) - periodTime*(len(stopFrameList[i])+1)) / (periodTime*(len(stopFrameList[i])+1)) < deviationValue

    def read_json(self, json_name, info):
        return readJsonGetInfo(os.path.join(self.json_path, f'{json_name}.json'),len(info))
    
    def ads_flashing_test(self, json_name, switch_gear=None):
        period=0.02
        self.nucapp.bgm_diag_line_down()
        info = ["WheelLampFrntLe", "WheelLampFrntRi", "WheelLampRearLe", "WheelLampRearRi"]
        signal_val, frame_num, stop_frame_list =self.read_json(json_name, info)
        logger.info(f"signal_val:{signal_val}, frame_num:{frame_num}, stop_frame_list={stop_frame_list}")
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl", {"seqId": json_name, "act": 1}) 
        sleep(1)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl", {"seqId": json_name, "act": 0})

        if switch_gear:
            sleep(0.1)
            self.set_gear(switch_gear)
        sleep(frame_num * period * 3)
            
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl", {"seqId": json_name, "act": 1})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        
        for i in range(len(info)):
            logger.info(f"[{i}]expect values:{signal_val[i]}")
            
            #默认循环灯效校验2个json周期
            act_values = self.bgm_eth_inter.get_signal_values(info[i])[0:len(signal_val[i]) * 2]
            logger.info(f"[{i}]actual values:{act_values}")
            if switch_gear in ["GearD", "GearN", "GearR"]:
                assert act_values == signal_val[i][:5] or act_values == signal_val[i][:6] or act_values == signal_val[i][:7]
            else:
                assert act_values == signal_val[i] * 2

    def ck_ads_frame_period(self, signal_name: str, period, deviation=0.2, permit_fail_times=0, del_last_num=0):
        items = self.bgm_eth_inter.get_signal_items(signal_name)[:-del_last_num]
        fail_timestamps = []
        last_time = None
        for item in items:
            if last_time is None:
                last_time = item[1]
            else:
                if abs(float(item[1]) - float(last_time) - period) / period > deviation:
                    fail_timestamps.append(item[1])
                    assert len(fail_timestamps) <= permit_fail_times, \
                    f"周期偏差次数过多, 失败时间戳{fail_timestamps}, 周期:{float(item[1])}-{float(last_time)}={float(item[1])-float(last_time)}"
                last_time = item[1]
        return len(fail_timestamps)

    def ads_solidon_test(self, json_name):
        period=0.02
        self.nucapp.bgm_diag_line_down()
        signal_list = ["WheelLampFrntLe", "WheelLampFrntRi", "WheelLampRearLe", "WheelLampRearRi"]
        # json_name = 'ADS_SOLIDON_LEVEL1'
        signal_val, frame_num, stop_frame_list = self.read_json(json_name, signal_list)
    
        # 轮眉灯非循环灯stop后会补发三帧最后值，再补发三帧0
        stop_frame_list = [frame_num+i for i in range(6)]  if stop_frame_list == [] else stop_frame_list 

        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl", {"seqId": json_name, "act": 1})
        sleep(2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl", {"seqId": json_name, "act": 0})
        sleep((frame_num + len(stop_frame_list)) * period + 3)
        
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl", {"seqId": json_name, "act": 1})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        
        for i in range(len(signal_list)):
            logger.info(f"----i={i}--signal_val={signal_val[i]}")
            
            result_val = self.bgm_eth_inter.get_signal_values(signal_list[i])[0:len(signal_val[i])]
            logger.info(f"----i={i}--result_val={result_val}")
            
            assert result_val == signal_val[i]
            self.ck_ads_frame_period(signal_list[i], period, 0.5, del_last_num=6) # 帧周期误差范围在10ms~30ms内
            
    @allure.title("ADS灯_Venus_ADS_FLASHING")#venus充电中ADS闪烁(循环灯效)
    @pytest.mark.sanity
    def test_caseid_1985239(self):
        self.ads_flashing_test('ADS_FLASHING')

    @allure.title("ADS灯_Venus_ADS_FLASHING_LEVEL4")
    @pytest.mark.full
    def test_caseid_1988300(self):
        self.ads_flashing_test('ADS_FLASHING_LEVEL4')
        
    @allure.title("ADS灯_Venus_ADS_FLASHING_LEVEL10")
    @pytest.mark.full
    def test_caseid_1988303(self):
        self.ads_flashing_test('ADS_FLASHING_LEVEL10')

    @allure.title("Venus切换到非P档位_HPI灯继续播放")
    @pytest.mark.full
    def test_caseid_1989649(self):
        self.sd_tester.change_usage_mode(13)
        # 从P档到N档到D档到R档到P档
        self.ads_flashing_test('ADS_FLASHING', switch_gear="GearN")
        self.ads_flashing_test('ADS_FLASHING', switch_gear="GearD")
        self.ads_flashing_test('ADS_FLASHING', switch_gear="GearR")
        self.ads_flashing_test('ADS_FLASHING', switch_gear="GearP")

        # 从P档切换到非P档
        self.set_gear("GearP")
        self.ads_flashing_test('ADS_FLASHING', switch_gear="GearN")
        self.set_gear("GearP")
        self.ads_flashing_test('ADS_FLASHING', switch_gear="GearD")
        self.set_gear("GearP")
        self.ads_flashing_test('ADS_FLASHING', switch_gear="GearR")
        
    @allure.title("ADS灯_Venus_ADS_SOLIDON")#venus解锁ADS常亮(触发式)
    @pytest.mark.full
    def test_caseid_1985242(self):
        self.ads_solidon_test('ADS_SOLIDON')
      
    @allure.title("ADS灯_Venus_ADS_SOLIDON_LEVEL1")
    @pytest.mark.sanity
    def test_caseid_1988306(self):
        self.ads_solidon_test('ADS_SOLIDON_LEVEL1')

    @allure.title("ADS灯_Venus_ADS_SOLIDON_LEVEL2")
    @pytest.mark.full
    def test_caseid_1988307(self):
        self.ads_solidon_test('ADS_SOLIDON_LEVEL2')

    @allure.title("ADS灯_Venus_ADS_SOLIDON_LEVEL4")
    @pytest.mark.full
    def test_caseid_1988308(self):
        self.ads_solidon_test('ADS_SOLIDON_LEVEL4')
        
    @allure.title("ADS灯_Venus_ADS_SOLIDON_LEVEL10")
    @pytest.mark.full
    def test_caseid_1988309(self):
        self.ads_solidon_test('ADS_SOLIDON_LEVEL10')
        
    @allure.title("ADS灯_Venus_ADS_SOLIDON_LEVEL20")
    @pytest.mark.full
    def test_caseid_1988310(self):
        self.ads_solidon_test('ADS_SOLIDON_LEVEL20')