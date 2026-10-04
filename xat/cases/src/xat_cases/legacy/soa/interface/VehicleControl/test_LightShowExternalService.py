# -*- coding: utf-8 -*-
"""
@File        : test_soa_lightservice.py
@Author      : peipei.yang_ext@jiduatuo.com
@Time        : 2024/03/26 15:00 PM
@Description : Test s2s interface about rctalarm function
"""

import pytest
import openpyxl
import json
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


class LightShowType(Enum):
    AI = 0
    WHEEL = 1
    Sequence = 2


class LightShowTest():

    def __init__(self, vehicle_type):
        veh_map = {"mars1": "marsone", 
                   "venus": "venus"}
        self.ls_json_dir = os.path.join(os.getcwd(), f"case_helper/config/{veh_map.get(vehicle_type, 'marsone')}_json")
        self.db_file_path = os.path.join(os.getcwd(), f"case_helper/config/LightShowSignalDB.xlsx")

        self.json_array = []
        self.light_show_type = None     # 灯光秀类型，AI或WHEEL或SEQUENCE
        self.id2signal_map = {}         # {0："AIInteractionLampLeftY1", 1:"AIInteractionLampLeftY2", ...}
        self.pdu2id_map = {}            # {2011: [0, 1, 3, 4], 2012: [5, 6, 7, 8], ...}
        self.id2pdu_map = {}            # {0: [2011], 1: [2011], ...}
        self.frame0_not_contain_all = False


    def __load_light_show_json(self, json_name: str):
        """读取灯光秀json文件"""
        with open(os.path.join(self.ls_json_dir, json_name)) as file:
            data = json.load(file)
        return data['arry']
    
    def __parse_db_by_json(self, json_name: str):
        """
        根据JSON文件名解析LightShowSignalDB.xlsx文件中对应灯的信息
        @param json_name: 灯光秀json文件名
        Returns: tuple: 包含三个字典，分别对应id到信号的映射、pdu到id的映射和id到pdu的映射
        """
        if json_name.startswith('AI_'):
            self.light_show_type = LightShowType.AI
            sheet_name = self.light_show_type.name
        elif json_name.startswith('WHEEL_'):
            self.light_show_type = LightShowType.WHEEL
            sheet_name = self.light_show_type.name
        else:
            self.light_show_type = LightShowType.Sequence
            sheet_name = 'Sequence'
            
        id2signal_map = {}          # {0："AIInteractionLampLeftY1", 1:"AIInteractionLampLeftY2", ...}
        pdu2id_map = {}             # {2011: [0, 1, 3, 4], 2012: [5, 6, 7, 8], ...}
        id2pdu_map = {}             # {0: [2011], 1: [2011], ...}
        
        mywb = openpyxl.load_workbook(self.db_file_path) 
        mysheet = mywb[sheet_name]
        
        for i in range(2, mysheet.max_row + 1): 
            beadid = mysheet.cell(i, 1).value
            signal = mysheet.cell(i, 2).value
            pduid = mysheet.cell(i, 3).value

            id2signal_map[beadid] = signal
            id2pdu_map[beadid] = pduid
            if pduid not in pdu2id_map:
                pdu2id_map[pduid] = [beadid]
            else:
                pdu2id_map[pduid].append(beadid)
        return id2signal_map, pdu2id_map, id2pdu_map
    
    def __find_last_valid_value(self, values):
        """
        找到最后一个有效值,即不为None的值
        params values: 值列表
        Returns:
            Any: 最后一个有效值
        """
        for value in reversed(values):
            if value is not None:
                return value

    # 处理外灯
    def pre_handle_external_light_show_json(self, json_name):
        """
        对读取的handle做预处理,比如9个灯组,其中序列中亮度不变化的灯组，可能没有写，另外对{"id":-1,"value":255}进行处理
        比如4个灯组处理成[[100, 100, 100, 100], [None, None, None, None], [99, 99, 99, 99] ...]的格式
        """
        self.id2signal_map, self.pdu2id_map, self.id2pdu_map = self.__parse_db_by_json(json_name)
        logger.info(f"[id2signal_map]:{self.id2signal_map}")
        logger.info(f"[pdu2id_map]:{self.pdu2id_map}")
        logger.info(f"[id2pdu_map]:{self.id2pdu_map}")
        self.json_array = self.__load_light_show_json(json_name)
        
        id_values_map = {}  # 承载json解析后预期发送beadid及对应信号值列表
        all_pdus = set()
        
        # 原则:每一帧数据中:只发送涉及到的id的pdu发送,其中未明确id对应value值的保持last_value
        # 比如上一帧中有pdu1和pdu2两个pdu,但是这一帧只改变pdu1中的signal1,则只发送pdu1,不会发送pdu2
        for index, array_item in enumerate(self.json_array):  
            cur_pdus = set()  # 当前帧的灯珠涉及哪些pdu
            cur_ids = []
            
            # 解析出当前帧涉及哪些灯珠id，并且将对应的value值存入id_values_map中
            # 特殊处理，-1表示无效数据，不发送，等待1帧的时间
            if len(array_item) == 1 and array_item[0]['id'] == -1: 
                for beadid in id_values_map:
                    id_values_map[beadid].append(None)
                continue
            
            # 指定灯珠正常解析填值
            for bead in array_item:
                beadid = bead['id']
                beadvalue = bead['value']
                
                cur_pdus.add(self.id2pdu_map[beadid])
                cur_ids.append(beadid)
                
                if beadid in id_values_map.keys():
                    id_values_map[beadid].append(beadvalue)
                else:
                    id_values_map[beadid] = [beadvalue]

            # 当前的pdu中在json中的id发送上一帧的值，没有在json中的灯珠id发送0(如SEQUENCE_CHARGING_100第0帧没有包含所有灯id)
            for pdu in cur_pdus:
                for beadid in self.pdu2id_map[pdu]:
                    if beadid not in cur_ids:
                        if beadid in id_values_map.keys():
                            id_values_map[beadid].append(self.__find_last_valid_value(id_values_map[beadid]))
                        else:
                            id_values_map[beadid] = [0]
                            self.frame0_not_contain_all = True
            
            # 其他的pdu发送None
            for pdu in all_pdus:
                if pdu not in cur_pdus:
                    for beadid in self.pdu2id_map[pdu]:
                        id_values_map[beadid].append(None)
            
            all_pdus |= cur_pdus
                        
        return id_values_map
    
    def double_check_period(self, index, items, last_time, jump_count, period=0.02):
        """
        实测灯光秀周期偶发偏差很大,如果出现一次偏差很大,则校验前后两帧的周期为2 * period也算过
        """
        if last_time is None:
            return True  # 说明是第一帧数据
        
        try:
            interval = float(items[index][1]) - last_time
            # logger.info(f"cur:{items[index]}, index:{index}/{len(items)} interval:{interval}, jump_count:{jump_count}")
            
            if jump_count == 0: # 为倒数第6帧立即发送，预期小于0.02
                assert interval < 0.02, \
                    f"[{items[index]}][jump_count:{jump_count}]与上一帧时间间隔为{interval}，与预期小于0.02不符"
            elif jump_count >= 500: # 灯舞长时间播放jump_count较大时，偶尔误差较大
                assert period * jump_count - jump_count/500 * 0.03 < interval < period * jump_count + jump_count/500 * 0.03, \
                    f"[{items[index]}][jump_count:{jump_count}]与上一帧时间间隔为{interval}，与预期{period * jump_count}不符"
            else:
                assert period * jump_count - 0.03 < interval < period * jump_count + 0.03, \
                    f"[{items[index]}][jump_count:{jump_count}]与上一帧时间间隔为{interval}，与预期{period * jump_count}不符"
                    
        except AssertionError as e:
            if jump_count == 1:  # 只在连续有效帧时给予第二次判断机会
                if index == 1: # 如果是0,1,2帧中1与0间隔不对，则只能判断0-2是否2倍周期
                    if 0.6 < float(items[index+1][1] - items[index-1][1]) / (period * 2) < 1.4:
                        return True
                if index > 1: # 如果类似1,2,3中2与1间隔不对，则可以判断1-3是否2倍周期或2-4是否2倍周期，因为如果1和2间隔不对，则要么0-1间隔不对，要么2-3间隔不对
                    if 0.6 < float(items[index+1][1] - items[index-1][1]) / (period * 2) < 1.4 or 0.6 < float(items[index][1] - items[index-2][1]) / (period * 2) < 1.4:
                        assert True
            else:
                assert False, str(e)

    def ck_external_signal_values(self, beadid, signal, pdu_items, json_values, loop_num, ck_last_three_frame=True):
        """
        校验外灯灯光秀实际下行数据是否与预期一致
        @param pdu_items: 实际下行数据,  [(pcap_index, timestamp, signal_value), (), ()...]
        @param json_values: 预期数据
        @param loop_num: 实际循环次数，默认1：一次完整播放，-1：小于一次循环，2：超过1次，不到2次，3：超过2次
        @param ck_last_three_frame: 是否检查最后3帧
        """    
        tmp_json_values = copy.deepcopy(json_values)
        last_time = None
        last_value = None
        # json_last_value_is_None = False

        if not pdu_items:
            assert False, "未解析出以太网数据"

        for index, item in enumerate(pdu_items): 
            if len(tmp_json_values) == 0:
                tag = f"还有pdu数据没有校验完{pdu_items[index:]}, 应该已超过1轮循环"
                if loop_num == -1:
                    if self.light_show_type in [LightShowType.AI, LightShowType.WHEEL]  and index < len(pdu_items) - 3:
                        assert False, tag
                    elif self.light_show_type == LightShowType.Sequence and index < len(pdu_items) - 6:
                        assert False, tag
                elif loop_num == 1 and index < len(pdu_items) - 6:
                    assert False, tag
                elif loop_num not in [-1, 1]:
                    tmp_json_values = copy.deepcopy(json_values)

            find_not_none = False
            jump_count = 1
            while not find_not_none:  # 找到预期数据中非None的有效值
                if tmp_json_values:
                    exp_value = tmp_json_values.pop(0)
                else:
                    # todo: 最后的数据是None，只在触发式见过，没有见循环灯效有最后数据是None的情况
                    # json_last_value_is_None = True
                    if loop_num > 1:
                        tmp_json_values = copy.deepcopy(json_values)
                        if tmp_json_values[0] == 0 and self.frame0_not_contain_all:
                            tmp_json_values[0] = self.__find_last_valid_value(json_values)
                    else:
                        break
                if exp_value is None: # 不用区分是不是第一个就是None，因为下面对第一次做了不校验时间间隔的处理
                    jump_count += 1
                    continue
                else:
                    find_not_none = True
                    break

            # 最后3-6帧要特殊处理，但数据长度要至少大于6。所有灯效正常退出补发3帧最后有效值，调stop再发3帧0
            if len(pdu_items) > 6 and len(pdu_items) - 3 > index >= len(pdu_items) - 6 and loop_num == 1:
                assert item[2] == last_value, "外灯灯光秀(非循环)正常播完会补发3帧最后值"

                if index == len(pdu_items) - 6: # 倒数第6帧的因为立即触发发送3帧最后值，比预期少1个20ms周期
                    self.double_check_period(index, pdu_items, last_time, jump_count-1)
                else:
                    self.double_check_period(index, pdu_items, last_time, jump_count)
            
            elif index >= len(pdu_items) - 3 and ck_last_three_frame:
                if self.light_show_type in [LightShowType.AI, LightShowType.WHEEL]:
                    assert item[2] == 0, "AI和轮眉（不管是否循环灯效）调stop后最后3帧应该是0"
                elif self.light_show_type == LightShowType.Sequence:
                    assert item[2] == last_value, "Sequence（不管是否循环灯效）调stop后最后3帧应该为最后值"
                else:
                    assert False, "未知的灯效类型"
                    
                if index != len(pdu_items) - 3: # 倒数第3帧的因为调用stop触发，和前一帧间隔不可控，故不做校验
                    self.double_check_period(index, pdu_items, last_time, jump_count=1)
            
            else:  # 正常校验信号
                assert item[2] == exp_value, f"[id:{beadid}][signal:{signal}][index:{index}][{item}]与预期{exp_value}不符"
                self.double_check_period(index, pdu_items, last_time, jump_count)

            last_value = item[2]
            last_time = float(item[1])

        if tmp_json_values and tmp_json_values != [None] * len(tmp_json_values) and loop_num == 1:
            assert False, f"预期一轮完整播放，json中还有数据没有在pcap中体现{tmp_json_values}"


@allure.feature("SOA服务接口")
@allure.story("整车控制/LightShowExternalService")
@pytest.mark.els
class TestLightShowExternalService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        partner_process_check()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.vehicle_type = ecu.tc_config['veh_type']#修改车辆配置
        # self.vehicle_type = "mars1"#强行改车辆配置
        self.ls = LightShowTest(self.vehicle_type)

        logger.info(f"打印车辆配置{self.vehicle_type}")
        if self.vehicle_type == "mars1":
            self.json_path = os.path.join(os.getcwd(), "case_helper/config/marsone_json")
        elif self.vehicle_type == "venus":
            self.json_path = os.path.join(os.getcwd(), "case_helper/config/venus_json")
        else:
            logger.info(f"车辆配置有误，请线下检查")

        # 启动partner operator
        self.partner = S2sBaseClass([("LightService", "client"),
                                     ("ChassisService", "client")])
        self.partner.method_default_timeout = 0.1
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        # 测试灯关秀的前提，非P挡，诊断激活线断开
        
    def before_each_func(self, ecu):
        self.sd_tester.tester_present()
        self.nucapp.bgm_diag_line_down()#诊断激活线断开
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "InteriorLampSequenceControl",
                                         {"seqId": "OVERLAY_TWEETER_OFF", "act": 1})#扬声器关
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
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT,"LightControl",
                {"lights": [{ "light": {"type": 24, "zoneId": 0},"mode": 0,}]})#智能氛围灯
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT,"LightControl",
                {"lights": [{ "light": {"type": 34, "zoneId": 0},"mode": 0,}]})#普通氛围灯
        self.partner.empty_all()
        super().before_each_func(ecu, start=False)
        self.ls.frame0_not_contain_all = False
        

    def after_each_func(self, ecu):
        self.sd_tester.stop_tester_present()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.nucapp.bgm_diag_line_up()#诊断激活线连上
        self.partner.stop_operators()
        super().after_class(self, ecu)
        
    def set_gear(self, gear):
        """设置档位"""
        map = {"GearP": 0, "GearN": 2, "GearR": 1, "GearD": 3}
        self.dk.set_chassis_service_gear(gear)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetGear", {}, {"out": map[gear]}, timeout=1.5)

    def external_light_show_test(self, json_name, is_loop = False, loop_num: int = 1):
        """
        处理数据并抓包校验外灯灯光秀，并校验下行pdu是否与预期一致
        @param json_name: 灯光秀json文件名
        @param is_loop: 是否循环播放
        @param loop_num: 循环次数，默认1：一次完整播放，-1：小于一次循环，2：超过1次，不到2次，3：超过2次 
        """
        self.nucapp.bgm_diag_line_down()
        id_values_map = self.ls.pre_handle_external_light_show_json(f"{json_name}.json")
        logger.info(f"[id_values_map]:{id_values_map}")
        frames = len(self.ls.json_array)  # 帧数
        logger.info(f"[frames_number]:{frames}")
        
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl",{"seqId": json_name, "act": 1})  # stop
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump(host="172.16.5.1", port=30500)#开始抓包
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl", {"seqId": json_name, "act": 0})  # start
        
        if loop_num == -1:
            sleep(0.02 * frames // 2)
        elif loop_num == 1:  # 此处只用于is_loop=False的场景，因为如何循环播放，无法精准控制刚好一轮播放完成的时候停止
            sleep(0.02 * frames + 1)
        elif loop_num == 2:
            sleep(0.02 * frames * 2 + 1)
        else:
            assert False, f"loop_num={loop_num}不合法"
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl",
                                         {"seqId": json_name, "act": 1})
        sleep(1.5)  # 给足3帧回0的时间
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()#停止抓包
        
        for beadid, exp_values in id_values_map.items():
            signal = self.ls.id2signal_map[beadid]
            items = self.bgm_eth_inter.get_signal_items(signal)
            if not is_loop and loop_num != -1:
                exp_loop_num = 1   # 非循环播放灯效，即使播放时间超过1次，也只会有一次循环
            elif is_loop and loop_num == 1:
                exp_loop_num = 2   # 循环播放灯效，如果播放时间超过1次，则至少会播放超过1次
            else:
                exp_loop_num = loop_num
            self.ls.ck_external_signal_values(beadid, signal, items, exp_values, exp_loop_num)

    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_轮眉灯_车外语音播报异常")#WHEEL_AICOMMUNICATION_BROCAST_ERR(循环灯效)
    @pytest.mark.full
    def test_caseid_1984428(self):
        for loop_num in [-1, 2]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("WHEEL_AICOMMUNICATION_BROCAST_ERR", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_轮眉灯_车外语音执行")#WHEEL_AICOMMUNICATION_BROCAST_OK(循环灯效)
    @pytest.mark.smoke
    def test_caseid_1984429(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("WHEEL_AICOMMUNICATION_BROCAST_OK", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_轮眉灯_车外语音聆听")#WHEEL_AICOMMUNICATION_LISTEN(循环灯效)
    @pytest.mark.full
    def test_caseid_1984430(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("WHEEL_AICOMMUNICATION_LISTEN", True, loop_num)

    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_轮眉灯_车外语音等待")#WHEEL_AICOMMUNICATION_STANDBY(触发灯效)
    @pytest.mark.full
    def test_caseid_1984431(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("WHEEL_AICOMMUNICATION_STANDBY", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_轮眉灯_车外语音识别处理")#WHEEL_AICOMMUNICATION_THINK(循环灯效)
    @pytest.mark.full
    def test_caseid_1984432(self):
        self.sd_tester.write_single_ccp(950, 1)
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("WHEEL_AICOMMUNICATION_THINK", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_轮眉灯_车外语音唤醒")#WHEEL_AICOMMUNICATION_WAITING(触发灯效)
    @pytest.mark.sanity
    def test_caseid_1984433(self):
        self.sd_tester.write_single_ccp(950, 1)
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("WHEEL_AICOMMUNICATION_WAITING", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_轮眉灯_车外语音唤醒等待")#WHEEL_AICOMMUNICATION_WAKEUPWAIT(循环灯效)
    @pytest.mark.full
    def test_caseid_1984434(self):
        self.sd_tester.write_single_ccp(950, 1)
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("WHEEL_AICOMMUNICATION_WAKEUPWAIT", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_轮眉灯_WHEEL_AVP_P")#WHEEL_AVP_P(触发灯效)
    @pytest.mark.sanity
    def test_caseid_1984435(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("WHEEL_AVP_P", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_AI灯_充电中25%")#AI_CHARGE_CHARGING_25(循环灯效)
    @pytest.mark.smoke
    def test_caseid_1984436(self):
        for loop_num in [-1, 2]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("AI_CHARGE_CHARGING_25", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_AI灯_充电中50%")#AI_CHARGE_CHARGING_50(循环灯效)
    @pytest.mark.full
    def test_caseid_1984437(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("AI_CHARGE_CHARGING_50", True, loop_num)

    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_AI灯_充电中75%")#AI_CHARGE_CHARGING_75(循环灯效)
    @pytest.mark.full
    def test_caseid_1984438(self):
        for loop_num in [-1, 2]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("AI_CHARGE_CHARGING_75", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_AI灯_充电中100%")#AI_CHARGE_CHARGING_100(循环灯效)
    @pytest.mark.full
    def test_caseid_1984439(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("AI_CHARGE_CHARGING_100", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_AI灯_充电中125%")#AI_CHARGE_CHARGING_125(循环灯效)  
    @pytest.mark.full
    def test_caseid_1984440(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("AI_CHARGE_CHARGING_125", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_AI灯_充电完成25%")#AI_CHARGE_DONE_25(触发灯效)  
    @pytest.mark.full
    def test_caseid_1984442(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("AI_CHARGE_DONE_25", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_AI灯_充电完成50%")#AI_CHARGE_DONE_50(触发灯效)  
    @pytest.mark.full
    def test_caseid_1984441(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("AI_CHARGE_DONE_50", False, loop_num)

    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_AI灯_充电完成75%")#AI_CHARGE_DONE_75(触发灯效)  
    @pytest.mark.full
    def test_caseid_1984443(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("AI_CHARGE_DONE_75", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_AI灯_充电完成100%")#AI_CHARGE_DONE_100(循环灯效)  
    @pytest.mark.sanity
    def test_caseid_1984444(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("AI_CHARGE_CHARGING_100", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_AI灯_充电完成125%")#AI_CHARGE_DONE_125 (触发灯效)   
    @pytest.mark.full
    def test_caseid_1985136(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("AI_CHARGE_DONE_125", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_哨兵开启")#SEQUENCE_SENTINEL_WORK(触发灯效)_marsone&venus
    @pytest.mark.sanity
    def test_caseid_1984468(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_SENTINEL_WORK", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_哨兵报警")#SEQUENCE_SENTINEL_WARINING(循环灯效)_marsone&venus
    @pytest.mark.sanity
    def test_caseid_1984469(self):
        for loop_num in [-1, 2]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_SENTINEL_WARINING", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_哨兵开启2")#SEQUENCE_SENTINEL_AFTERBYE(触发式)_marsone&venus
    @pytest.mark.full
    def test_caseid_1984470(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_SENTINEL_AFTERBYE", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_展车灯舞")#SEQUENCE_ROBODANCE(触发式)_marsone&venus
    @pytest.mark.full
    def test_caseid_1984467(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_ROBODANCE", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_解锁迎宾灯效")#SEQUENCE_HELLO_UNLOCK(触发式)_marsone&venus
    @pytest.mark.full
    def test_caseid_1984466(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_HELLO_UNLOCK", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_展车欢迎")#SEQUENCE_HELLO_EXHIBITION(触发式)_marsone&venus
    @pytest.mark.sanity
    def test_caseid_1983346(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_HELLO_EXHIBITION", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_车外迎宾")#SEQUENCE_HELLO_APPROACH(循环灯效)_marsone&venus
    @pytest.mark.sanity
    def test_caseid_1984465(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_HELLO_APPROACH", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_灯舞B")#SEQUENCE_DANCE_B(触发式)_marsone&venus
    @pytest.mark.full
    def test_caseid_1984464(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_DANCE_B", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_灯舞A")#SEQUENCE_DANCE_A(触发式)_marsone&venus
    @pytest.mark.full
    def test_caseid_1984463(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_DANCE_A", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_充电中2")#SEQUENCE_CHARGE_CHARGINGSTART(循环灯效)
    @pytest.mark.full
    def test_caseid_1984462(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_CHARGE_CHARGINGSTART", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_充电中1")#SEQUENCE_CHARGE_CHARGING(循环灯效)
    @pytest.mark.full
    def test_caseid_1984461(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_CHARGE_CHARGING", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_闭锁")#SEQUENCE_BYE_LOCK(触发式)
    @pytest.mark.full
    def test_caseid_1984458(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_BYE_LOCK", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_低速无人泊车停止")#SEQUENCE_AVP_STOP(触发式)
    @pytest.mark.full
    def test_caseid_1984457(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_AVP_STOP", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_低速无人泊车开启")#SEQUENCE_AVP_P(触发式)
    @pytest.mark.sanity
    def test_caseid_1984456(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_AVP_P", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_车外语音唤醒等待")#SEQUENCE_AICOMMUNICATION_WAKEUPWAIT(触发灯效)
    @pytest.mark.full
    def test_caseid_1984454(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_AICOMMUNICATION_WAKEUPWAIT", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_车外语音唤醒")#SEQUENCE_AICOMMUNICATION_WAITING(触发式)
    @pytest.mark.smoke
    def test_caseid_1984453(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_AICOMMUNICATION_WAITING", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_车外语音识别处理")#SEQUENCE_AICOMMUNICATION_THINK(触发式)
    @pytest.mark.full
    def test_caseid_1984448(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_AICOMMUNICATION_THINK", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_车外语音游离(待命)")#SEQUENCE_AICOMMUNICATION_STANDBY(循环灯效)
    @pytest.mark.full
    def test_caseid_1984446(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_AICOMMUNICATION_STANDBY", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_车外语音聆听")#SEQUENCE_AICOMMUNICATION_LISTEN(持续式)
    @pytest.mark.sanity
    def test_caseid_1984447(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_AICOMMUNICATION_LISTEN", True, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_车外语音执行")#SEQUENCE_AICOMMUNICATION_BROCAST_OK(触发式)
    @pytest.mark.full
    def test_caseid_1984445(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_AICOMMUNICATION_BROCAST_OK", False, loop_num)
    
    @allure.title("控制预制灯光秀(外灯)&获取灯光秀播放状态&通知灯光秀播放状态_车外语音执行")#SEQUENCE_AICOMMUNICATION_BROCAST_ERR(循环灯效)
    @pytest.mark.full
    def test_caseid_1984427(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_AICOMMUNICATION_BROCAST_ERR", True, loop_num)
    
    @allure.title("外灯灯光秀_SEQUENCE_CHARGING_100")
    @pytest.mark.full
    def test_caseid_1985245(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_CHARGING_100", True, loop_num)

    @allure.title("外灯灯光秀_SEQUENCE_CHARGING_25")
    @pytest.mark.full
    def test_caseid_1989555(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_CHARGING_25", True, loop_num)    

    @allure.title("外灯灯光秀_SEQUENCE_CHARGING_50")
    @pytest.mark.full
    def test_caseid_1989556(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_CHARGING_50", True, loop_num)    

    @allure.title("外灯灯光秀_SEQUENCE_CHARGING_75")
    @pytest.mark.full
    def test_caseid_1989557(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_CHARGING_75", True, loop_num)    

    @allure.title("外灯灯光秀_SEQUENCE_DISCHARGING_100")
    @pytest.mark.full
    def test_caseid_1989558(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_DISCHARGING_100", True, loop_num)         
    
    @allure.title("外灯灯光秀_SEQUENCE_CHARGING_COMPLETE_100")
    @pytest.mark.sanity
    def test_caseid_1985253(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_CHARGING_COMPLETE_100", False, loop_num)
    
    @allure.title("外灯灯光秀_SEQUENCE_CHARGING_ERROR")
    @pytest.mark.sanity
    def test_caseid_1985254(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_CHARGING_ERROR", True, loop_num)
    
    @allure.title("外灯灯光秀_SEQUENCE_CHARGING_INSERT_100")
    @pytest.mark.full
    def test_caseid_1985256(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_CHARGING_INSERT_100", False, loop_num)

    @allure.title("外灯灯光秀_SEQUENCE_CHARGING_BOOKING_100") # Venus
    @pytest.mark.sanity
    def test_caseid_1985250(self):
        for loop_num in [-1, 1]:
            logger.info(f"loop_num={loop_num}")
            self.external_light_show_test("SEQUENCE_CHARGING_BOOKING_100", False, loop_num)

    @allure.title("Venus切换到非P档_非HPI灯停止播放") # Venus
    @pytest.mark.full
    def test_caseid_1989651(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.sd_tester.change_usage_mode(13)
        sleep(1)
        json_name = "SEQUENCE_CHARGING_BOOKING_100"
        id_values_map = self.ls.pre_handle_external_light_show_json(f"{json_name}.json")
        logger.info(f"[id_values_map]:{id_values_map}")
        frames = len(self.ls.json_array)  # 帧数
        logger.info(f"[frames_number]:{frames}")
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl",{"seqId": json_name, "act": 1})  # stop
        sleep(1)
        
        for gear in ["GearN", "GearD", "GearR"]:
            self.set_gear('GearP')
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl", {"seqId": json_name, "act": 0})  # start
            sleep(0.02 * frames // 2)
            self.set_gear(gear)
            logger.info(f"[gear]:switch to {gear}")
            sleep(0.02 * frames)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=3)
            
            for beadid, exp_values in id_values_map.items():
                signal = self.ls.id2signal_map[beadid]
                items = self.bgm_eth_inter.get_signal_items(signal)
                # 检查最后两帧应该为0
                assert items[-1][2] == 0 and items[-2][2] == 0, "切换到非P档后，非HPI灯最后两帧应该为0"
                exp_loop_num = -1
                self.ls.ck_external_signal_values(beadid, signal, items[:-2], exp_values, exp_loop_num, ck_last_three_frame=False)
            
    @allure.title("Mars1切换到非P档_轮眉灯停止播放") # Mars1
    @pytest.mark.full
    def test_caseid_1989652(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_usage_mode(13)
        sleep(1)
        json_name = "WHEEL_AICOMMUNICATION_LISTEN"
        id_values_map = self.ls.pre_handle_external_light_show_json(f"{json_name}.json")
        logger.info(f"[id_values_map]:{id_values_map}")
        frames = len(self.ls.json_array)  # 帧数
        logger.info(f"[frames_number]:{frames}")
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl",{"seqId": json_name, "act": 1})  # stop
        sleep(1)
        
        for gear in ["GearN", "GearD", "GearR"]:
            self.set_gear('GearP')
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl", {"seqId": json_name, "act": 0})  # start
            sleep(0.02 * frames // 2)
            self.set_gear(gear)
            logger.info(f"[gear]:switch to {gear}")
            sleep(0.02 * frames)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=3)
            
            for beadid, exp_values in id_values_map.items():
                signal = self.ls.id2signal_map[beadid]
                items = self.bgm_eth_inter.get_signal_items(signal)
                # 检查最后六帧应该为0
                for i in range(-6, 0):
                    assert items[i][2] == 0, "切换到非P档后，轮眉灯最后六帧应该为0"
                exp_loop_num = -1
                self.ls.ck_external_signal_values(beadid, signal, items[:-6], exp_values, exp_loop_num, ck_last_three_frame=False)
            
    @allure.title("Mars1切换到非P档_非HPI灯停止播放") # Mars1
    @pytest.mark.full
    def test_caseid_1989653(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_usage_mode(13)
        sleep(1)
        json_name = "SEQUENCE_CHARGING_100"
        id_values_map = self.ls.pre_handle_external_light_show_json(f"{json_name}.json")
        logger.info(f"[id_values_map]:{id_values_map}")
        frames = len(self.ls.json_array)  # 帧数
        logger.info(f"[frames_number]:{frames}")
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl",{"seqId": json_name, "act": 1})  # stop
        sleep(1)
        
        for gear in ["GearN", "GearD", "GearR"]:
            self.set_gear('GearP')
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl", {"seqId": json_name, "act": 0})  # start
            sleep(0.02 * frames // 2)
            self.set_gear(gear)
            logger.info(f"[gear]:switch to {gear}")
            sleep(0.02 * frames)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=3)
            
            for beadid, exp_values in id_values_map.items():
                signal = self.ls.id2signal_map[beadid]
                items = self.bgm_eth_inter.get_signal_items(signal)
                # 检查最后两帧应该为0
                assert items[-1][2] == 0 and items[-2][2] == 0, "切换到非P档后，非HPI灯最后两帧应该为0"
                exp_loop_num = -1
                self.ls.ck_external_signal_values(beadid, signal, items[:-2], exp_values, exp_loop_num, ck_last_three_frame=False)
            
    def ipdu_check_signals(self, json_name): 
        self.pdu2obj = {5311:self.ipdu.cem_lin2.CemCem_Lin2Fr07,
                        5312:self.ipdu.cem_lin2.CemCem_Lin2Fr08,
                        5314:self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr04,
                        5315:self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr06,
                        5316:self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr02,
                        5317:self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr03, 
                        5318:self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr04, 
                        5319:self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr08, 
                        5320:self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr10, 
                        5321:self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr02,}
                
        id_values_map = self.ls.pre_handle_external_light_show_json(f"{json_name}.json")
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl", {"seqId": json_name, "act": 1},  timeout=0.5)  # stop
        self.partner.empty_all(0.5)
        
        #  按json中的第0帧获取到所有要检查的信号[('self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr10', 'PIXReRiX9Y5', 60)...]
        multi_signals = [[i[0], i[1], 0] for i in list(self.ls.id2signal_map.items()) if i[0] is not None]
        for index, value in enumerate(multi_signals):
            if value[1][:9] in ['PIXFrntRi']:
                value[0] = self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr07
            elif value[1][:10] in ['CrossReMid']:
                value[0] = self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr05
            elif value[1][:9] in ['PIXReLeXC', 'PIXReLeXD', 'PIXReLeXE', 'PIXReLeXF', 
                                  'PIXReRiXA', 'PIXReRiXB', 'PIXReRiXC', 'PIXReRiXD', 'PIXReRiXE', 'PIXReRiXF']:
                value[0] = self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr09
            elif value[1][:7] in ['PIXReRi']:
                value[0] = self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr10
            else:
                value[0] = self.pdu2obj[self.ls.id2pdu_map[value[0]]]
        for index, value in enumerate(list(id_values_map.values())):
            multi_signals[index][2] = value[0]
        for index, value in enumerate(multi_signals):
            multi_signals[index] = tuple(value)
            logger.info(f"multi_signals:{multi_signals[index]}")

        # 按ipdu区分
        check_signals = {}
        for sig_info in multi_signals:
            obj = sig_info[0]
            if obj not in check_signals:
                check_signals[obj] = [sig_info]
            else:
                check_signals[obj].append(sig_info)
        check_lists = list(check_signals.values())

        #检查信号
        for signals in check_lists:
            logger.info(f"check signals:{signals}")
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl", {"seqId": json_name, "act": 0}, timeout=0.5)  # start
            self.ipdu.check_multiple_signals(signals, timeout=0.5) 
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl", {"seqId": json_name, "act": 1}, timeout=0.5)

        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SequenceControl", {"seqId": json_name, "act": 1},  timeout=0.5)
        self.partner.empty_all()
    
    @allure.title("设置外灯灯光秀像素_信号路由检查_WHEEL灯")
    @pytest.mark.full
    def test_caseid_1988774(self):
        self.ipdu_check_signals('WHEEL_AICOMMUNICATION_STANDBY')

    @allure.title("设置外灯灯光秀像素_信号路由检查_SEQUENCE灯")
    @pytest.mark.full
    def test_caseid_1988775(self):
        self.ipdu_check_signals('SEQUENCE_AVP_P') 
        
    @allure.title("设置外灯灯光秀像素_信号路由检查_AI灯")
    @pytest.mark.full
    def test_caseid_1988776(self):
        self.ipdu_check_signals('AI_CHARGE_DONE_100')  
        
        
if __name__ == "__main__":
    ls = LightShowTest(vehicle_type='mars1')
    print(ls.pre_handle_external_light_show_json("SEQUENCE_CHARGING_100.json"))