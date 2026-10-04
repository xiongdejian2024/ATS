# -*- coding: utf-8 -*-
"""
@File        : test_LightShowService_Internal.py
@Author      : chi.han@jiduatuo.com
@Time        : 2024/08/07 15:00 PM
@Description : Test s2s interface about InternalLightShow
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
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.common.logger import logger


def is_invalid_frame(frame):
    """
    判断当前帧是否为无效帧(当前帧只包含一个id为-1的灯)
    @param frame: 当前帧
    return: True表示当前帧为无效帧，False表示当前帧为有效帧
    """
    if len(frame) == 1 and frame[0]['id'] == -1:
        return True
    return False


class InterLightShow():

    def __init__(self, vehicle_type):
        veh_map = {"mars1": "marsone", 
                   "venus": "venus"}
        self.json_path = os.path.join(os.getcwd(), 
                                      f"case_helper/config/{veh_map.get(vehicle_type, 'marsone')}_json")
        self.db_file_path = os.path.join(os.getcwd(), f"case_helper/config/LightShowSignalDB.xlsx")

        self.json_array = []
        self.id2signal_map = {}  # {0：[OrdinaryAmbientLightTweeterLeftBrightness...], ...}
        self.pdu2id_map = {}     # {6252: [0, 1, 2, 3, 4...], 6251: [8, 9, 10, 11...]}
        self.id2pdu_map = {}     # {0: [6252], 1: [6252], ...}
        self.odd_loop = False    # json文件是否为循环帧且帧总数为奇数帧

        if vehicle_type == 'venus':
            self.id_total = 214
        else:
            self.id_total = 215  # 0~214

    def load_light_show_json(self, json_name: str):
        """读取灯光秀json文件"""
        with open(os.path.join(self.json_path, json_name)) as file:
            data = json.load(file)
        return data['arry']

    def parse_interlight_db(self):
        """
        解析LightShowSignalDB.xlsx文件中内灯氛围灯信息
        Returns: tuple: 包含三个字典，分别对应id到信号的映射、pdu到id的映射和id到pdu的映射
        """
        sheet_name = 'Internal' 

        mywb = openpyxl.load_workbook(self.db_file_path)
        mysheet = mywb[sheet_name]                  
            
        for i in range(2, mysheet.max_row+1):           
            id = mysheet.cell(i, 1).value               
            signal = mysheet.cell(i, 2).value           
            pdu = mysheet.cell(i, 3).value

            self.id2signal_map[id] = [i for i in signal.split('\n')]          
            self.id2pdu_map[id] = pdu                
            if pdu not in self.pdu2id_map:
                self.pdu2id_map[pdu] = [id]
            else:
                self.pdu2id_map[pdu].append(id)
                
        return self.id2signal_map, self.pdu2id_map, self.id2pdu_map

    def fill_values(self, id_value_map, value):
        """
        将指定的值填充到给定的id_value_map字典中每个id对应的列表中，
        每个id对应四个列表，分别为对应[BRIGHTNESS]，[RED]，[GREEN]，[BLUE]
        """
        for id_val in id_value_map:
            for i in range(4):
                id_value_map[id_val][i].append(value)
    
    def get_id_value_by_json(self, json_name, is_loop=False):
        """
        根据内灯json文件解析出预取发送帧中包含的id、亮度色彩值和次数，跳过的帧以None填充
        {id：[[BRIGHTNESS]，[RED]，[GREEN]，[BLUE]]} （每个list中的个数即为次数）, 如：
        {11：[[0,0,0...]，[100,100,100...]，[50,50,50...]，[255,255,255...]], 
         13：[[0,0,0...]，[100,100,100...]，[50,50,50...]，[255,255,255...]]]
        @param json_name: 内灯氛围灯的JSON文件名，带后缀。        
        return: id到亮度色彩值列表的映射。   
        """
        self.json_array = self.load_light_show_json(json_name)
        
        # OVERLAY循环灯效且帧总数为偶数时，第二次播放会错位需要特殊处理
        if is_loop and len(self.json_array) % 2 == 0 and json_name.startswith('OVERLAY'):
            self.json_array.append(self.json_array[-1])

        # 如果灯效为循环帧且帧总数为奇数, 则特殊处理：json文件内容乘以2
        if is_loop and len(self.json_array) % 2 == 1:
            self.odd_loop = True
            self.json_array = self.json_array * 2
        
        if is_invalid_frame(self.json_array[0]): 
            # 第0帧无效帧，所有灯id发0
            id_value_map = {i: [[], [], [], []] for i in range(self.id_total)}
            self.fill_values(id_value_map, 0)
        else:
            # 第0帧为有效帧时, 如果BRIGHTNESS为-1则替换为255, RED GREEN BLUE为-1则替换为0
            for i in self.json_array[0]:
                i['BRIGHTNESS'] = 255 if i['BRIGHTNESS'] == -1 else i['BRIGHTNESS']
                i['RED'] = 0 if i['RED'] == -1 else i['RED']
                i['GREEN'] = 0 if i['GREEN'] == -1 else i['GREEN']
                i['BLUE'] = 0 if i['BLUE'] == -1 else i['BLUE']
            # 第0帧包含所有灯id
            id_value_map = {i["id"]: [[i["BRIGHTNESS"]], 
                                      [i["RED"]], 
                                      [i["GREEN"]], 
                                      [i["BLUE"]]] for i in self.json_array[0]} 

        pre_valid_frame = []
        # 循环每一帧：智能氛围灯偶发奇不发，但无论奇/偶帧，从有效值变到无效值时，都自动补发一帧
        for index, frame in enumerate(self.json_array):
            # 当前是第0帧，则跳过
            if index == 0:
                pre_valid_frame = frame
                continue
            # 当前是无效帧，前一帧也是无效帧则跳过 
            pre_frame = self.json_array[index-1]    
            if is_invalid_frame(frame) and is_invalid_frame(pre_frame): 
                self.fill_values(id_value_map, None)
                logger.info(f"0: skip index {index}")
                continue
            # 最后一帧无效帧，非循环灯效且非OVERLAY文件则跳过
            if index == len(self.json_array) - 1 and is_invalid_frame(frame):  
                if not (is_loop or json_name.startswith('OVERLAY')):
                    self.fill_values(id_value_map, None)
                    logger.info(f"1: skip index {index}")
                    continue   
            # 奇数帧并且是有效帧，则跳过，但帧中的灯信息需要保存，下一帧发送
            if index % 2 == 1 and not is_invalid_frame(frame) :
                pre_valid_frame = frame
                self.fill_values(id_value_map, None)
                logger.info(f"2: skip index {index}")
                continue
                                           
            update_cur_ids = set()
            # 处理帧数据 ：1.偶数帧为有效帧，2.当前帧为无效帧并且前一帧为有效帧 
            # 找出在前一帧中的但没有在当前帧中的值
            val_in_pre_not_cur = []
            if pre_valid_frame:
                for i in pre_valid_frame:
                    found = False
                    if self.id2pdu_map[i['id']] == 6252:
                        if not is_invalid_frame(frame): # 当前有效帧不补发上一帧的普通氛围灯
                            continue
                    for j in frame:
                        if i['id'] == j['id']:
                            found = True
                    if not found:
                        val_in_pre_not_cur.append(i)    
            pre_valid_frame = []  
                                                    
            # 更新当前帧中灯的值，和在前一帧中的没有在当前帧中的值              
            for light in frame + val_in_pre_not_cur: 
                light_id = light["id"] 
                if light_id in id_value_map:
                    id_value_map[light_id][0].append(light['BRIGHTNESS'])
                    id_value_map[light_id][1].append(light['RED'])
                    id_value_map[light_id][2].append(light['GREEN'])
                    id_value_map[light_id][3].append(light['BLUE'])
                update_cur_ids.add(light_id)
            
            # 当前帧中不需要变化的灯保持上一帧的值
            for id_val in id_value_map:
                # 其他智能氛围灯填充非None值，其他普通氛围灯在无效帧时填充非None值
                if (self.id2pdu_map[id_val] == 6251 and id_val not in update_cur_ids) or \
                    (is_invalid_frame(frame) and self.id2pdu_map[id_val] == 6252 and id_val not in update_cur_ids):
                    # 上一帧数据最后一个非None值
                    last_values = [[j for j in id_value_map[id_val][i] if j is not None][-1] for i in range(4)]
                    for j in range(4):
                        id_value_map[id_val][j].append(last_values[j])
                # 其他普通氛围灯在有效帧时填充None
                elif not is_invalid_frame(frame) and self.id2pdu_map[id_val] == 6252 and id_val not in update_cur_ids: 
                    for j in range(4):
                        id_value_map[id_val][j].append(None)

        # OVERLAY文件恢复底色，补一帧0
        if json_name.startswith('OVERLAY'):
            self.fill_values(id_value_map, 0)
        
        # 最后一帧为全灭，补一帧0
        # self.fill_values(id_value_map, 0)
        return id_value_map        

    def check_signal_value_and_period(self, json_name, id, signal, act_values, exp_values, loop=1, period=0.02, deviation=0.01):
        """
        校验内灯灯光秀实际下行数据是否与预期一致
        @param act_values: 实际下行数据 [(pcap_index, timestamp, signal_value), (), ()...]
        @param exp_values: 预期数据列表
        @param loop: 循环次数
        @param period: 预期周期
        @param deviation: 帧间隔允许的时间偏差 0.01s        
        return：bool, 如果校验通过返回True，否则触发断言失败。
        """        
        pos = -1
        pre_period = 0        
        
        if loop > 1 and (not self.odd_loop): # 循环灯效(总数非奇数帧)时预期为预期值乘以循环次数
            exp_values =  exp_values * loop 
        # logger.info(f"[id:{id}][signal:{signal}][loop:{loop}] expect values:{exp_values}")

        # 检查最后一帧（补0帧）
        # AMBIENT_SINGLE系列和AMBIENT_MUTI系列灯效，收到act==kSequenceStop时保持最后一帧灯效；其他AMBIENT灯效，在收到act==SequenceStop时，会将氛围灯熄灭。
        if not ('AMBIENT_MUTI' in json_name or 'AMBIENT_SINGLE' in json_name):
            assert act_values[-1][2] == 0, \
            f"[id:{id}][signal:{signal}][loop:{loop}]最后一帧值为{act_values[-1][2]}, 与预期 0 不符"
            exp_values.append(0)
        
        # 检查帧的个数与预期是否一致 
        act_num = len(act_values) 
        exp_num = len([i for i in exp_values if i is not None]) 
        if loop == 1 or (loop == 2 and act_num in [2, 3] and not self.odd_loop):
            assert act_num == exp_num, \
            f"[id:{id}][signal:{signal}][loop:{loop}]有效帧个数为{act_num}, 与预期{exp_num}帧不符"
        # 未播放一轮存在发前1~3帧，最后补0的情况，总数奇数帧的循环灯效存在未播放两轮共发了4帧，最后补0的情况
        elif (loop == -1 and exp_num <= 4) or (loop == 2 and self.odd_loop and act_num <=5): 
            assert act_num <= exp_num, \
            f"[id:{id}][signal:{signal}][loop:{loop}]有效帧个数为{act_num}, 与预期{exp_num}帧不符"
        else:
            assert act_num < exp_num, \
            f"[id:{id}][signal:{signal}][loop:{loop}]有效帧个数为{act_num}, 循环灯效预期应该小于{exp_num}帧" 
        
        # 检查信号的值和帧周期                 
        for index, exp_value in enumerate(exp_values[:-1]):
            # 如果值为None，代表此帧跳过，下一帧的时间间隔需加上一个周期
            if exp_value is None: 
                pre_period += period
                continue
            else:
                exp_period = pre_period + period
                pre_period = 0
                pos += 1

            # 检查完倒数第二帧后跳出循环
            if pos > len(act_values) - 1 - 1:
                break
            
            pcap_index, timestamp, act_value = act_values[pos]
            
            # 检查信号的值是否正确
            if 'Brightness' in signal: # Brightness信号值占7位
                exp_value &= 0x7f
            assert act_value == exp_value, \
            f"[id:{id}][signal:{signal}][loop:{loop}][json_index:{index}][pcap_index:{pcap_index}]:值为{act_value}, 与预期{exp_value}不符" 
            
            # 从第一帧开始检查当前帧的周期(预期为20ms,误差为10ms,预期超过20ms,误差为25ms)
            if index in [0]: 
                continue
            interval = float(timestamp) - float(act_values[pos-1][1])
            deviation = deviation if exp_period == period else 0.25
            assert abs(float(interval) - exp_period) < deviation , \
            f"[id:{id}][signal:{signal}][loop:{loop}][json_index:{index}][pcap_index:{pcap_index}]:时间搓为{timestamp}, 与上一帧的间隔为{interval}，与预期{exp_period}偏差过大"  
            
        return True

@allure.feature("SOA服务接口")
@allure.story("整车控制/LightShowInternalService")
@pytest.mark.ils
class TestLightShowInternalService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        partner_process_check()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.vehicle_type = ecu.tc_config['veh_type']#修改车辆配置
        # self.vehicle_type = "mars1"#强行改车辆配置
        self.ils = InterLightShow(self.vehicle_type)

        logger.info(f"车辆配置为{self.vehicle_type}")
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
        # 检查上位机上是否有其它未关闭的soa_partner进程在运行，如果有，则杀死进程
        # 测试灯关秀的前提，非P挡，诊断激活线断开
        
        # 解析内灯灯光秀的db文件
        self.ils.parse_interlight_db()

    def before_each_func(self, ecu):
        self.sd_tester.tester_present()
        self.nucapp.bgm_diag_line_down()#诊断激活线断开
        # self.set_gear("GearN")
        # self.set_gear("GearP")
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 35, "inhibitSts": False}]})#普通氛围灯不禁用
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 25, "inhibitSts": False}]})#智能氛围灯不禁用
        # self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 0} , timeout=0.5) #外灯模式关闭
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                            {"lights": [{"light": {"type": 33, "zoneId": 12}, "mode": 0,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}]}, timeout=0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                            {"lights": [{"light": {"type": 33, "zoneId": 13}, "mode": 0,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}]}, timeout=0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                            {"lights": [{"light": {"type": 33, "zoneId": 14}, "mode": 0,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}]}, timeout=0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT,"LightControl",
                {"lights": [{ "light": {"type": 25, "zoneId": 0},"mode": 0,}]}, timeout=0.5)#智能氛围灯
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT,"LightControl",
                {"lights": [{ "light": {"type": 35, "zoneId": 0},"mode": 0,}]}, timeout=0.5)#普通氛围灯
        self.partner.empty_all()
        self.ils.odd_loop = False
        super().before_each_func(ecu, start=False)
        
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
        sleep(1)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetGear", {}, {"out": map[gear]}, timeout=1.5)

    def internal_light_show_test(self, json_name, is_loop = False, loop_num: int = 1):
        """
        处理数据并抓包校验内灯灯光秀，并校验下行pdu是否与预期一致
        @param json_name: 灯光秀json文件名
        @param is_loop: 是否循环播放
        @param loop_num: 循环次数，默认1：一次完整播放，-1：小于一次循环，2：超过1次，不到2次
        """
        id_values_map = self.ils.get_id_value_by_json(f"{json_name}.json", is_loop)
        
        frame_num = int(len(self.ils.json_array)/2) if self.ils.odd_loop else len(self.ils.json_array) # 帧数
        logger.info(f"[json_name：{json_name}.json][is_loop:{is_loop}][odd:{self.ils.odd_loop}]总共帧数：{frame_num}")
        
        json_name = json_name + '_L100' if 'AMBIENT_MUTI' in json_name or 'AMBIENT_SINGLE' in json_name else json_name
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "InteriorLampSequenceControl",
                                         {"seqId": json_name, "act": 1}, timeout=0.5)  # stop
        sleep(1)        
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "InteriorLampSequenceControl", 
                                         {"seqId": json_name, "act": 0}, timeout=0.5)  # start
        if loop_num == -1:
            sleep(0.02 * frame_num * 0.2)
        elif loop_num == 1:  
            sleep(0.02 * frame_num + 1)
        elif loop_num == 2:
            sleep(0.02 * frame_num * 1.2)
        else:
            assert False, f"loop_num={loop_num}不合法"

        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "InteriorLampSequenceControl", 
                                         {"seqId": json_name, "act": 1}, timeout=0.5)  # stop
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=3) # 给足补0的时间
        
        for id, exp_values in id_values_map.items():
            for index, signal in enumerate(self.ils.id2signal_map[id]):
                logger.info(f"[id:{id}][index:{index}][signal:{signal}][loop:{loop_num}][odd:{self.ils.odd_loop}]Expect:{exp_values[index]}")
                
                act_values = self.bgm_eth_inter.get_signal_items(signal)
                if not is_loop and loop_num != -1:
                    exp_loop = 1   # 非循环播放灯效，即使播放时间超过1次，也只会有一次循环
                elif is_loop and loop_num == 1:
                    exp_loop = 2   # 循环播放灯效，如果播放时间超过1次，则至少会播放超过1次
                else:
                    exp_loop = loop_num
                    
                self.ils.check_signal_value_and_period(json_name, id, signal, act_values, exp_values[index], exp_loop)
                logger.info(f"[id:{id}][index:{index}][signal:{signal}] check pass.")

    @allure.title("内灯氛围灯_AMBIENT_CAR_CountDown")
    @pytest.mark.smoke
    def test_caseid_1984358(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_CAR_CountDown", False, i)
        
    @allure.title("内灯氛围灯_AMBIENT_CAR_DEFAULT")
    @pytest.mark.sanity
    def test_caseid_1984471(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_CAR_DEFAULT", False, i)

    @allure.title("内灯氛围灯_AMBIENT_CAR_EnterTrack")
    @pytest.mark.full
    def test_caseid_1984357(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_CAR_EnterTrack", False, i)

    @allure.title("内灯氛围灯_AMBIENT_CAR_ExitTrack")
    @pytest.mark.sanity
    def test_caseid_1984360(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_CAR_ExitTrack", False, i)
                   
    @allure.title("内灯氛围灯_AMBIENT_CAR_LOADING")
    @pytest.mark.sanity
    def test_caseid_1984354(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_CAR_LOADING", True, i)

    @allure.title("内灯氛围灯_AMBIENT_HAPPY_DEFAULT")
    @pytest.mark.full
    def test_caseid_1984472(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_HAPPY_DEFAULT", False, i)
        
    @allure.title("内灯氛围灯_AMBIENT_HAPPY_EXIT")
    @pytest.mark.full
    def test_caseid_1984473(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_HAPPY_EXIT", False, i)
        
    @allure.title("内灯氛围灯_AMBIENT_HAPPY_LOADING")
    @pytest.mark.sanity
    def test_caseid_1984474(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_HAPPY_LOADING", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_HAPPY_LOSE")
    @pytest.mark.full
    def test_caseid_1984475(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_HAPPY_LOSE", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_HAPPY_START")
    @pytest.mark.full
    def test_caseid_1984476(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_HAPPY_START", False, i)

    @allure.title("内灯氛围灯_AMBIENT_HAPPY_WIN")
    @pytest.mark.sanity
    def test_caseid_1984477(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_HAPPY_WIN", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_HELLO_COLDBOOT")
    @pytest.mark.full
    def test_caseid_1984348(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_HELLO_COLDBOOT", False, i)

    @allure.title("内灯氛围灯_AMBIENT_HELLO_WARMBOOTSTART")
    @pytest.mark.smoke
    def test_caseid_1984349(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")        
            self.internal_light_show_test("AMBIENT_HELLO_WARMBOOTSTART", True, i)

    @allure.title("内灯氛围灯_AMBIENT_HELLO_WARMBOOTSEATOCCUPIED")
    @pytest.mark.sanity
    def test_caseid_1984350(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_HELLO_WARMBOOTSEATOCCUPIED", False, i)

    @allure.title("内灯氛围灯_AMBIENT_HERO_BOSS")
    @pytest.mark.smoke
    def test_caseid_1984479(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_HERO_BOSS", True, i)

    @allure.title("内灯氛围灯_AMBIENT_HERO_DEFAULT")
    @pytest.mark.full
    def test_caseid_1984480(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_HERO_DEFAULT", False, i)
        
    @allure.title("内灯氛围灯_AMBIENT_HERO_EXIT")
    @pytest.mark.sanity
    def test_caseid_1984481(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_HERO_EXIT", False, i)
        
    @allure.title("内灯氛围灯_AMBIENT_HERO_LOADING")
    @pytest.mark.full
    def test_caseid_1984482(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_HERO_LOADING", True, i)

    @allure.title("内灯氛围灯_AMBIENT_MISSION_LOADING")
    @pytest.mark.full
    def test_caseid_1984485(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MISSION_LOADING", True, i)

    @allure.title("内灯氛围灯_AMBIENT_MISSION_DEFAULT")
    @pytest.mark.full
    def test_caseid_1984361(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MISSION_DEFAULT", False, i)

    @allure.title("内灯氛围灯_AMBIENT_MISSION_Enter")
    @pytest.mark.full
    def test_caseid_1984483(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MISSION_Enter", False, i)

    @allure.title("内灯氛围灯_AMBIENT_MISSION_Exit")
    @pytest.mark.sanity
    def test_caseid_1984484(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MISSION_Exit", False, i)

    @allure.title("内灯氛围灯_AMBIENT_SINGLE_MODE1")
    @pytest.mark.full
    def test_caseid_1984478(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_SINGLE_MODE1", False, i)        

    @allure.title("内灯氛围灯_AMBIENT_SINGLE_MODE2")
    @pytest.mark.smoke
    def test_caseid_1984494(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_SINGLE_MODE2", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_SINGLE_MODE2B")
    @pytest.mark.full
    def test_caseid_1984495(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_SINGLE_MODE2B", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_SINGLE_MODE3")
    @pytest.mark.sanity
    def test_caseid_1984496(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_SINGLE_MODE3", True, i)      
            
    @allure.title("内灯氛围灯_AMBIENT_MUTI1_MODE1")
    @pytest.mark.full
    def test_caseid_1984497(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI1_MODE1", False, i)

    @allure.title("内灯氛围灯_AMBIENT_MUTI1_MODE2")
    @pytest.mark.full
    def test_caseid_1986221(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI1_MODE2", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_MUTI1_MODE2B")
    @pytest.mark.full
    def test_caseid_1984407(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI1_MODE2B", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_MUTI1_MODE4")
    @pytest.mark.full
    def test_caseid_1984419(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI1_MODE4", True, i)        
        
    @allure.title("内灯氛围灯_AMBIENT_MUTI2_MODE1")
    @pytest.mark.full
    def test_caseid_1984418(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI2_MODE1", False, i)        

    @allure.title("内灯氛围灯_AMBIENT_MUTI2_MODE2")
    @pytest.mark.sanity
    def test_caseid_1984410(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI2_MODE2", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_MUTI2_MODE2B")
    @pytest.mark.sanity
    def test_caseid_1984368(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI2_MODE2B", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_MUTI2_MODE4")
    @pytest.mark.full
    def test_caseid_1984371(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI2_MODE4", True, i)      

    @allure.title("内灯氛围灯_AMBIENT_MUTI3_MODE1")
    @pytest.mark.full
    def test_caseid_1984412(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI3_MODE1", False, i)        

    @allure.title("内灯氛围灯_AMBIENT_MUTI3_MODE2")
    @pytest.mark.full
    def test_caseid_1984409(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI3_MODE2", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_MUTI3_MODE2B")
    @pytest.mark.full
    def test_caseid_1984415(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI3_MODE2B", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_MUTI3_MODE4")
    @pytest.mark.smoke
    def test_caseid_1984372(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI3_MODE4", True, i)      

    @allure.title("内灯氛围灯_AMBIENT_MUTI4_MODE1")
    @pytest.mark.full
    def test_caseid_1984373(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI4_MODE1", False, i)        

    @allure.title("内灯氛围灯_AMBIENT_MUTI4_MODE2")
    @pytest.mark.sanity
    def test_caseid_1984413(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI4_MODE2", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_MUTI4_MODE2B")
    @pytest.mark.smoke
    def test_caseid_1984406(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI4_MODE2B", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_MUTI4_MODE4")
    @pytest.mark.sanity
    def test_caseid_1984405(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI4_MODE4", True, i)      
        
    @allure.title("内灯氛围灯_AMBIENT_MUTI5_MODE1")
    @pytest.mark.sanity
    def test_caseid_1984417(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI5_MODE1", False, i)        

    @allure.title("内灯氛围灯_AMBIENT_MUTI5_MODE2")
    @pytest.mark.full
    def test_caseid_1984404(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI5_MODE2", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_MUTI5_MODE2B")
    @pytest.mark.full
    def test_caseid_1984403(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI5_MODE2B", True, i)
        
    @allure.title("内灯氛围灯_AMBIENT_MUTI5_MODE4")
    @pytest.mark.full
    def test_caseid_1984414(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_MUTI5_MODE4", True, i)      

    @allure.title("内灯氛围灯_AMBIENT_SENTINEL_ALERT")
    @pytest.mark.sanity
    def test_caseid_1984344(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_SENTINEL_ALERT", True, i)      
            
    @allure.title("内灯氛围灯_AMBIENT_SENTINEL_CAUTION")
    @pytest.mark.full
    def test_caseid_1984493(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_SENTINEL_CAUTION", False, i)      

    @allure.title("内灯氛围灯_AMBIENT_SENTINEL_ALARM")
    @pytest.mark.full
    def test_caseid_1984363(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_SENTINEL_ALARM", False, i)           
        
    @allure.title("内灯氛围灯_AMBIENT_PARKOUR_LOADING")
    @pytest.mark.smoke
    def test_caseid_1984488(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_PARKOUR_LOADING", True, i)      
            
    @allure.title("内灯氛围灯_AMBIENT_PARKOUR_DEFAULT")
    @pytest.mark.full
    def test_caseid_1984486(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_PARKOUR_DEFAULT", False, i)      

    @allure.title("内灯氛围灯_AMBIENT_PARKOUR_START")
    @pytest.mark.full
    def test_caseid_1984489(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_PARKOUR_START", False, i)                   
 
    @allure.title("内灯氛围灯_AMBIENT_PARKOUR_EXIT")
    @pytest.mark.full
    def test_caseid_1984487(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_PARKOUR_EXIT", False, i)         
        
    @allure.title("内灯氛围灯_AMBIENT_PARTY_DEFAULT")
    @pytest.mark.sanity
    def test_caseid_1984490(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_PARTY_DEFAULT", True, i)     

    @allure.title("内灯氛围灯_AMBIENT_PARTY_ENTER")
    @pytest.mark.full
    def test_caseid_1984491(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_PARTY_ENTER", False, i)                   
 
    @allure.title("内灯氛围灯_AMBIENT_PARTY_EXIT")
    @pytest.mark.sanity
    def test_caseid_1984492(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_PARTY_EXIT", False, i)    
        
    @allure.title("内灯氛围灯_AMBIENT_RACEMODE_EJECT")
    @pytest.mark.sanity
    def test_caseid_1984362(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_RACEMODE_EJECT", True, i)     

    @allure.title("内灯氛围灯_AMBIENT_RACEMODE_ENTER")
    @pytest.mark.full
    def test_caseid_1988603(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_RACEMODE_ENTER", False, i)                   
 
    @allure.title("内灯氛围灯_AMBIENT_RACEMODE_EXIT")
    @pytest.mark.full
    def test_caseid_1988604(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_RACEMODE_EXIT", False, i)       
        
    # @allure.title("内灯氛围灯_OVERLAY_TWEETER_FLASH") # 此json不再使用
    # @pytest.mark.tweeter
    # def test_caseid_1984519(self):
    #     for i in [-1, 2]:
    #         logger.info(f"loop_num={i}")
    #         self.internal_light_show_test("OVERLAY_TWEETER_FLASH", True, i)     

    # @allure.title("内灯氛围灯_OVERLAY_TWEETER_OFF") # 此json不再使用
    # @pytest.mark.tweeter
    # def test_caseid_1984520(self):
    #     for i in [-1, 2]:
    #         logger.info(f"loop_num={i}")
    #         self.internal_light_show_test("OVERLAY_TWEETER_OFF", True, i)             
        
    @allure.title("内灯氛围灯_OVERLAY_IP_CAR_Nitrogen1")
    @pytest.mark.sanity
    def test_caseid_1984374(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IP_CAR_Nitrogen1", False, i)       

    @allure.title("内灯氛围灯_OVERLAY_IP_CAR_Nitrogen2")
    @pytest.mark.full
    def test_caseid_1984375(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IP_CAR_Nitrogen2", False, i)       
        
    @allure.title("内灯氛围灯_OVERLAY_IP_CAR_Nitrogen3")
    @pytest.mark.sanity
    def test_caseid_1984376(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IP_CAR_Nitrogen3", False, i)       
        
    @allure.title("内灯氛围灯_OVERLAY_IP_CAR_Nitrogen4")
    @pytest.mark.full
    def test_caseid_1984377(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IP_CAR_Nitrogen4", False, i)              

    @allure.title("内灯氛围灯_OVERLAY_IP_CAR_VehicleCrash")
    @pytest.mark.full
    def test_caseid_1984388(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IP_CAR_VehicleCrash", False, i)      

    @allure.title("内灯氛围灯_OVERLAY_IP_CAR_VehicleCrashOver")
    @pytest.mark.full
    def test_caseid_1984389(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IP_CAR_VehicleCrashOver", False, i)   

    @allure.title("内灯氛围灯_OVERLAY_IP_CAR_Success")
    @pytest.mark.full
    def test_caseid_1984395(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IP_CAR_Success", False, i)          

    @allure.title("内灯氛围灯_OVERLAY_IP_CAR_Failure")
    @pytest.mark.full
    def test_caseid_1984396(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IP_CAR_Failure", False, i)    
        
    @allure.title("内灯氛围灯_OVERLAY_IPL_CAR_Nitrogen1")
    @pytest.mark.sanity
    def test_caseid_1984378(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IPL_CAR_Nitrogen1", False, i)       

    @allure.title("内灯氛围灯_OVERLAY_IPL_CAR_Nitrogen2")
    @pytest.mark.full
    def test_caseid_1984379(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IPL_CAR_Nitrogen2", False, i)       
        
    @allure.title("内灯氛围灯_OVERLAY_IPL_CAR_Nitrogen3")
    @pytest.mark.full
    def test_caseid_1984380(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IPL_CAR_Nitrogen3", False, i)       
        
    @allure.title("内灯氛围灯_OVERLAY_IPL_CAR_Nitrogen4")
    @pytest.mark.smoke
    def test_caseid_1984381(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IPL_CAR_Nitrogen4", False, i)             

    @allure.title("内灯氛围灯_OVERLAY_IPL_CAR_VehicleCrash") # 失败
    @pytest.mark.full
    def test_caseid_1984391(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IPL_CAR_VehicleCrash", False, i)     

    @allure.title("内灯氛围灯_OVERLAY_IPL_CAR_VehicleCrashOver") # 失败
    @pytest.mark.full
    def test_caseid_1984392(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IPL_CAR_VehicleCrashOver", False, i)   
        
    @allure.title("内灯氛围灯_OVERLAY_IPR_CAR_Nitrogen1")
    @pytest.mark.sanity
    def test_caseid_1984382(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IPR_CAR_Nitrogen1", False, i)       

    @allure.title("内灯氛围灯_OVERLAY_IPR_CAR_Nitrogen2")
    @pytest.mark.full
    def test_caseid_1984384(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IPR_CAR_Nitrogen2", False, i)       
        
    @allure.title("内灯氛围灯_OVERLAY_IPR_CAR_Nitrogen3")
    @pytest.mark.full
    def test_caseid_1984385(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IPR_CAR_Nitrogen3", False, i)       
        
    @allure.title("内灯氛围灯_OVERLAY_IPR_CAR_Nitrogen4")
    @pytest.mark.full
    def test_caseid_1984387(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IPR_CAR_Nitrogen4", False, i)                   
        
    @allure.title("内灯氛围灯_OVERLAY_IPR_CAR_VehicleCrash")
    @pytest.mark.full
    def test_caseid_1984393(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IPR_CAR_VehicleCrash", False, i)                        
        
    @allure.title("内灯氛围灯_OVERLAY_IPR_CAR_VehicleCrashOver")
    @pytest.mark.full
    def test_caseid_1984394(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IPR_CAR_VehicleCrashOver", False, i)                               
        
    @allure.title("内灯氛围灯_OVERLAY_IP_MISSION_Damage")
    @pytest.mark.full
    def test_caseid_1984397(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IP_MISSION_Damage", False, i)              
        
    @allure.title("内灯氛围灯_OVERLAY_IP_MISSION_Ultimate")
    @pytest.mark.full
    def test_caseid_1984398(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IP_MISSION_Ultimate", False, i)           

    @allure.title("内灯氛围灯_OVERLAY_IP_MISSION_Success1")
    @pytest.mark.full
    def test_caseid_1984399(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IP_MISSION_Success1", False, i)           
        
    @allure.title("内灯氛围灯_OVERLAY_IP_MISSION_Success2")
    @pytest.mark.full
    def test_caseid_1984400(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IP_MISSION_Success2", False, i)           
        
    @allure.title("内灯氛围灯_OVERLAY_IP_MISSION_Success3")
    @pytest.mark.full
    def test_caseid_1984401(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IP_MISSION_Success3", False, i)           
        
    @allure.title("内灯氛围灯_OVERLAY_IP_MISSION_Failure")
    @pytest.mark.full
    def test_caseid_1984402(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_IP_MISSION_Failure", False, i)           
        
    @allure.title("内灯氛围灯_OVERLAY_HAPPY_JOKER_BOMB")
    @pytest.mark.sanity
    def test_caseid_1984500(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_HAPPY_JOKER_BOMB", False, i)           
        
    @allure.title("内灯氛围灯_OVERLAY_HAPPY_BOMB")
    @pytest.mark.sanity
    def test_caseid_1984499(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_HAPPY_BOMB", False, i)             
        
    @allure.title("内灯氛围灯_OVERLAY_HAPPY_PLANE")
    @pytest.mark.full
    def test_caseid_1984501(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_HAPPY_PLANE", False, i)        
        
    @allure.title("内灯氛围灯_OVERLAY_PARKOUR_CRASH")
    @pytest.mark.sanity
    def test_caseid_1984516(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_PARKOUR_CRASH", False, i)     

    @allure.title("内灯氛围灯_OVERLAY_PARKOUR_BEAT")
    @pytest.mark.full
    def test_caseid_1984515(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_PARKOUR_BEAT", False, i)            
        
    @allure.title("内灯氛围灯_OVERLAY_PARKOUR_FLIGHT")
    @pytest.mark.smoke
    def test_caseid_1984517(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_PARKOUR_FLIGHT", True, i)            
    
    @allure.title("内灯氛围灯_OVERLAY_PARKOUR_LOSE")
    @pytest.mark.full
    def test_caseid_1984518(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_PARKOUR_LOSE", False, i)     

    @allure.title("内灯氛围灯_OVERLAY_HERO_DIE")
    @pytest.mark.full
    def test_caseid_1984502(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_HERO_DIE", False, i)     
             
    @allure.title("内灯氛围灯_OVERLAY_HERO_DISCOVERED")
    @pytest.mark.smoke
    def test_caseid_1984503(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_HERO_DISCOVERED", False, i)     
        
    @allure.title("内灯氛围灯_OVERLAY_HERO_ENTER")
    @pytest.mark.sanity
    def test_caseid_1984504(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_HERO_ENTER", False, i)     
        
    @allure.title("内灯氛围灯_OVERLAY_HERO_MONSTER")
    @pytest.mark.full
    def test_caseid_1984505(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_HERO_MONSTER", False, i)     
        
    @allure.title("内灯氛围灯_OVERLAY_HERO_PASS")
    @pytest.mark.full
    def test_caseid_1984506(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_HERO_PASS", False, i)     
        
    @allure.title("内灯氛围灯_OVERLAY_HERO_RESCUE")
    @pytest.mark.sanity
    def test_caseid_1984507(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_HERO_RESCUE", False, i)     
        
    @allure.title("内灯氛围灯_OVERLAY_ALERT_FLDOOR")
    @pytest.mark.full
    def test_caseid_1989193(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_ALERT_FLDOOR", True, i)     

    @allure.title("内灯氛围灯_OVERLAY_ALERT_FRDOOR")
    @pytest.mark.full
    def test_caseid_1989194(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_ALERT_FRDOOR", True, i)  

    @allure.title("内灯氛围灯_OVERLAY_ALERT_RLDOOR")
    @pytest.mark.full
    def test_caseid_1989195(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_ALERT_RLDOOR", True, i)  
            
    @allure.title("内灯氛围灯_OVERLAY_ALERT_RRDOOR")
    @pytest.mark.full
    def test_caseid_1989196(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("OVERLAY_ALERT_RRDOOR", True, i)  

    @allure.title("内灯氛围灯_AMBIENT_REMOTE_LOADING")
    @pytest.mark.full
    def test_caseid_1989481(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_REMOTE_LOADING", True, i)  

    @allure.title("内灯氛围灯_AMBIENT_REMOTE_DEFAULT")
    @pytest.mark.full
    def test_caseid_1989483(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_REMOTE_DEFAULT", False, i)                  

    @allure.title("内灯氛围灯_AMBIENT_REMOTE_START")
    @pytest.mark.full
    def test_caseid_1989484(self):
        for i in [-1, 2]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_REMOTE_START", True, i)  

    @allure.title("内灯氛围灯_AMBIENT_REMOTE_NEW")
    @pytest.mark.full
    def test_caseid_1989485(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_REMOTE_NEW", False, i)  

    @allure.title("内灯氛围灯_AMBIENT_REMOTE_EXIT")
    @pytest.mark.full
    def test_caseid_1989486(self):
        for i in [-1, 1]:
            logger.info(f"loop_num={i}")
            self.internal_light_show_test("AMBIENT_REMOTE_EXIT", False, i)  
            
            
if __name__ == "__main__":
    ils = InterLightShow(vehicle_type='mars1')
    ils.parse_interlight_db()
    # print(ls.get_id_value_by_json("AMBIENT_CAR_EnterTrack.json"))    
    # print(ls.get_id_value_by_json("AMBIENT_CAR_ExitTrack.json")[10])
    exp_values = ils.get_id_value_by_json("AMBIENT_MUTI1_MODE4.json", True)[0][0]
    print(exp_values)
    print('\n')
    a = [i for i in exp_values if i is not None]
    print(len(a), a)
    # print(ils.check_signal_value_and_period('SmartAmbientLightIpLeft2Brightness',
    #                                         act_values, exp_values))