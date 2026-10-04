#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :tsp.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :云端能力模拟 实现接口
"""

from xat_ecu.api import CommonTsp


from xat_ecu import reporting as allure
from xat_ecu.legacy.common.logger import logger
from xat_ecu.api.constants.common import *
from groot2.cloud.biz.auth.auth_manager import AuthManager as Auth
import requests
import csv
import json
import re
import yaml
import time, datetime
import hashlib
from requests.exceptions import RequestException 
from xat_ecu.api.common.common import retry_on_failure
from xat_ecu.legacy import DataDev
from xat_ecu.api.constants.remote_subscribe.remote_subscribe_class import *
from onepiece.app.b_plat_cloud_config.cloud_config_fe_api import CloudConfigFeApi

class Tsp(CommonTsp):

    @retry_on_failure(max_retry_count=3)
    def trigger_vsp_fota(self, vsp_operation: VSP, task_id: int, vin: str = None):
        self.ota = self.ota_obj(task_id)
        if vin is not None:
            logger.info(f"Use Vin Entered: {vin}")
            ids = self.ota.get_sub_task_vehicles(vin=vin)['data']['list'][0]['id']
        else:
            logger.info(f"Use bench_config Vin,task_id:{task_id},vin:{self.vin}")
            response = self.ota.get_sub_task_vehicles(vin=self.vin)
            logger.info(f"get_sub_task_vehicles接口返回值：{response}")
            ids = response['data']['list'][0]['id']
        if vsp_operation.name == 'Repub':
            result = self.ota.re_deploy_vehicle_task([ids])
        elif vsp_operation.name == 'Cancel':
            result = self.ota.cancel([ids], reason="Script call")
        elif vsp_operation.name == 'Reset':
            result = self.ota.reset(ids)
        elif vsp_operation.name == 'UnFreeze':
            result = self.ota.subtask_unfreeze(ids, reason="Script call")
        else:
            logger.error(f"Not support {vsp_operation} yet")
        if result["msg"] == "success":
            logger.info(f"succeed to {vsp_operation.name} task")
            return True
        else:
            logger.info(f"fail to {vsp_operation.name} task")
            return False

    def rvs_event_check(self, block: BlockName, keys: list, target_value: Union[str,list], index: int = 0,
                        timeout: Union[int, float] = 10):
        prompt_info = f"----------> Check RVS 上报中是否有数据块{block.name},并且{keys}是否分别为{target_value}"
        self.rvs_client = self.rvs_obj()
        with allure.step(prompt_info):
            logger.info(prompt_info)
            start_time = time.time()
            while time.time() - start_time < timeout:
                event_data = self.rvs_client.get_rvs_data_from_cloud(block.value)
                value = event_data
                for k in keys:
                    value = value[k]
                    if isinstance(value, list):
                        value = value[index]

                if isinstance(target_value,list):
                    logger.info(f"RVS 上报的值为: {value}, 期望的值为: {target_value[0]},允许的误差为{target_value[1]}")
                    if float(target_value[0] - target_value[1])<= float(value) and float(target_value[0] + target_value[1]) >= float(value):
                        assert True
                        return
                else:
                    logger.info("Get the value: {0}, target value: {1}".format(value, target_value))
                    if value == target_value:
                        assert True
                        return
            assert False

    def set_bench_config(self, vid, tel):
        self.vid = vid
        self.tel = tel
        self.get_token_from_web()
        logger.info("Get bench config: vid {0}, tel {1}".format(self.vid, self.tel))

    @retry_on_failure(10,1)
    def get_token_from_web(self):
        "获取远控操作token"
        headers = {  
            "Content-Type": "application/json",  
            "client": "4"  
        }  
        data = {  
            "countryCode": "86",  
            "tel": self.tel,  
            "captcha": "6825",  
            "captchaKey": __import__("os").environ['XAT_CREDENTIAL_SCAN_D2BA9422021B076AA78B']  
        }  
        response = requests.post(self.token_url, headers=headers, json=data, timeout=5)
        if response.status_code == 200:
            logger.info(f'获取到的token： {response.json()}')
            self.token = (response.json()['data']['token'])
            self.uid = (response.json()['data']['user']['userId'])
        else:
            raise ConnectionError('获取token失败')
        return self.token
    
    def get_token(self):
        if self.token is None:
            self.get_token_from_web()
            return self.token
        else:
            return self.token
    
    @retry_on_failure(10,1)
    def cmd_to_pb(self, data):
        headers = {"Content-Type": "application/json","client": "4", "Connection":"close"}
        postdata = json.dumps(data, skipkeys=True, indent=4, separators=(',', ': '))
        logger.info(postdata)
        try:
            response = requests.post(self.pb_url, headers=headers, data=postdata,timeout=10)
            data_raw = response.text
            logger.info(data_raw)
            cmdBody = json.loads(data_raw)["data"]
            del cmdBody["json"]
            return cmdBody
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
            logger.info("cmd转PB数据异常，{}:".format(e))
            raise ConnectionError(e)
        #     time.sleep(2)
        #     response = requests.post(self.url, headers=headers, data=postdata)
        #     data_raw = response.text
        #     logger.info(data_raw)
        #     cmdBody = json.loads(data_raw)["data"]
        #     del cmdBody["json"]
        #     return cmdBody
        # except Exception as e:  
        #     logger.info("远控请求发生异常进行重试{}:".format(e))
        #     time.sleep(2)
        #     response = requests.post(self.url, headers=headers, data=postdata)
        #     data_raw = response.text
        #     logger.info(data_raw)
        #     cmdBody = json.loads(data_raw)["data"]
        #     del cmdBody["json"]
        #     return cmdBody

    def cmd_to_ready(self, data):
        token = self.get_token()
        headers = {"Content-Type": "application/json", "Authorization": token,"client": "4", "user-agent":"jiduapp/3.2.88 (Android; 12; HUAWEI; com.jiduauto.app; RTE-AL00; debugapp; 000000003b3b9f65ffffffffc6d8a9da; SFdSVEU=)", "x-jidu-servicename":"app_android", "Connection":"close"}
        postdata = json.dumps(data, skipkeys=True, indent=4, separators=(',', ': '))
        logger.info(postdata)
        response = requests.post(self.Ready_url, headers=headers, data=postdata)
        data_raw = response.text
        logger.info(data_raw)
        code = json.loads(data_raw)["code"]
        logger.info(code)
        return code

    @retry_on_failure(10,1)
    def send_rvc_cmd(self, pb_data, subscribe_flage=0):
        "下发远控指令"
        if subscribe_flage:
            url = self.Subscribe_task_url
        else:
            url = self.cmd_url
        token = self.get_token()
        logger.info("获取车云token为{}:".format(token))        
        headers = {"Content-Type": "application/json", "Authorization": token,"client": "4", "user-agent":"jiduapp/3.2.88 (Android; 12; HUAWEI; com.jiduauto.app; RTE-AL00; debugapp; 000000003b3b9f65ffffffffc6d8a9da; SFdSVEU=)", "x-jidu-servicename":"app_android", "Connection":"close"}
        # try:
        logger.info(f'pb_dataaqqqq:{pb_data}')
        resp = requests.post(url, headers=headers, data=json.dumps(pb_data), timeout=10)
        logger.info(resp.text)
        code = (resp.json()["code"])
        logger.info("获取远控指令下发车云返回code的值为{}:".format(code))
        if resp.status_code != 200:
            logger.info(f'接口调用失败，重试')
            raise ConnectionError('接口调用失败')
        if code == 10047:
            logger.info(f'token失效，重新获取token并重新下发指令')
            self.get_token_from_web()
            raise PermissionError('用户权限失效，重新登录')
        if code == 600007:
            logger.info("远控指令加锁中,等待3秒后重新下发")
            raise KeyError('远控指令加锁中,等待3秒后重新下发')
        elif code != 0:
            logger.info("指令执行失败，请稍后重试")
            raise ConnectionError('指令执行失败，请稍后重试')
            #     time.sleep(3)
        #     resp = requests.post(self.cmd_url, headers=headers, data=json.dumps(pb_data))
            #     logger.info(resp.text)
            #     code = (resp.json()["code"])
            #     if code == 600007:
            #         logger.info("远控指令加锁中,等待3秒后重新下发")
            #         time.sleep(3)
            #         resp = requests.post(self.cmd_url, headers=headers, data=json.dumps(pb_data))
            #         logger.info(resp.text)
        # except ConnectionError:
        #     logger.info("远控指令请求域名解析发生异常进行重试{}:".format(e))
        #     time.sleep(2)
        #     logger.info(f'Request failed: {e}')  
        #     resp = requests.post(self.cmd_url, headers=headers, data=json.dumps(pb_data))
        #     logger.info(resp.text)
        #     code = (resp.json()["code"])
        #     logger.info("获取远控指令下发车云返回code的值为{}:".format(code))
        # except Exception as e:  
        #     logger.info(f'Request failed: {e}')  
        #     resp = requests.post(self.cmd_url, headers=headers, data=json.dumps(pb_data))
        #     logger.info(resp.text)
        #     code = (resp.json()["code"])
        #     logger.info("获取远控指令下发车云返回code的值为{}:".format(code))
        return resp.json()

    def rvc_lock_control(self, op: int = 2):
        "远控接闭锁请求,op:1: 解锁, 2:闭锁, 3: 关门+闭锁"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 1,
            "cmdDetail": {
                "lock_control": {
                    "op": op,
                    "userId": "1254382316769029465"
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def check_rvc_lock_control(self, op: int = 2):
        "远控接闭锁请求,op:1: 解锁, 2:闭锁, 3: 关门+闭锁"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 1,
            "cmdDetail": {
                "lock_control": {
                    "op": op,
                    "userId": "1254382316769029465"
                }
            }
        }
        return self.send_rvc_cmd(self.cmd_to_pb(data))

    def check_error_rvc_lock_control(self, op: int = 2, error_vid="aaaaaaaaaaaaaa"):
        "远控接闭锁请求,op:1: 解锁, 2:闭锁, 3: 关门+闭锁"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": error_vid,
            "vehicleModel": 61,
            "cmdCode": 1,
            "cmdDetail": {
                "lock_control": {
                    "op": op,
                    "userId": "1254382316769029465"
                }
            }
        }

        token = self.get_token()
        logger.info("获取车云token为{}:".format(token))
        headers = {"Content-Type": "application/json", "Authorization": token,"client": "4", "user-agent":"jiduapp/3.2.88 (Android; 12; HUAWEI; com.jiduauto.app; RTE-AL00; debugapp; 000000003b3b9f65ffffffffc6d8a9da; SFdSVEU=)", "x-jidu-servicename":"app_android", "Connection":"close"}
        # try:
        resp = requests.post(self.cmd_url, headers=headers, data=json.dumps(self.cmd_to_pb(data)), timeout=10)
        logger.info(f"resp.json() is:{resp.json()}")
        return resp.json()

    def rvc_find_vehicle(self, op: int = 1):
        "远控寻车,op:(-1,关闭;1,鸣笛闪灯;2,仅闪灯)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 3,
            "cmdDetail": {
                "panic_vehicle": {
                    "op": op,
                    "userId": "1254382316769029465"
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_window_control(self, win_fl: int = 100, win_fr: int =100, win_rl: int = 100, win_rr: int = 100):
        "远控开窗请求"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 2,
            "cmdDetail": {
                "window_control": {
                    "frontLeft": win_fl,
                    "frontRight": win_fr,
                    "secondRowLeft": win_rl,
                    "secondRowRight": win_rr
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_tailgate_control(self, op: int = -1, position: int = 0):
        "远控尾门请求,op:动作(-1: 关, 1:开)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 4,
            "cmdDetail": {
                "tailgate_control": {
                    "op": op,
                    "position": position
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_charge_soc_settings(self, max_soc: int = 1000):
        "充电设置请求，千分比(50.0%-100.0%,默认85.0%)如870为87%"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 5,
            "cmdDetail": {
                "charge_soc_settings": {
                    "max": max_soc,
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_rear_view_control(self, op: int = 1):
        """
        op后视镜状态(1展开, -1折叠)
        
        Args:
            op (int, optional): 后视镜状态，1表示展开，-1表示折叠。默认为1。
        
        Returns:
            str: 执行ID
        
        """
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 24,
            "cmdDetail": {
                "rear_view_control": {
                    "op": op
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_ac_control(self, op: int = 1, temp: int = 220):
        "空调请求, op(1: 开，-1: 关), temp: 22 //int 温度(16~28, 默认 22)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 6,
            "cmdDetail": {
                "ac_Control": {
                    "op": op,
                    "temp": temp
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_cold_down(self, op: int = 1):
        "极速制冷， op(1: 开，-1: 关)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 27,
            "cmdDetail": {
                "ac_rapid_cooling": {
                    "op": op,
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_heat_up(self, op: int = 1):
        "极速制热， op(1: 开，-1: 关)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 28,
            "cmdDetail": {
                "ac_rapid_heating": {
                    "op": op,
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_driver_seat_heat(self, level: int = 2):
        "主驾加热,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid":self.vid,
            "vehicleModel":61,
            "cmdCode":13,
            "cmdDetail":{
            "driver_seat_heat":{
                "level":level
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_passenger_seat_heat(self, level: int = 2):
        "副驾加热,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid":self.vid,
            "vehicleModel":61,
            "cmdCode":14,
            "cmdDetail":{
            "passenger_seat_heat":{
                "level":level
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id
    
    def rvc_rearleft_seat_heat(self, level: int = 2):
        "左后座椅加热,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid":self.vid,
            "vehicleModel":61,
            "cmdCode":22,
            "cmdDetail":{
            "rear_left_seat_heat":{
                "level":level
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_rearright_seat_heat(self, level: int = 2):
        "右后座椅加热,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid":self.vid,
            "vehicleModel":61,
            "cmdCode":23,
            "cmdDetail":{
            "rear_right_seat_heat":{
                "level":level
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_steering_wheel_heat(self, level: int = 2):
        "level方向盘加热等级(1档,2......)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 8,
            "cmdDetail": {
                "steering_wheel_heat": {
                    "level": level
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_charge_operation(self, op: int = -1):
        "op充电开关(1: 开始，-1: 结束).  注：当前只有-1生效"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 9,
            "cmdDetail": {
                "charge_operation": {
                    "op": op
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_charge_Lidgate(self, op: int = 1):
        "op充电口盖(1: 开，-1: 关)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 12,
            "cmdDetail": {
                "charge_lid_gate": {
                    "op": op
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_defrost_control(self, op: int = 1):
        "op除霜开关(-1关,1开)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 15,
            "cmdDetail": {
                "defrost_control": {
                    "op": op
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_remote_authorization(self, op: int = 1):
            "op授权(1开)"
            exec_id = str(int(time.time()*10))
            data = {
                "execId": exec_id,
                "vid": self.vid,
                "vehicleModel": 61,
                "cmdCode": 16,
                "cmdDetail": {
                    "remote_auth_start_up": {
                        "op": op
                    }
                }
            }
            self.send_rvc_cmd(self.cmd_to_pb(data))
            return exec_id
    
    def rvc_maintainpower_control(self, op: int = -1):
        "op维持上电开关(-1关,1开), 当前只能远控关闭维持上电"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 17,
            "cmdDetail": {
                "maintain_power": {
                    "op": op
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_driver_seat_vent(self, level: int = 2):
        "level座椅通风等级(1档,2......)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 18,
            "cmdDetail": {
                "driver_seat_vent": {
                    "level": level
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_passenger_seat_vent(self, level: int = 2):
        "level座椅通风等级(1档,2......)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 19,
            "cmdDetail": {
                "passenger_seat_vent": {
                    "level": level
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_rear_left_seat_vent(self, level: int = 2):
        "level座椅通风等级(1档,2......)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 20,
            "cmdDetail": {
                "rear_left_seat_vent": {
                    "level": level
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_rear_right_seat_vent(self, level: int = 2):
        "level座椅通风等级(1档,2......)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 21,
            "cmdDetail": {
                "rear_right_seat_vent": {
                    "level": level
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def rvc_one_click_smart_cockpit_1(self, selectedLoc: list = [1,2,3,4,5], temp: int = 220):
        "一键备车: 1:主驾座椅、2:副驾座椅、3:后排左座椅、4:后排右座椅、5:方向盘加热、目标温度需要*10"
        exec_id = str(int(time.time()*10))
        data = {
            "vid": self.vid,
            "execId": exec_id,
            "userConf":{
            "switch":"true",
            "selectedLoc": selectedLoc,
            "temp": temp
            }
        }
        self.cmd_to_ready(data)

    def rvc_one_click_smart_cockpit_3(self, selectedLoc: list = [1,2,3,4,5,6], temp: int = 220, acAutoType: int = 2):
        "一键备车: 1:主驾座椅、2:副驾座椅、3:后排左座椅、4:后排右座椅、5:方向盘加热、6:电池加热、目标温度需要*10"
        exec_id = str(int(time.time()*10))
        data = {
            "vid": self.vid,
            "execId": exec_id,
            "userConf":{
            "switch":"true",
            "selectedLoc": selectedLoc,
            "temp": temp,
            "acAutoType":acAutoType
            }
        }
        self.cmd_to_ready(data)

    def rvc_one_click_smart_cockpit_2(self, op: int = 1):
        "一键备车PB指令"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 25,
            "cmdDetail": {
                "super_ac_control": {
                    "op": op
                }
            }
        }
        a = self.cmd_to_pb(data)
        logger.info(a)
        self.send_rvc_cmd(a)
        return exec_id

    def log_search(self, keywords: str = "Success", timeout: int = 28):  
        # ParkFail，Success，UsageModeFail，PluggerConnected......
        """
        :params str : keywords为校验车云结果的关键字,例如以前在TCAM日志中'code = 0 msg = Success execType = 3',keywords就取Success
        """
        start_time = time.time()  
        end_time = start_time + timeout  
        url = 'https://logservice.jidustaging.com/api/search/common'  
        headers = {  
            'Content-Type': 'application/json',  
            'Cookie': 'jidu_device_id=d5725be5-2a5b-41fd-9637-8e12501abf2c'  
        }  
        data = {  
            "index": "jidulogapp-staging-remote-vehicle-control-serverlog",  
            "service_name": "remote-vehicle-control",  
            "term_query": {"level": "INFO"},  
            "fuzzy_query": ["", "vehicleReportHandleFinish", "execType"],  
            "begin": 0,  
            "end": int(time.time()),  
            "from": 0,  
            "size": 10  
        }  
        while time.time() < end_time:  
            current_time = datetime.datetime.now()  
            data["begin"] = int(time.mktime((current_time - datetime.timedelta(seconds=37)).timetuple()))  
            data["end"] = int(time.mktime(current_time.timetuple()))
            data["fuzzy_query"][0] = f"vid:\"{self.vid}\""  
            
            logger.info("查询的参数为: data {}".format(data))  
            try:  
                response = requests.post(url, headers=headers, json=data)  
                if response.json()["code"] == 0:  
                    res = response.json()["data"]  
                    logger.info("查询TCAM上报到车云的远控结果集为: res {}".format(res))  
                    if res:  
                        match = re.search(rf'msg:"{keywords}"', str(res))  
                        if match:  
                            logger.info("查找到TCAM上报到车云的远控结果为{}".format(keywords))  
                            return True  
                    else:  
                        logger.error("查询到当前时间TCAM上报到车云的远程控制结果为空: res {}".format(res))  
                else:  
                    logger.error("TCAM云端日志查询失败")  
            except requests.exceptions.RequestException as e:  
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
                logger.error("请求失败: {}".format(e))  
            
            # 每次等待1秒再次尝试 
            time.sleep(1)  
        
        # 如果循环结束仍未找到，则返回False  
        logger.error("在指定时间内未查到TCAM上报到车云的远程控制结果")  
        return False  
    
    @retry_on_failure(10,5)     
    def rvc_taskCmd(self,fixed=False,appointment_hour=0,appointment_minute=30,appointWeekday="0000000", cyclesType=1,ac=1,temp=230,driver_level=1,passenger_level=1, RearLeft_level=-1,RearRight_level=-1, steering_level=1,DriverVent_level=-1,PassengerVent_level=-1,RearLeftVent_level=-1,RearRightVent_level=-1):
        """
        远程座舱预约,自动预约当前时间00分钟后的预约任务,时间可以根据需要调整
        :params  fixed bool:                根据 'true or false' 进行座舱预约上车时间计算
        :params  appointment_hour int:      预约上车时间, 设置预约时间为每天的指定时间
        :params  appointment_minute int:    预约上车时间, 默认当前时间后30分钟上车,例如预约空调、座椅加热立即执行,appointment_minute可以设置15分钟
        :params  appointWeekday int：       设置一周的周几执行，appointWeekday="1000000": 为每周一执行
        :params  ac   int:                  设置空调开关,默认1为开, -1为关
        :params  temp int:                  设置空调温度,例如设置23°C,就是230
        :params  driver_level int:          主驾加热挡位默认1,level(ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  passenger_level int:       副驾加热挡位默认1,level(ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  RearLeft_level int:        后左座椅加热挡位默认-1,level(ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  RearRight_level int:       后右座椅加热挡位默认-1,level(ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  steering_level int :       方向盘加热等级默认1,1档,2......
        :params  DriverVent_level int:      主驾通风挡位默认-1,level(ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  PassengerVent_level int:   副驾通风挡位默认-1,level(ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  RearLeftVent_level int:    后左驾通风挡位默认-1,level(ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  RearRightVent_level int:   后右驾通风挡位默认-1,level(ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  cyclesType int:            为预约循环设置,SctUnknown=0;//空挡
                                                SctOnce= 1;//一次 
                                                SctDaily= 2;//每日 
                                                SctWorkDay=3;//工作日 
                                                SctweekDay= 4; // 周一到周日可选                                
        """
        # current_time = datetime.datetime.now()
        if not fixed:
            # 设置预约当前时间00分钟后的预约任务  
            appointment_time = datetime.datetime.now() + datetime.timedelta(minutes=appointment_minute)  
        else:
            # 设置预约时间为每天的指定时间
            appointment_time = datetime.datetime.now().replace(hour=appointment_hour, minute=appointment_minute)

        # 将时间格式转换化为类似16:40形式  
        formattedUseVehicleTime = appointment_time.strftime("%H:%M")  
        
        token = self.get_token()
        url = 'https://api.jidustaging.com/api/rvc/client/opSubscribeTask'  
        headers = {  
            'Authorization': token,  
            "client": "4",  
            'User-Agent': 'jiduapp/2.2.0 (Android; 12; HUAWEI; com.jiduauto.app; TAS-AN00; huaweigeneral; 791a8f7f2def4fd9a4ac8023f29cacfe; SFdUQVM=)',  
            'x-jidu-servicename': 'app_android',  
            'Content-Type': 'application/json',  
            'Cookie': 'jidu_device_id=b60f1ed4-151b-4bda-8ff0-c74249e279ca' 
        }
        exec_id = str(int(time.time()*10))  
        data = {  
            "execID" : exec_id,  
            "op" : 1,  
            "taskDetail" : {  
                "appointWeekday" : appointWeekday,  
                "cmdDetail" : {  
                    "acControl" : {  
                        "op" : ac,  
                        "temp" : temp 
                    },  
                    "driverSeatHeat" : {  
                        "level" : driver_level 
                    },  
                    "passengerSeatHeat" : {  
                        "level" : passenger_level  
                    },  
                    "rearLeftSeatHeat" : {  
                        "level" : RearLeft_level 
                    },  
                    "rearRightSeatHeat" : {  
                        "level" : RearRight_level  
                    },  
                    "steeringWheelHeat": {  
                        "level" : steering_level 
                    },
                     "driverSeatVent":{
                        "level" : DriverVent_level
                    },
                    "passengerSeatVent":{
                        "level" : PassengerVent_level
                    },
                    "rearLeftSeatVent":{
                        "level" : RearLeftVent_level
                    },
                    "rearRightSeatVent":{
                        "level" : RearRightVent_level
                    } 
                },  
                "cyclesType" : cyclesType,  
                "formattedUseVehicleTime": formattedUseVehicleTime,  
                "taskID" : 0  
            },
            "vid" : self.vid
        } 
        logger.info(f'下发的指令data:{data}')
        response = requests.post(url, headers=headers, json=data)
        logger.info(response.text)
        msg = (response.json()["msg"])  
        if "OK" in msg: 
            logger.info("TSP下发预约座舱用户上车时间为:{}".format(formattedUseVehicleTime))
            return appointment_time, formattedUseVehicleTime,exec_id
        elif "用户认证失败,请登录后再次操作" in msg:
            self.get_token_from_web()
            raise PermissionError
        else:
            raise requests.RequestException
        

    def log_appointment_search(self, keywords: str = "Success"):
        """
        远程座舱预约TCAM上报到车云的预约结果查询
        :params str : keywords为校验车云结果的关键字,例如:Success
                                                   
        """
        time.sleep(10)
        # 获取当前时间  
        current_time = datetime.datetime.now()  
        print(current_time)
        # 计算37秒之前的时间  
        time_25_seconds_ago = current_time - datetime.timedelta(seconds=40)  
        # 车云日志查询开始时间 
        begin = int(time.mktime(time_25_seconds_ago.timetuple()))
        # 车云日志查询结束时间  
        end = int(time.mktime(current_time.timetuple()))
        
        url = 'https://logservice.jidustaging.com/api/search/common'  
        headers = {  
            'Content-Type': 'application/json',  
            'Cookie': 'jidu_device_id=d5725be5-2a5b-41fd-9637-8e12501abf2c'  
        } 
        data = {  
            "index": "jidulogapp-staging-remote-vehicle-control-serverlog",  
            "service_name": "remote-vehicle-control",  
            "term_query": {"level": "INFO"},  
            "fuzzy_query": ["","SubscribeTask|SubscribeTaskExecUpload finsh", "execDetail"],  
            "begin": begin,  
            "end": end,  
            "from": 0,  
            "size": 10  
            }        
        data["fuzzy_query"][0] = f"{self.vid}"
        
        logger.info("查询的参数为: data {}".format(data))
        try: 
            response = requests.post(url, headers=headers, json=data)  
            if response.json()["code"] == 0:
                res = response.json()["data"] 
                logger.info("查询的TCAM上报到车云的结果集为: res {}".format(res))
                if res is not None: 
                    if res.get('entries'):
                        for entry in res['entries']:  
                            message = entry['message']  
                            if keywords in message:  
                                logger.info("查找到TCAM上报到车云的远程座舱预约结果为: {}".format(keywords))  
                                return True
                            else:  
                                logger.error("未查到TCAM上报到车云的远程座舱预约结果: {}".format(message))
                                return False
                    else:
                        logger.error("未查询到当前时间TCAM上报到车云的远程座舱预约结果: {}".format(res.get('entries')))
                        return False
                else:
                    logger.error("查询到当前时间TCAM上报到车云的远程座舱预约结果为空: {}".format(res))
                    return False
            else:
                logger.error("TCAM云端日志查询失败")
                return False
            
        except requests.exceptions.RequestException as e:  
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
            logger.error("请求失败: {}".format(e))      

    def log_SubscribeTaskResp_search(self, fuzz_match: str = "msg=SubscribeTask|SubscribeTaskResp finsh", detail="code:1", keywords: str = "Success", seconds: int=60):
        """
        远程座舱预约执行过程中TCAM上报到车云的执行结果查询
        :params str : fuzz_match为校验车云结果的模糊词,例如：SubscribeTask|SubscribeTaskResp finsh、SubscribeTask|SubscribeTaskExecUpload finsh
        :params str : detail为校验车云结果的准确词，例如：code:1、cmdResp=execId
        :params str : keywords为校验车云结果的关键字,例如:CarModeFail、SOCLow、ChargingOngoing、ParkFail 、MntnMode、UsageModeFail
        :params str : seconds为校验多少秒之前的车云时间
                                                   
        """
        time.sleep(20)
        # 获取当前时间  
        current_time = datetime.datetime.now()  
        print(current_time)
        # 计算60秒之前的时间  
        time_60_seconds_ago = current_time - datetime.timedelta(seconds=seconds)  
        # 车云日志查询开始时间 
        begin = int(time.mktime(time_60_seconds_ago.timetuple()))
        # 车云日志查询结束时间  
        end = int(time.mktime(current_time.timetuple()))
        
        url = 'https://logservice.jidustaging.com/api/search/common'  
        headers = {  
            'Content-Type': 'application/json',  
            'Cookie': 'jidu_device_id=d5725be5-2a5b-41fd-9637-8e12501abf2c'  
        } 
        data = {  
            "index": "jidulogapp-staging-remote-vehicle-control-serverlog",  
            "service_name": "remote-vehicle-control",  
            "term_query": {"level": "INFO"},  
            "fuzzy_query": ["", fuzz_match, detail],  
            "begin": begin,  
            "end": end,  
            "from": 0,  
            "size": 10  
            }        
        data["fuzzy_query"][0] = f"vid={self.vid}"
        
        logger.info("查询的参数为: data {}".format(data))
        try: 
            response = requests.post(url, headers=headers, json=data)  
            logger.info("查询TCAM上报到车云的结果:{}".format(response.json()["code"]))
            if response.json()["code"] == 0:
                res = response.json()["data"] 
                logger.info("查询的TCAM上报到车云的结果集为: res {}".format(res))
                if res is not None: 
                    if res.get('entries'):
                        for entry in res['entries']:  
                            message = entry['message']  
                            if keywords in message:  
                                logger.info("查找到TCAM上报到车云的远程座舱预约结果为: {}".format(keywords))  
                                return True
                        logger.error(f"未在TCAM上报到车云的远程座舱预约结果中找到关键字:{keywords}")
                        return False
                    else:
                        logger.error("未查询到当前时间TCAM上报到车云的远程座舱预约结果: {}".format(res.get('entries')))
                        return False
                else:
                    logger.error("查询到当前时间TCAM上报到车云的远程座舱预约结果为空: {}".format(res))
                    return False
            else:
                logger.error("TCAM云端日志查询失败")
                return False
            
        except requests.exceptions.RequestException as e:  
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
            logger.error("请求失败: {}".format(e))    

    def log_SubscribeTaskUpload_search(self, fuzz_match: str = "SubscribeTask|SubscribeTaskUpload finsh", detail="taskDetail", keywords: str = "useVehicleTime", seconds: int=60):
        """
        远程座舱预约执行过程中TCAM上报预约任务查询
        :params str : fuzz_match为校验预约任务的模糊词,例如：SubscribeTask|SubscribeTaskResp finsh、SubscribeTask|SubscribeTaskExecUpload finsh
        :params str : detail为校验预约任务的准确词，例如：code:1、cmdResp=execId
        :params str : keywords为校验预约任务的关键字,例如:CarModeFail、SOCLow、ChargingOngoing、ParkFail 、MntnMode、UsageModeFail
        :params str : seconds为校验多少秒之前的车云时间
                                                   
        """
        time.sleep(20)
        # 获取当前时间  
        current_time = datetime.datetime.now()  
        print(current_time)
        # 计算60秒之前的时间  
        time_60_seconds_ago = current_time - datetime.timedelta(seconds=seconds)  
        # 车云日志查询开始时间 
        begin = int(time.mktime(time_60_seconds_ago.timetuple()))
        # 车云日志查询结束时间  
        end = int(time.mktime(current_time.timetuple()))
        
        url = 'https://logservice.jidustaging.com/api/search/common'  
        headers = {  
            'Content-Type': 'application/json',  
            'Cookie': 'jidu_device_id=d5725be5-2a5b-41fd-9637-8e12501abf2c'  
        } 
        data = {  
            "index": "jidulogapp-staging-remote-vehicle-control-serverlog",  
            "service_name": "remote-vehicle-control",  
            "term_query": {"level": "INFO"},  
            "fuzzy_query": ["", fuzz_match, detail],  
            "begin": begin,  
            "end": end,  
            "from": 0,  
            "size": 10  
            }        
        data["fuzzy_query"][0] = f"vid={self.vid}"
        
        logger.info("查询的参数为: data {}".format(data))
        try: 
            response = requests.post(url, headers=headers, json=data)  
            if response.json()["code"] == 0:
                res = response.json()["data"] 
                logger.info("查询的TCAM上报到车云的结果集为: res {}".format(res))
                if res is not None: 
                    if res.get('entries'):
                        for entry in res['entries']:  
                            message = entry['message']
                            if keywords in message:  
                                logger.info("已查到TCAM上报到车云的预约任务")  
                                return True, message
                        logger.error(f"未在TCAM上报到车云的远程座舱预约结果中找到关键字:{keywords}")
                        return False
                    else:
                        logger.error("未查询到当前时间TCAM上报到车云的远程座舱预约任务结果: {}".format(res.get('entries')))
                        return False
                else:
                    logger.error("查询到当前时间TCAM上报到车云的远程座舱预约任务结果为空: {}".format(res))
                    return False
            else:
                logger.error("TCAM云端日志查询失败")
                return False
            
        except requests.exceptions.RequestException as e:  
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
            logger.error("请求失败: {}".format(e))   

    def cancel_cock_reserv_task(self, task_time: str, appointWeekday="0000000",cyclesType=1,ac=1,temp=230,driver_level=1,passenger_level=1,steering_level=1):
        taskID = self.get_rvc_appoint_taskID()
        token = self.get_token()
        url = 'https://api.jidustaging.com/api/rvc/client/opSubscribeTask'  
        headers = {  
            'Authorization': token,  
            'client': '4',
            'User-Agent': 'jiduapp/2.2.0 (Android; 12; HUAWEI; com.jiduauto.app; TAS-AN00; huaweigeneral; 791a8f7f2def4fd9a4ac8023f29cacfe; SFdUQVM=)',  
            'x-jidu-servicename': 'app_android',  
            'Content-Type': 'application/json',  
            'Cookie': 'jidu_device_id=b60f1ed4-151b-4bda-8ff0-c74249e279ca'  
        }  

        data = {  
            "execID" : "1699847469871",  
            "op" : 3,  
            "taskDetail" : {  
                "appointWeekday" : appointWeekday,  
                "cmdDetail" : {  
                    "acControl" : {  
                        "op" : ac,  
                        "temp" : temp 
                    },  
                    "driverSeatHeat" : {  
                        "level" : driver_level 
                    },  
                    "passengerSeatHeat" : {  
                        "level" : passenger_level  
                    },  
                    "steeringWheelHeat": {  
                        "level" : steering_level 
                    }  
                },  
                "cyclesType" : cyclesType,  
                "formattedUseVehicleTime": task_time,  
                "taskID" : taskID  
            },  
            "vid" : self.vid
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)  
            response.raise_for_status()  # 如果状态不是200, 引发HTTPError异常  
        except RequestException as e:  
           __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
           logger.info(f"请求出错：{e}")  
        except Exception as e:  
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
            print(f"发生未知错误：{e}")  
        else:    
            logger.info(response.text)

    def get_rvc_appoint_taskID(self):
        token = self.get_token()
        url = 'https://api.jidustaging.com/api/rvc/client/getSubscribeTask?vid=' + str(self.vid)  
        headers = {  
            'Authorization': token,
            'client': '4',  
            'User-Agent': 'jiduapp/2.2.0 (Android; 12; HUAWEI; com.jiduauto.app; TAS-AN00; huaweigeneral; 791a8f7f2def4fd9a4ac8023f29cacfe; SFdUQVM=)',  
            'x-jidu-servicename': 'app_android',  
            'Content-Type': 'application/json',  
            'Cookie': 'jidu_device_id=b60f1ed4-151b-4bda-8ff0-c74249e279ca'  
        }  
        try: 
            response = requests.get(url, headers=headers)
            if response.json()["code"] == 0:
                data = response.json()["data"] 
                logger.info(f"查询的TCAM上报到车云的任务内容为:{data}")
                if data is not None: 
                    task_id = data["taskDetail"]["taskID"]
                    logger.info(f"查找到当前时间TCAM上报到车云的预约任务ID为{task_id}")
                    return task_id   
                else:
                    logger.error(f"查询到当前时间TCAM上报到车云的预约任务内容为空: {data}")
                    return False
            else:
                logger.error("TCAM云端日志查询失败")
                return False    
        except requests.exceptions.RequestException as e:  
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
            logger.error(f"请求失败: {e}")


    def get_task_name(self, task_id: int):
        self.ota = self.ota_obj(task_id)
        task_name = self.ota.get_sub_tasks()["data"]["list"][0]["vehicleDescription"]
        return task_name
    
    def get_vsp_fota_status(self, task_id: int, vin: str = None):
        self.ota = self.ota_obj(task_id)
        if vin is not None:
            logger.info(f"Use Vin Entered: {vin}")
            sub_tasks = self.ota.get_sub_task_vehicles(vin=vin, deliver_city="", debug=True)
        else:
            logger.info("Use bench_config Vin")    
            sub_tasks = self.ota.get_sub_task_vehicles(vin=self.vin, deliver_city="", debug=True)
        update_status = sub_tasks["data"]["list"][0]['vehicleUpgradeStatus']
        logger.info(f"vsp fota status is {update_status}")
        return update_status
    
    def datetime_to_timestamp(self, date_time: str):
        time_array = time.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        return int(time.mktime(time_array))

    def timestamp_to_datetime(self, time_stamp: int):
        return datetime.datetime.fromtimestamp(time_stamp).strftime("%Y-%m-%d %H:%M:%S")

    def get_gb32960data_direct(self, vin: str, start_time, end_time, data_type: str, cycle_time: int = 10,
                                data_mode: str = "直连模式"):
        if type(start_time) == str:
            start_time = self.datetime_to_timestamp(start_time)
        if type(end_time) == str:
            end_time = self.datetime_to_timestamp(end_time)
        payload = {
            "uniqueId": vin,
            "startTime": self.timestamp_to_datetime(int(start_time)),
            "endTime": self.timestamp_to_datetime(int(end_time)),
            "commandId": data_type,
            "dataMode": data_mode
        }
        header = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        res = requests.post(self.gb32960_dirct_url, json=payload, headers=header)
        logger.info("Query result of GB32960 data from DB {0}".format(res.text))
        gb_data = json.loads(res.text)["data"]
        return gb_data
    
    def check_gb_data_cycle(self, gb_data_list:list, start_time, end_time, data_type: str, cycle_time: int = 10):
        if type(start_time) == str:
            start_time = self.datetime_to_timestamp(start_time)
        if type(end_time) == str:
            end_time = self.datetime_to_timestamp(end_time)
        collect_times = []
        for data in gb_data_list:
            collect_times.append(data["dataCollectTime"])
        logger.info("Query result of GB32960 data from DB {0}".format(collect_times))
        s_time = int(start_time)
        e_time = int(end_time)
        if data_type == "车辆登入":
            if len(gb_data_list) != 1:
                assert False
            logger.info("开始检查的时间： {0}".format(self.timestamp_to_datetime(int(s_time))))
            logger.info("报文时间戳： {0}".format(gb_data_list[0]["dataCollectTime"]))
            assert self.datetime_to_timestamp(gb_data_list[0]["dataCollectTime"]) - s_time <= 10
        elif data_type == "车辆登出":
            if len(gb_data_list) != 1:
                assert False
            logger.info("开始检查的时间： {0}".format(self.timestamp_to_datetime(int(s_time))))
            logger.info("报文时间戳： {0}".format(gb_data_list[0]["dataCollectTime"]))
            assert self.datetime_to_timestamp(gb_data_list[0]["dataCollectTime"]) - e_time < 20
        else:
            if len(gb_data_list) == 0:
                assert False 
            for data in gb_data_list:
                logger.info("开始检查的时间： {0}".format(self.timestamp_to_datetime(int(s_time))))
                logger.info("报文时间戳： {0}".format(data["dataCollectTime"]))
                tmp_time = self.datetime_to_timestamp(data["dataCollectTime"])
                assert  tmp_time - s_time <= cycle_time + 1
                s_time = tmp_time
            assert e_time - s_time <= cycle_time

    def get_gb32960data_direct_alarm_level3(self, vin:str, alarm_trigger_time: int):
        gb_data = self.get_gb32960data_direct(vin=vin, start_time=self.timestamp_to_datetime(alarm_trigger_time-31),
                                    end_time=self.timestamp_to_datetime(alarm_trigger_time),
                                    data_type="补发信息上报", cycle_time=1)
        self.check_gb_data_cycle(gb_data_list=gb_data,start_time=self.timestamp_to_datetime(alarm_trigger_time-31),
                                    end_time=self.timestamp_to_datetime(alarm_trigger_time),
                                    data_type="补发信息上报", cycle_time=1)       
        gb_data = self.get_gb32960data_direct(vin=vin, start_time=self.timestamp_to_datetime(alarm_trigger_time-1),
                                    end_time=self.timestamp_to_datetime(alarm_trigger_time+30),
                                    data_type="实时信息上报", cycle_time=1)
        self.check_gb_data_cycle(gb_data_list=gb_data,start_time=self.timestamp_to_datetime(alarm_trigger_time-1),
                            end_time=self.timestamp_to_datetime(alarm_trigger_time+30),
                            data_type="实时信息上报", cycle_time=1)       
        
    def get_gb32960data_forward(self, vin: str = "LSTEST6R9F2086644"):
        # auth = AuthManager(env_name="staging")
        # token = auth.get_passport_b_token(
        #     client_id="0c39c12e8c134d47",
        #     client_secret="${XAT_CREDENTIAL_SCAN_0096632CF015095C98D0}",
        #     user_name=self.user_name,
        #     password=self.password,
        # )

        data = requests.get(
            url=self.gb32960_forward_url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": __import__("os").environ.get('XAT_CREDENTIAL_____INTERFACES_DP1_TSP_PY_AUTHORIZATION', ""),
            },
            params= {"vin": vin}
        )
        return data.text(vin)["data"]

    def trigger_update_by_real_app(self, vid: str = None, tel: str = None):
        #不能乱用，云端会报警，仅限休眠唤醒场景使用
        #平时测试使用 trigger_fota_type90() 
        token = Auth(env_name='staging').get_app_token(env_name="staging", tel=tel)[0]
        headers =  {"Content-Type": "application/json", 'authorization': token}
        pre_url = f'https://m-staging.jiduapp.cn/api/fota/cache/app/task/detail?vid={vid if vid is not None else self.vid}&userId={self.get_userid(tel) if tel is not None else self.get_userid()}'
        url = f'https://m-staging.jiduapp.cn/api/fota/cache/appUpgrade/trigger?vid={vid if vid is not None else self.vid}&userId={self.get_userid(tel) if tel is not None else self.get_userid()}'
        for i in range(10):
            pre_response = requests.get(url=pre_url, headers=headers).json().get("data")['canTriggerUpgrade']
            if pre_response == 1:
                logger.info("当前条件满足手机app触发升级")
                response = requests.get(url=url, headers=headers).json()
                logger.info(f"{response['code']}, {response['msg']}")
                return response['code'], response['msg']
            else:
                logger.info("app触发条件不满足，稍后重试")
                time.sleep(12)
        else:
            logger.info("app触发条件不满足，无法触发升级")

    def get_userid(self, tel: str = None):
        "获取APP 操作的userid"
        headers = {  
            "Content-Type": "application/json",  
            "client": "4"  
        }  
        data = {
            "countryCode": "86",
            "tel": tel if tel is not None else self.tel,
            "captcha": "6825",
            "captchaKey": __import__("os").environ['XAT_CREDENTIAL_SCAN_E1A925FC15AC6FA6CC7D']
        }
        response = requests.post(self.token_url, headers=headers, json=data)  
        userid = (response.json()['data']['user']['userId'])
        return userid
    
    def mno_setAPNsts(self, APN4sts: int=1, iccid="89860808092390000036"):
        """
        仅限蜂窝测试实名使用，其他勿调用此接口
        通过MNO平台提供模拟APN4开关状态下发的接口，实现云端开关APN4，默认apn4状态为开
        param： APN4sts: int
                0  关
                1  开
        """
        url = 'https://mno-tsp.jidustaging.com/api/mno/apnStatus/notify'  
        headers = {   
            'Content-Type': 'application/json',  
            'Cookie': 'jidu_device_id=8ac91c70-efd5-417a-9fe5-e7fe8f705917' 
        }  
        data = {  
                "type": 2,
                "iccid": iccid,
                "timestamp": 1705026018832,
                "notifyBody": [
                    {
                        "apnName": "CMMTM5GJDC.SH",
                        "status": "1"
                    },
                    {
                        "apnName": "CMMTM5GJDD.SH",
                        "status": APN4sts
                    },
                    {
                        "apnName": "CMIOT5GJDA.SH",
                        "status": "1"
                    },
                    {
                        "apnName": "CMMTM5GJDB.SH",
                        "status": "1"
                    }
        ],
        "notifyType": 2
        }      
        try:
            response = requests.post(url, headers=headers, json=data)  
            response.raise_for_status()  # 如果状态不是200, 引发HTTPError异常  
        except RequestException as e:  
           __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
           logger.info(f"请求出错：{e}")  
        except Exception as e:  
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
            print(f"发生未知错误：{e}")  
        else:    
            logger.info(response.text)  
            logger.info(f"MNO设置APN4状态为{APN4sts}成功")
    
    def mno_log_search(self, search_time: int=30, fuzz_match="由调用网关成功更新状态为", detail= "lambda$mqttCallback", keywords: str = "车端处理成功"):
        """
        mno平台apn4状态查询
        :params serach_time : search_time为查询多少秒之前的云端结果 
        :params fuzz_match  : fuzz_match为校验预约任务的模糊词,例如："由调用网关成功更新状态为"
        :params detail      : detail为校验预约任务的准确词，例如："lambda$mqttCallback"
        :params keywords    : keywords为校验预约任务的关键字,例如:"车端处理成功"                                      
        """
        time.sleep(20)
        # 获取当前时间  
        current_time = datetime.datetime.now()  
        # 计算20秒之前的时间  
        search_time_ago = current_time - datetime.timedelta(seconds=search_time)  
        # 车云日志查询开始时间 
        begin = int(time.mktime(search_time_ago.timetuple()))
        # 车云日志查询结束时间  
        end = int(time.mktime(current_time.timetuple()))
        
        url = 'https://logservice.jidustaging.com/api/search/common'  
        headers = {  
            'Content-Type': 'application/json',  
            'Cookie': 'jidu_device_id=8ac91c70-efd5-417a-9fe5-e7fe8f705917'  
        } 
        data = {  
            "index": "jidulogapp-staging-iot-mno-service-serverlog",  
            "service_name": "iot-mno-service",  
            "term_query": {"level": "INFO"},  
            "fuzzy_query": ["", fuzz_match, detail],  
            "begin": begin,  
            "end": end,  
            "from": 0,  
            "size": 10  
            }        
        data["fuzzy_query"][0] = f"vid:\"{self.vid}"
        logger.info(f"查询的参数为: {data}")
        try: 
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()  # 如果状态不是200, 引发HTTPError异常 
            logger.info(f"查询的TCAM上报到车云的结果集为: {response.text}")
            if response.json()["data"]["entries"][0]['message'] is None:   
                logger.error("未查到TCAM上报到的MNO apn4状态结果")
                return False
            else: 
                assert keywords in response.json()["data"]['entries'][0]['message'],f"云端未查询到mqtt网关结果"  
        except requests.exceptions.RequestException as e:  
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
            logger.error("请求失败: {}".format(e))   
            
    def send_remote_diag_cmd(self, cmd_type: CmdType, session_time_out=300, check_intervel=3):
        with open("config/remote_diag_lua.yaml", encoding="utf-8") as fn:
            yaml_content = yaml.safe_load(fn)
        headers = yaml_content["remote_diag_headers"]
        url = 'https://remote-diagnostic-service.jidustaging.com/api/remote-diagnostic-service/remote/uds/cmd/reqDiagnosticSessionCmd'
        if cmd_type.value == "session_open":
            session_open_json = yaml_content["session_open"]
            session_open_json["vid"] = self.vid
            json_str = json.dumps(session_open_json, ensure_ascii=False)
            result = re.sub(r"SESSION_TIME_OUT=\d+", f"SESSION_TIME_OUT={session_time_out}", json_str)
            payload = re.sub(r"CHECK_INTERVEL=\d+", f"CHECK_INTERVEL={check_intervel}", result)
        elif cmd_type.value == "session_close":
            session_close_json = yaml_content["session_close"]
            session_close_json["vid"] = self.vid
            payload = json.dumps(session_close_json, ensure_ascii=False)
        elif cmd_type.value.split("_")[0] == "SendDiagCmd":
            url = 'https://remote-diagnostic-service.jidustaging.com/api/remote-diagnostic-service/remote/uds/cmd/reqDiagnosticSequenceCmd'
            send_diag_cmd_json = yaml_content["send_diag_cmd"]
            send_diag_cmd_json["vid"] = self.vid
            para = cmd_type.value.split("SendDiagCmd_")[-1]
            send_diag_cmd_json["para"] = yaml_content[para]
            payload = json.dumps(send_diag_cmd_json, ensure_ascii=False)
        else:
            logger.error(f"错误的参数：{cmd_type.value}")
        logger.info(f"参数{payload}")
        try:
            response = requests.post(url=url, data=json.dumps(eval(payload)), headers=headers)  
            response.raise_for_status()  # 如果状态不是200, 引发HTTPError异常  
        except RequestException as e:  
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
            raise f"请求出错：{e}"
        except Exception as e:  
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
            raise f"发生未知错误：{e}"
        else:    
            logger.info(response.text)  
            logger.info(f"下发远程诊断指令{cmd_type.value}成功")

    def get_remote_diag_token(self):
        data = {
            "client_id": "c839a7fe0ad44f12",
            "device_id": "5bb7ebe0-4835-42a6-a1a1-8067348c08fb",
            "password": __import__("os").environ.get('XAT_CREDENTIAL_____INTERFACES_DP1_TSP_PY_PASSWORD', ""),
            "safe_device_id": "726f16d2930bb1c988dbf190d8acd13a",
            "username": "jianwen.wang"
        }
        header = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        response = requests.post(url='https://passport-ext.jidustaging.com/api/passportb-external/v2/login/password', json=data, headers=header)
        if response.status_code == 200:
            data = response.json()
            token = data["data"]["token"]
            with open("config/remote_diag_lua.yaml") as fn:
                yaml_content = yaml.safe_load(fn)
                yaml_content["remote_diag_headers"]["Authorization"] = token
            with open("config/remote_diag_lua.yaml", "w") as f:
                yaml.safe_dump(yaml_content, f)
        else:
            logger.error("请求失败，状态码：", response.status_code)

    def trigger_remote_rescue(self, rescue_type: RescueType):
        data = {
            "vid": self.vid,
            "type": rescue_type.value
        }
        header = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Jidu-Color': 'vehicle-future-sl'
        }
        try:
            response = requests.post(url='http://fota.jidustaging.com/api/fota/gateway/manual/rescue', json=data, headers=header)
            response.raise_for_status()  # 如果状态不是200, 引发HTTPError异常  
        except RequestException as e:  
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
            raise f"请求出错：{e}"
        except Exception as e:  
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
            raise f"发生未知错误：{e}"
        else:    
            logger.info(response.text)

    def get_rvs_data(self,block_id: str, rvs_db="jidulogapp-staging-vidb-report-data", retry_count=10):
        """
        根据查询条件查询rvs数据，数据类型列表，列表中的数据为字符串

        @param condition： 查询条件列表
        @param rvs_db: 查询数据库
        @param retry_count：查询失败最多重试次数
        """
        # client = ES_client()
        condition =  [str(self.vid), block_id]
        result_dict = ""
        query_count = 1
        while query_count < retry_count:
            query_count += 1
            try:
                result_dict = self.log_platform_obj.query_newest_in_es(condition, rvs_db)
            except AttributeError:
                result_dict = self.log_platform_obj.query_newest_in_es(condition, rvs_db)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
                logger.info(type(e))
                result_dict = self.log_platform_obj.query_newest_in_es(condition, rvs_db)
            finally:
                if "##JIDU##" in result_dict:
                    result_dict = result_dict.split("##JIDU##")[0]
                    return eval(result_dict)
                else:
                    return result_dict

            
    def get_digital_key_data(self,condition: list, dk_db="jidulogapp-staging-digital-key-service-serverlog", retry_count=5):
        """
        根据查询条件查询rvs数据，数据类型列表，列表中的数据为字符串

        @param condition： 查询条件列表
        @param rvs_db: 查询数据库
        @param retry_count：查询失败最多重试次数
        """
        # client = ES_client()
        result_dict = ""
        query_count = 1
        current_time = datetime.datetime.now()
        later_time = current_time + datetime.timedelta(seconds=15)
        before_time = current_time - datetime.timedelta(seconds=2)
        before_time_str = before_time.strftime("%Y-%m-%dT%H:%M")
        later_time_str = later_time.strftime("%Y-%m-%dT%H:%M")
        if before_time_str == later_time_str:
            condition = [before_time_str] + condition
        else:
            condition = [f'("{before_time_str}" or "{later_time_str}")'] + condition

        logger.info(f"---------->过滤条件是condition{condition}")
        while query_count < retry_count:
            query_count += 1
            try:
                result_dict = self.log_platform_obj.query_newest_in_es(condition, dk_db)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
                logger.info(f"get_digital_key_data Error:{e}")
                result_dict = self.log_platform_obj.query_newest_in_es(condition, dk_db)
            finally:
                # logger.info(result_dict)
                return result_dict

    def check_digital_key_result(self, func:str,keys: list, target_value: dict ,timeout: Union[int, float] = 20):
        prompt_info = f"----------> Check 数字钥匙结果反馈中是否能查到{target_value}"
        self.rvs_client = self.rvs_obj()
        with allure.step(prompt_info):
            logger.info(prompt_info)
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    result_dict = {}
                    resp_res = self.get_digital_key_data(condition=keys)
                    logger.info(f"--------------------------->{resp_res}")
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
                    logger.info(f"Received data error:{str(e)},Continue")
                    time.sleep(0.5)
                    continue
                
                if resp_res == "":
                    logger.info("Received data is null,Continue")
                    time.sleep(0.5)
                    continue

                if func == "NFCLearning":
                    if "ErrCode:" in resp_res:
                        pos0 = resp_res.find("ErrCode:")
                        match = re.search(r"ErrCode:\d+", resp_res[pos0:])
                        if match:
                            errCode_int = match.group().split(":")[1]
                            result_dict["errCode"] = int(errCode_int)
                        else:
                            result_dict["errCode"] = "Null"
                    elif "errCode:" in resp_res:
                        pos0 = resp_res.find("errCode:")
                        match = re.search(r"errCode:\d+", resp_res[pos0:])
                        if match:
                            errCode_int = match.group().split(":")[1]
                            result_dict["errCode"] = int(errCode_int)
                        else:
                            result_dict["errCode"] = "Null"
                    
                    if "ErrMsg:" in resp_res:
                        pos0 = resp_res.find("ErrMsg:")
                        pos1 = resp_res[pos0:].find(";")
                        errmsg = resp_res[pos0+7+1:pos0+pos1-1]
                        result_dict["ErrMsg"] = errmsg

                    flag = 1
                    for item in target_value:
                        logger.info(f"------------------------>item:{item},云端返回结果:{result_dict[item]},期望结果:{target_value[item]}")
                        if item not in result_dict or result_dict[item] != target_value[item]:
                            flag = 0
                            break
                    if flag == 1:
                        assert True
                        return
                    
                elif func == "WhiteListSync":
                    if "LastSyncTimeForBLE:" in resp_res:
                        pos0 = resp_res.find("LastSyncTimeForBLE:")
                        match = re.search(r"LastSyncTimeForBLE:\d+", resp_res[pos0:])
                        if match:
                            ble_ver = match.group().split(":")[1]
                            result_dict["LastSyncTimeForBLE"] = int(ble_ver)
                        else:
                            result_dict["LastSyncTimeForBLE"] = "Null"
                    if "LastSyncTimeForEntityKey:" in resp_res:
                        pos0 = resp_res.find("LastSyncTimeForEntityKey:")
                        match = re.search(r"LastSyncTimeForEntityKey:\d+", resp_res[pos0:])
                        if match:
                            entiry_ver = match.group().split(":")[1]
                            result_dict["LastSyncTimeForEntityKey"] = int(entiry_ver)
                        else:
                            result_dict["LastSyncTimeForEntityKey"] = "Null"
                    
                    flag = 1
                    for item in target_value:
                        if item not in result_dict or result_dict[item] != target_value[item]:
                            flag = 0
                            break
                    if flag == 1:
                        assert True
                        return
            assert False
                    
    def check_rvs_data_pos(self, block: BlockName, keys: str, target_pos: GeneralInVehiclePos,timeout: Union[int, float] = 10):
        prompt_info = f"----------> Check RVS 上报中是否有数据块{block.name}中{target_pos}所在返回数组中的index"
        self.rvs_client = self.rvs_obj()
        with allure.step(prompt_info):
            logger.info(prompt_info)
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    event_data = self.get_rvs_data(block_id=str(block.value))
                    logger.info(f"--------------------------->{event_data['data']}")
                    value = event_data['data']
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
                    logger.info("Received data is null,Continue")
                    continue
                list_cont = value[keys]
                logger.info(f"上报中{keys}中对应的数据是{list_cont}")
                if isinstance(list_cont, list):
                    if target_pos.name == "FrontLeft":
                        for index in range(len(list_cont)):
                            if int(list_cont[index]["id"]) == 0:
                                logger.info(f"上报中是否有数据块{block.name}中没有找到FrontLeft所在返回数组中的index = {index}")
                                return index
                    elif target_pos.name == "FrontRight":
                        for index in range(len(list_cont)):
                            if int(list_cont[index]["id"]) == 1:
                                logger.info(f"上报中是否有数据块{block.name}中没有找到FrontLeft所在返回数组中的index = {index}")
                                return index
                    elif target_pos.name == "RearLeft":
                        for index in range(len(list_cont)):
                            if int(list_cont[index]["id"]) == 2:
                                logger.info(f"上报中是否有数据块{block.name}中没有找到FrontLeft所在返回数组中的index = {index}")
                                return index
                    elif target_pos.name == "RearRight": 
                        for index in range(len(list_cont)):
                            if int(list_cont[index]["id"]) == 3:
                                logger.info(f"上报中是否有数据块{block.name}中没有找到FrontLeft所在返回数组中的index = {index}")
                                return index
            logger.info(f"上报中数据块{block.name}中没有找到{target_pos}所在返回数组中的index")
            assert False

    def check_rvs_data_update(self, block: BlockName, keys: list, target_value: str, index: int = 0,
                        timeout: Union[int, float] = 10):
        prompt_info = f"----------> Check RVS 上报中是否有数据块{block.name},并且{keys}是否分别为{target_value}"
        self.rvs_client = self.rvs_obj()
        with allure.step(prompt_info):
            logger.info(prompt_info)
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    event_data = self.get_rvs_data(block_id=str(block.value))
                    logger.info(f"--------------------------->{event_data['data']}")
                    value = event_data['data']
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
                    logger.info("Received data is null,Continue")
                    continue
                for k in keys:
                    value = value[k]
                    if isinstance(value, list):
                        value = value[index]
                try:
                    if isinstance(value,str):
                        logger.info("Get the value: {0}, target value: {1}".format(value, target_value))
                        if value == str(target_value):
                            assert True
                            return
                    elif isinstance(value,int):
                        if isinstance(target_value,list):
                            logger.info(f"RVS 上报的值为: {value}, 期望的值为: {target_value[0]},允许的误差为{target_value[1]}")
                            if float(target_value[0] - target_value[1])<= float(value) and float(target_value[0] + target_value[1]) >= float(value):
                                assert True
                                return
                        elif value == int(target_value):
                            logger.info("Get the value: {0}, target value: {1}".format(value, target_value))
                            assert True
                            return
                    elif isinstance(value,float):
                        if isinstance(target_value,list):
                            logger.info(f"RVS 上报的值为: {value}, 期望的值为: {target_value[0]},允许的误差为{target_value[1]}")
                            if float(target_value[0] - target_value[1])<= float(value) and float(target_value[0] + target_value[1]) >= float(value):
                                assert True
                                return
                        elif value == float(target_value):
                            logger.info("Get the value: {0}, target value: {1}".format(value, target_value))
                            assert True
                            return
                    # if isinstance(target_value,list):
                    #     logger.info(f"RVS 上报的值为: {value}, 期望的值为: {target_value[0]},允许的误差为{target_value[1]}")
                    #     if float(target_value[0] - target_value[1])<= float(value) and float(target_value[0] + target_value[1]) >= float(value):
                    #         assert True
                    #         return
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
                    logger.info(f"对比RVS的上报结果{value}和期望结果{target_value}过程中报错：{str(e)}")
                    assert False
            assert False                

    
    # def check_rvs_data_update(self, block: BlockName, keys: list, target_value: str, index: int = 0,
    #                     timeout: Union[int, float] = 20):
    #     prompt_info = f"----------> Check RVS 上报中是否有数据块{block.name},并且{keys}是否分别为{target_value}"
    #     self.rvs_client = self.rvs_obj()
    #     with allure.step(prompt_info):
    #         logger.info(prompt_info)
    #         start_time = time.time()
    #         while time.time() - start_time < timeout:
    #             try:
    #                 event_data = self.get_rvs_data(block_id=str(block.value))
    #                 logger.info(f"--------------------------->{event_data['data']}")
    #                 value = event_data['data']
    #             except Exception as e:
    #                 logger.info("Received data is null,Continue")
    #                 continue
    #             for k in keys:
    #                 value = value[k]
    #                 if isinstance(value, list):
    #                     value = value[index]
    #             try:
    #                 if isinstance(value,str):
    #                     logger.info("Get the value: {0}, target value: {1}".format(value, target_value))
    #                     if value == str(target_value):
    #                         assert True
    #                         return
    #                 elif isinstance(value,int):
    #                     logger.info("Get the value: {0}, target value: {1}".format(value, target_value))
    #                     if value == int(target_value):
    #                         assert True
    #                         return
    #                 elif isinstance(value,float):
    #                     logger.info("Get the value: {0}, target value: {1}".format(value, target_value))
    #                     if value == float(target_value):
    #                         assert True
    #                         return
    #                 if isinstance(target_value,list):
    #                     logger.info(f"RVS 上报的值为: {value}, 期望的值为: {target_value[0]},允许的误差为{target_value[1]}")
    #                     if float(target_value[0] - target_value[1])<= float(value) and float(target_value[0] + target_value[1]) >= float(value):
    #                         assert True
    #                         return
    #             except Exception as e:
    #                 logger.info(f"对比RVS的上报结果{value}和期望结果{target_value}过程中报错：{str(e)}")
    #                 assert False
    #         assert False

    def trigger_fod_task(self, FodConfig):
        millis = int(round(datetime.datetime.now().timestamp() * 1000))
        FodConfig['timestamp'] = millis
        FodConfig['thirdOrderNo'] = str(millis)
        encrypt_dict = FodConfig.copy()
        encrypt_dict["secretKey"] = "bgmKey"
        sorted_keys = sorted(encrypt_dict.keys())
        sorted_dict = {key: encrypt_dict[key] for key in sorted_keys}
        payload_string = json.dumps(sorted_dict)
        pattern = re.compile(r"[^a-zA-Z0-9]")
        payload_string = re.sub(pattern, "", payload_string)
        md5 = hashlib.md5()
        md5.update(payload_string.encode("utf-8"))
        encrypted_payload_string = md5.hexdigest()
        fod_dict = FodConfig.copy()
        fod_dict["sign"] = encrypted_payload_string
        payload = json.dumps(fod_dict)
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", "https://fod-server.jidustaging.com/api/fod-server/change/changeService", headers=headers, data=payload)
        return response.text
    
    def rvs_log_wakeup(self, vid: str = '', ecus: str = 'bgm'):
        """
        触发远程上报日志请求
        :param vid: 设备VID 默认
        :param ecus: bgm, tcam等
        :return:
        """
        if not vid:
            vid = self.vid
        headers = {
            "Content-Type": "application/json",
            "client": "4"
        }
        url = "https://logservice.jidustaging.com/api/vclink/wakeup"
        try:
            response = requests.get(url, headers=headers,
                                    params={'vid': vid, 'ecus': ecus})
            if response.status_code == 200:
                logger.info(f'请求地址:{response.url} 成功')
                return True
        except requests.exceptions as e:
            logger.error(e)
            assert False

    def check_rvs_data_update_new(self, block: BlockName, keys: list, target_value,begin_time:int=None, timeout: Union[int, float] = 5,sleep_time: Union[int, float] = 40,target_value_buffer=0):
            start_time = time.time()
            if not begin_time:
                begin_time = int(time.time()) - 1
            end_time = begin_time + timeout
            while time.time() - start_time < sleep_time:
                data = self.log_search_result(index='jidulogapp-staging-vidb-report-data',service_name='vidb-report',fuzzy_query=[str(block.value)],begin_time=begin_time,end_time=end_time)
                # data_entries_list = self.get_rvs_data_new(str(block.value),timeout=timeout,begin_time=begin_time)
                data_entries_list = data['entries'] if data['entries'] else []
                logger.info(f'获取到数据: {data_entries_list}')
                for data_entry in data_entries_list:
                    data = data_entry['data']
                    value = self.find_value(data, keys)
                    logger.info(f'查找到的值为:{value}')
                    if type(value) == list and type(target_value) != list:
                        value = value[0]
                    logger.info(f'{keys} 当前值: {value}, 期望值: {target_value}')
                    if target_value_buffer != 0:
                        if abs(int(value) - int(target_value)) <= target_value_buffer:
                            assert abs(int(value) - int(target_value)) <= target_value_buffer
                            return
                    else:
                        if value == target_value:
                            assert value == target_value, f'{keys} 没有更新到 {target_value}'
                            return
            assert value == target_value, f'{keys} 没有更新到 {target_value}'


    # def get_rvs_data_new(self, block_id:str='10105', begin_time:int=None, timeout: Union[int, float] = 5):
    #     if not begin_time:
    #         begin_time = int(time.time()) - 1
    #     end_time = begin_time + timeout
        
    #     return data['entries'] if data['entries'] else []
        
    def find_value(self, data, expression_list):
        """Find value by expression in a nested data structure."""
        def _find_value(data1, expression1, value=None):
            if isinstance(data1, list):
                data_list = []
                for item in data1:
                    item = _find_value(item, expression1, value)
                    if item is not None:
                        data_list.append(item)
                return data_list
            elif isinstance(data1, dict):
                item = data1[expression1]
                if value is None:
                    return item
                elif str(value) == str(item):
                    return data1
                else:
                    return None
        for expression in expression_list:
            if '==' in expression:
                value1 = expression.split('==')[1].replace(' ', '')
                expression = expression.split('==')[0].replace(' ', '')
                data = _find_value(data, expression, value1)
            else:
                data = _find_value(data, expression)
        return data
    
    def log_search_result(self,vid:str=None,index = 'jidulogapp-staging-remote-vehicle-control-serverlog', service_name:str = 'remote-vehicle-control', term_query_level:str='INFO',fuzzy_query: list = [],begin_time: int=0,end_time: int=0,size: int=10,interval_time:int =1, num:int=15):
        """
        基础查询,将查询的结果格式化后返回
        """
        if not vid:
            vid = self.vid
        url = 'https://logservice.jidustaging.com/api/search/common'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'jidu_device_id=d5725be5-2a5b-41fd-9637-8e12501abf2c'
        }
        data = {
            "index": index,
            "service_name": service_name,
            "fuzzy_query": [f"{vid}"] + fuzzy_query,
            "begin": int(begin_time),
            "end": int(end_time),
            "from": 0,
            "size": size
        }
        res = {'total':0}
        for i in range(num):
            if not end_time:
                data['end'] = int(time.time())
            logger.info("查询的参数为: data {}".format(data))
            try:
                response = requests.post(url, headers=headers, json=data, timeout=10)
                logger.debug("查询TCAM上报到车云的远控结果集为: response {}".format(response))
                if response.json()["code"] == 0:  
                    res = response.json()["data"]
                    logger.debug("查询TCAM上报到车云的远控结果集为: res {}".format(res))
                    if res['total'] != 0:
                        return res
                else:  
                    logger.error("TCAM云端日志查询失败")
            except requests.exceptions.RequestException as e:  
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
                logger.error("请求失败: {}".format(e))
            time.sleep(interval_time)
        return res
        
    def log_search_remote_vehicle_control(self,keywords: str = "Success", execid:str="", begin_time: int = None, num: int = 25, exectype_num: int=1):
        """
        及时查询remote-vehicle-control服务的log日志
        查询开始时间为调用该方法时间，查询开始时间为调用时间 -1 秒
        结束时间为最大延迟时间。(默认为25s)
        """
        onlyone = True
        if not begin_time:
            begin_time = int(time.time()) - 1 # 预留1s的buff，避免上传时间到查询时间存在1s间隔
        if not execid:
            fuzzy_query = ["sendCmd",'vehicleReportHandleFinish',keywords]
        else:
            begin_time = begin_time - 300
            fuzzy_query = ["sendCmd",'vehicleReportHandleFinish',keywords, execid]

        # 新增msg和exectype对应关心检测
        # 判断execType
        if keywords in ['PreConditionOK','StartOK','AuthEscLockStartOK']:
            fuzzy_query += ['execType:2']
        else:
            fuzzy_query += ['execType:3']

        # 原远控msg查询
        res_data = self.log_search_result(begin_time=begin_time,fuzzy_query=fuzzy_query,num=num)
        logger.info("查询到远控结果集为: {}".format(res_data))
        if keywords not in ['PreConditionOK','StartOK','AuthEscLockStartOK']:
            # 新增exectype=3的唯一性检测
            fuzzy_query1 = ["sendCmd",'vehicleReportHandleFinish','execType:3', execid]
            res_data1 = self.log_search_result(begin_time=begin_time,fuzzy_query=fuzzy_query1,num=num)
            logger.info("查询到远控execType为3数据集: {}".format(res_data1))
            if res_data1['total'] > exectype_num:
                onlyone = False

        if res_data['total'] != 0 and onlyone:
            return True
        else:
            return False


    def get_subscribeId(self,execid,begin_time):
        fuzzy_query = ['SubscribeTaskResp','Success',execid]
        res_data = self.log_search_result(begin_time=begin_time,fuzzy_query=fuzzy_query,num=50)
        if res_data['total'] == 0:
            raise ValueError(f'该{execid}没有查询到对应的subscribeId')
        log_string = res_data['entries'][0]['message']
        logger.info(f'获取到的message： {log_string}')
        pattern = r'subscribeId:\"([^"]+)\"'  
        match = re.search(pattern, log_string)
        if match:  
            subscribe_id = match.group(1)  
            logger.info(f"获取到的subscribeId: {subscribe_id}")  
        else:  
            logger.info("没有找到subscribeId")
            raise ValueError("没有找到subscribeId")
        return subscribe_id
    
    def log_search_battery(self, execid:str, keyword: str = "Success", num: int = 25):
        """
        查询预约充电的结果
        查询开始时间为调用该方法时间，查询开始时间为调用时间 -1 秒
        结束时间为最大延迟时间。(默认为25s)
        """
        begin_time = int(time.time()) - 1 # 预留1s的buff，避免上传时间到查询时间存在1s间隔
        begin_time = begin_time - 300
        subscribe_id = self.get_subscribeId(execid=execid,begin_time=begin_time)
        fuzzy_query = ['SubscribeTaskExecUpload finsh',keyword, subscribe_id]
        res_data = self.log_search_result(begin_time=begin_time,fuzzy_query=fuzzy_query,num=num)
        logger.info("查询到远控结果集为: {}".format(res_data))
        if res_data['total'] != 0:
            return True
        else:
            return False
        
    def log_search_climate_control(self, execid:str, num: int = 25,**kwargs):
        """
        查询预约座舱的结果
        查询开始时间为调用该方法时间，查询开始时间为调用时间 -1 秒
        结束时间为最大延迟时间。(默认为25s)
        **kwargs: 当前支持： ac_control : Success
                            steering_wheel_heat
                            driver_seat_heat
                            driver_seat_vent
                            passenger_seat_heat
                            passenger_seat_vent
                            rear_left_seat_vent
                            rear_left_seat_heat
                            rear_right_seat_vent
                            rear_right_seat_heat
        """
        begin_time = int(time.time()) - 1 # 预留1s的buff，避免上传时间到查询时间存在1s间隔
        begin_time = begin_time - 300
        subscribe_id = self.get_subscribeId(execid=execid,begin_time=begin_time)
        fuzzy_query = ['SubscribeTaskExecUpload finsh', subscribe_id]
        # 构建对应的查询关键词
        for key, value in kwargs.items():
            if value != 'Success':
                fuzzy_query.append(f'cmdCode:{key} code:1 msg:"{value}"')
            else:
                fuzzy_query.append(f'cmdCode:{key}  msg:"{value}"')
        res_data = self.log_search_result(begin_time=begin_time,fuzzy_query=fuzzy_query,num=num)
        logger.info("查询到远控结果集为: {}".format(res_data))
        if res_data['total'] != 0:
            return True
        else:
            return False

    # 异步查询
    def check_async_log_search_result_from_remote_vehicle_control(self,keywords: str = "Success", execid:str="", begin_time: int = None, num: int = 25,flage: int = 0,exectype_num=1):
        """
        异步查询方法,用来实现多步查询
        """
        log_search_dict = {'keywords': keywords, 'begin_time': int(time.time()) - 1, "execid": execid, "num": num,'exectype_num':exectype_num}
        
        if flage == 0:
            self.log_search_list.clear()
            self.log_search_list.append(log_search_dict)
        elif flage == 1:
            self.log_search_list.append(log_search_dict)
        else:
            self.log_search_list.append(log_search_dict)
            logger.info("开始查询远控日志")
            log_search_list = self.log_search_list.copy()
            self.log_search_list.clear()
            for i in log_search_list:
                logger.info(f"开始查询远控日志,参数是：{str(i)}")
                assert self.log_search_remote_vehicle_control(**i)

    def get_tcam_power_status(self):
        prompt_info = f"----------> 检查TCAM电源模式切换上报事件"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.rvs_client = self.rvs_obj()
            return self.rvs_client.manager.get_gateway_data(vid=self.vid, data_type="POWER")[0]

    def get_tcam_network_status(self):
        prompt_info = f"----------> 检查TCAM网络状态切换上报事件"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.rvs_client = self.rvs_obj()
            return self.rvs_client.manager.get_gateway_data(vid=self.vid, data_type="NETWORK")[0]
    
    def buried_point_data_query(self, dt: str=None, hour: str=None, signalname: str=None, httpheadervid: str=None, sigvalue: str=None, timeout: int=200, wait_interval: int=3):
        start_time = time.time()
        flag = True
        Data = DataDev()
        with allure.step("获取时间"):
            if dt is None:
                dt = datetime.datetime.now().strftime("%Y-%m-%d")
            if hour is None:
                hour = datetime.datetime.now().strftime("%H")
        with allure.step("获取httpheadervid"):
            if httpheadervid is None:
                httpheadervid = self.vid
        with allure.step("开始主流程验证sql"):       
            Data.validate_sql(dt, hour, signalname, httpheadervid, sigvalue)
            assert Data.code == 0, "验证sql失败"
            assert Data.data is not None, "验证sql返回结果为空"
        with allure.step("执行sql"):            
            Data.run_sql()
            assert Data.code == 0, "执行sql失败"
            assert Data.data is not None, "执行sql返回结果为空"
        with allure.step("获取执行日志"):
            while flag:
                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout:
                    assert False, "日志查询操作超时"
                Data.get_log()
                assert Data.code == 0, "获取日志失败"
                assert Data.data is not None, "获取日志返回结果为空"
                time.sleep(wait_interval)
                if Data.has_result == 1 and Data.status == 2:
                    flag = False
        time.sleep(wait_interval)
        with allure.step("获取result结果"):
            Data.get_result()
            assert Data.code == 0, "获取结果失败"
            assert Data.data is not None, "获取结果返回结果为空"
            assert Data.has_result == 1 and Data.total_size > 0, "未查询到预期数据,result数据结果为空"
    # def get_tcam_state_by_cloud(self, vid: str=None) -> str:
    #     """
    #     从赛博坦平台上获取TCAM的电源状态
    #     :param vid: 车辆唯一标识
    #     """
    #     if vid is None:
    #         vid = self.vid
    #     if vid is None:
    #         raise ValueError("请输入一个vid号")
    #     state_dict = {
    #         0: "待机",
    #         1: "运行",
    #         2: "休眠",
    #         3: "循环休眠1",
    #         4: "循环休眠2",
    #         5: "关闭",
    #         6: "切换备电状态",
    #     }
    #     response = requests.get(url=f"{self.cybertron_url}/getTCAMPower/{vid}")
    #     if response.status_code == 200:
    #         res = response.json()
    #         state = state_dict.get(res.get('data').get('state'))
    #         logger.info(state)
    #         return state
    #     else:
    #         raise ValueError(f"请求失败，状态码: {response.status_code}")

    def create_vsp_task(self, vin,
                              target_soft_id, 
                              skip_ecu, 
                              task_name="SOA_" + datetime.datetime.now().strftime("%m_%d-%H_%M_%S")
                              ):
        self.ota = self.ota_obj(0)
        ecuid_list = []
        soft_detail = self.ota.query_vehicle_soft_detail(vehicle_soft_id=target_soft_id)
        model_group_id = soft_detail['data']['modelId']
        logger.info(type(model_group_id))
        target_version = soft_detail['data']['vehicleSoftNumberAndVersion']
        with open('config/ecu_info_v2.0.yaml', 'r') as file:
            data = yaml.safe_load(file)
        if model_group_id == 61:
            ecu_info = data.get('mars1')
        elif model_group_id == 62:
            ecu_info = data.get('venus')
        else:
            logger.error(f"Error model_group_id:{model_group_id}")
        for ecu_skip in skip_ecu:
            ecuid = ecu_info[ecu_skip]['ecuid']
            logger.info(ecuid)
            ecuid_list.append(str(ecuid))
        result = self.ota.create_task(vin=vin, 
                             task_name=task_name,
                             target_soft_id=target_soft_id, 
                             model_group_id=str(model_group_id), 
                             target_version=target_version, 
                             no_upgrade_ecu_list=ecuid_list, 
                             is_check_self_dependency=0,
                             upgrade_method=0)
        logger.info(f'create task:{result}')
        if result['code'] == 0:
            logger.info(f'create task:{result}, task name:{task_name}')
            return True
        else:
            logger.info(f'create task:{result}, task name:{task_name}')
            return False
        
    def get_bgm_version_from_soft_detail(self, soft_id):
        self.ota = self.ota_obj(0)
        soft_detail = self.ota.query_vehicle_soft_detail(vehicle_soft_id=soft_id)
        bridge_version = {"SWPN": "", "name": "BGM"}
        for i in soft_detail['data']['appList']:
            if i['ecuName'] == 'BGM':
                logger.info(i['appList'][0]['softName'])
                logger.info(i['otherList'][0]['softName'])
                bridge_version["SWPN"] = f"{i['appList'][0]['softName']},{i['otherList'][0]['softName']}"
        if bridge_version["SWPN"] == "":
            assert False, "null bridge_version"
        else:
            logger.info(f"bridge_version: {bridge_version}")
            return bridge_version

    def get_softid_from_taskid(self, task_id):
        self.ota = self.ota_obj(0)
        task_detail = self.ota.get_task_detail(task_id)
        soft_id = task_detail["data"]["targetSoftId"]
        return soft_id
    
    def get_domain_version_from_softid(self, soft_id, domain_name: DOMAIN):
        self.ota = self.ota_obj(0)
        soft_detail = self.ota.query_vehicle_soft_detail(vehicle_soft_id=soft_id)       
        for i in soft_detail['data']['appList']:
            if i['ecuName'] == domain_name.name:
                logger.info(i['appList'][0]['softName'])
                return i['appList'][0]['softName']

    def back_vsp_to_Idle(self):
        self.ota = self.ota_obj(task_id = 1)
        try:
            for i in self.ota.get_upgrade_status_list(vin=self.vin)["data"]["list"]:
                cur_task_status = i["vehicleUpgradeStatus"]
                cur_task_id = i["taskId"]
                if cur_task_status in [VehicleUpgradeStatus.Downloading.value,
                                                VehicleUpgradeStatus.DownloadSuccess.value,
                                                VehicleUpgradeStatus.PushSuccess.value
                                                ]:
                    self.trigger_vsp_fota(VSP.Reset, 
                                        task_id=cur_task_id, vin=self.vin)
                    logger.info(f"task:{cur_task_id}, status: {cur_task_status}, execute VSP Reset")
                elif cur_task_status in [VehicleUpgradeStatus.FOTAFailCanNotDriving.value
                                                ]:
                    self.trigger_vsp_fota(VSP.UnFreeze, 
                                        task_id=cur_task_id, vin=self.vin)
                    logger.info(f"task:{cur_task_id}, status: {cur_task_status}, execute VSP UnFreeze")
                else:
                    logger.info(f"task:{cur_task_id}, status: {cur_task_status}, do nothing")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
            logger.error(e)
    
    def get_signal_mining_data(self, table_name="ods.ods_data_jade_ee_signal_qa_staging_h", dt=None, hour=None, vid=None, 
                               limit=100000, timeout: int = 600, wait_interval: int = 3):
        data = DataDev()
        if dt is None:
            dt = datetime.datetime.now().strftime("%Y-%m-%d")
        if hour is None:
            hour = datetime.datetime.now().strftime("%H")
        if vid is None:
            vid = self.vid
        data.validate_sql(table_name=table_name, dt=dt, hr=hour, vid=vid, limit=limit)
        data.run_sql()
        start_time = time.time()
        flag = True
        while flag:
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                assert False, "日志查询操作超时"
            data.get_log()
            time.sleep(wait_interval)
            if data.has_result == 1 and data.status == 2:
                flag = False
        time.sleep(wait_interval)
        data.get_result()
        if data.has_result == 1 and data.total_size > 0:
            download_file_name = data.download_result()
            return download_file_name
        
    def validate_signal_mining_data(self, vid: str = None, signame: str = None, sigvalue: str = None, message_id: str = None, 
                                    timestamp: float = None, csv_file: str = None):
        with open(csv_file, 'r', newline='') as file:
            rows = csv.DictReader(file)
            for row in rows:
                if row['httpheadervid'] == vid and row['signalname'] == signame and row['sigvalue'] == str(sigvalue):
                    t1 = int(row['sigtimestamp'][:-3].replace(".", "")) // 1000
                    t2 = int(timestamp)
                    if abs(t1 - t2) < 5:
                        logger.info(f"成功匹配到数据, signame:{signame}, timestamp:{timestamp}")
                        return True
            logger.info(f"未匹配到数据, signame:{signame}, timestamp:{timestamp}")
            return False

    def check_digital_key_result_log(self, target_value:list=[], begin_time: int = None, num: int = 25):
        """
        及时查询digital-key-service服务的log日志
        查询开始时间为调用该方法时间，查询开始时间为调用时间 -1 秒
        结束时间为最大延迟时间。(默认为25s)
        """
        index = 'jidulogapp-staging-digital-key-service-serverlog'
        service_name = 'digital-key-service'
        if not begin_time:
            begin_time = int(time.time()) - 1 # 预留1s的buff，避免上传时间到查询时间存在1s间隔
        if not target_value:
            fuzzy_query = ['LastSyncTimeForBLE:100','LastSyncTimeForEntityKey:99']
        else:
            begin_time = begin_time - 300
            fuzzy_query = target_value
        res_data = self.log_search_result(index=index,service_name=service_name,begin_time=begin_time,fuzzy_query=fuzzy_query,num=num)
        logger.info("查询到远控结果集为: {}".format(res_data))
        if res_data['total'] != 0:
            prompt_info = f"查询到远控结果集为: {fuzzy_query}"
            with allure.step(prompt_info):
                return True
        else:
            return False

    def check_task_existence(self, vin: str, soft_id: int):
        self.ota = self.ota_obj(task_id = 1)
        vehicleSoftNumberAndVersion = self.get_vehicleSoftNumberAndVersion_from_softid(soft_id=soft_id)
        logger.info(vehicleSoftNumberAndVersion)
        for i in self.ota.get_upgrade_status_list(vin=vin)["data"]["list"]:
            cur_task_status = i["targetVersion"]
            if vehicleSoftNumberAndVersion == cur_task_status and i["taskStatusName"] == "已发布":
                return True, i["taskId"]
        return False, 0

    def get_vehicleSoftNumberAndVersion_from_softid(self, soft_id: int):
        self.ota = self.ota_obj(task_id = 1)
        vehicleSoftNumberAndVersion = self.ota.query_vehicle_soft_detail(vehicle_soft_id=soft_id)["data"]["vehicleSoftNumberAndVersion"]
        return vehicleSoftNumberAndVersion

    def get_target_version_from_softid(self, soft_id: int, ecu_name: str):
        ecu_version = {}
        self.ota = self.ota_obj(task_id = 1)
        soft_version = self.ota.query_vehicle_soft_detail(vehicle_soft_id=soft_id)["data"]
        target_baseline = soft_version["vehicleSoftNumberAndVersion"]
        target_dis_baseline = soft_version["baselineName"]
        for ecu_info in soft_version["appList"]:
            if ecu_info["ecuName"] == ecu_name.upper():
                for app_info in ecu_info["appList"]:
                    ecu_version[f'{app_info["fileType"]}_version'] = app_info["softName"]
                for other_info in ecu_info["otherList"]:
                    ecu_version[f'{other_info["fileType"]}_version'] = other_info["softName"]       
        return target_baseline, target_dis_baseline, ecu_version
    
    def is_task_consuming(self, task_id: int, vin: str):
        self.ota = self.ota_obj(task_id = 1)
        for i in self.ota.get_upgrade_status_list(vin=vin)["data"]["list"]:
            taskId = i["taskId"]
            vehicleUpgradeStatus = i["vehicleUpgradeStatus"]
            if task_id != taskId and vehicleUpgradeStatus in [
                                            VehicleUpgradeStatus.Downloading.value,
                                            VehicleUpgradeStatus.DownloadSuccess.value,
                                            VehicleUpgradeStatus.PushSuccess.value
                                            ]:
                logger.info(f"{task_id} is not consuming, now {taskId} is {vehicleUpgradeStatus}, cancle it")
                return False
            elif task_id != taskId and vehicleUpgradeStatus in [
                                            VehicleUpgradeStatus.FOTAFailCanNotDriving.value,
                                            VehicleUpgradeStatus.Upgrading.value
                                            ]:
                logger.info(f"{task_id} is not consuming, now {taskId} is {vehicleUpgradeStatus}")
                return False
            else:
                logger.info(f"{task_id} , {taskId} is {vehicleUpgradeStatus}")
        return True
    
    def get_uid(self):
        "获取uid"
        headers = {  
            "Content-Type": "application/json",  
            "client": "4"  
        }  
        data = {  
            "countryCode": "86",  
            "tel": self.tel,  
            "captcha": "6825",  
            "captchaKey": __import__("os").environ['XAT_CREDENTIAL_SCAN_7667AA2977241A431C4E']  
        }  
        response = requests.post(self.token_url, headers=headers, json=data, timeout=5)
        if response.status_code == 200:
            logger.info(f'获取到的token： {response.json()}')
            self.uid = (response.json()['data']['user']['userId'])
        else:
            raise ConnectionError('获取token失败')
        return self.uid

    def rvc_realtime_battery_heat(self, op: int = 1):
        "远控电池包立即加热 (-1: 关, 1: 开)"
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 26,
            "cmdDetail": {
                "heat_battery_pack_at_once": {
                    "op": op
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id
    
    def uplaod_log_search_result(self,vid:str=None,index = 'jidulogapp-staging-*-serverlog', term_query_level:str='INFO',fuzzy_query: list = [],begin_time: int=0,end_time: int=0,size: int=10,interval_time:int =1, num:int=15, timeout:int=300):
        """
        基础查询,将查询的结果格式化后返回
        """
        if not vid:
            vid = self.vid
        url = 'https://logservice.jidustaging.com/api/search/common'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'jidu_device_id=d5725be5-2a5b-41fd-9637-8e12501abf2c'
        }
        data = {
            "index": index,
            "fuzzy_query": [f"{vid}"] + fuzzy_query,
            "begin": int(begin_time),
            "end": int(end_time),
            "from": 0,
            "size": size
        }
        res = {'total':0}
        for i in range(num):
            if not end_time:
                data['end'] = int(time.time())
            logger.info("查询的参数为: data {}".format(data))
            try:
                response = requests.post(url, headers=headers, json=data, timeout=timeout)
                logger.debug("查询TCAM上报到车云的远控结果集为: response {}".format(response))
                if response.json()["code"] == 0:  
                    res = response.json()["data"]
                    logger.debug("查询TCAM上报到车云的远控结果集为: res {}".format(res))
                    if res['total'] != 0:
                        return res
                else:  
                    logger.error("TCAM云端日志查询失败")
            except requests.exceptions.RequestException as e:  
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/tsp.py")
                logger.error("请求失败: {}".format(e))
            time.sleep(interval_time)
        if res['total'] != 0:
            assert True, '查询成功'
        else:
            assert False, f'{fuzzy_query}查询失败'
    
    def log_search_wti(self,wtiKey:str='ANP Risk Reminder',wtiFlag:str='1',num:int=25):
        begin_time = int(time.time()) - 1 # 预留1s的buff，避免上传时间到查询时间存在1s间隔
        fuzzy_query = [f"wtiKey:'{wtiKey}'",f"wtiFlag:'{wtiFlag}'"]
        res_data = self.log_search_result(index='jidulogapp-staging-remote-monitor-wti-serverlog',service_name='remote-monitor-wti',begin_time=begin_time,fuzzy_query=fuzzy_query,end_time=begin_time+3,num=num)
        logger.info("查询到WTI结果集为: {}".format(res_data))
        if res_data['total'] != 0:
            return True
        else:
            return False

    def rvc_discharge_control_soc_settings(self, lowerLimit: int = 200):
        """
        设置放电SOC
        lowerLimit : 放电下限 千分比20.0%~100.0%, 200 = 20.0%
        """
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 31,
            "cmdDetail": {
                "discharge_soc_settings": {
                    "lowerLimit": lowerLimit,
                }
            }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id
    

    def rvc_discharge_control(self, op: int = 1):
        """
        开始放电 op :1 开始放电, -1 停止放电
        """
        
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 30,
            "cmdDetail": {
                "discharge_control":
                    {
                    "op": op
                     }
                              }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id
    
    def rvc_booking_ac_charge(self, op: int = 1, chargingfull: bool = False, starttime: int = 0, endtime: int = 0):
        """
        预约交流充电
        op : 动作 int 1 新增/修改充电信息， -1 关闭预约充电
        chargingfull ：是否充到目标SOC为止，为True时，只取开始时间，不用取结束时间
        starttime : int 充电开始时间的时间戳
        endtime : int  充电结束时间的时间戳
        """
        
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 32,
            "cmdDetail": {
                "booking_ac_charge":
                    {
                        'op':op,
                        'chargingfull': chargingfull,
                        'starttime':starttime,
                        'endtime':endtime
                    }
                              }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id
        
    def check_appStatus(self, bin_name: str):
        detail_response = self.api.get_vsp_detail(bin_name)
        appStatus = detail_response['data']['data']['appStatus']
        appId = detail_response['data']['data']['appId']
        return appStatus, appId
            
    def submit_app(self, app_name: str):
        appStatus, appId = self.check_appStatus(bin_name = app_name)
        app_name_list = list(app_name)
        baseline = ["V" + f"{app_name_list[7]}" + "." + f"{app_name_list[8]}" + "." + f"{app_name_list[9]}"]
        if app_name_list[2] == "6":
            pnList = [BGM_HWPN.A_2500000095.value,
                      BGM_HWPN.A_8893802862.value,
                      BGM_HWPN.B_2500000095.value,
                      BGM_HWPN.B_8895036214.value,
                      BGM_HWPN.C_8895036214.value,
                      BGM_HWPN.D_8895036214.value,
                      BGM_HWPN.E_8895036214.value,
                      BGM_HWPN.F_8895036214.value,
                      BGM_HWPN.G_8895036214.value,
                      BGM_HWPN.H_8895036214.value,
                      BGM_HWPN.XH_8895036214.value,
                      BGM_HWPN.L_8895036214.value,
                      ]
        elif app_name_list[2] == "1":
            pnList = [TCAM_HWPN.A_8893810192.value,
                      TCAM_HWPN.A_8895036217.value,
                      TCAM_HWPN.B_8895036217.value,
                      TCAM_HWPN.C_8895036217.value,
                      TCAM_HWPN.D_8895036217.value,
                      ]            
        if appStatus == 0:
            post_body = {
                "id": appId,
                "releaseNote": "<div>自动生成</div>",
                "testReport": "<div>自动生成</div>",
                "baselineNameList": baseline,
                "modelGroupNameList": ["Mars One","Venus"],
                "soa": "soa autotest",
                "jidl": "soa autotest",
                "sdb": "soa autotest",
                "pnList": pnList,
            }
            self.api.submit_vsp(post_body, swim_lane_name="vehicle-future-sl")
            xappStatus, xappId = self.check_appStatus(bin_name = app_name)
            if xappStatus == 10:
                assert True
            else:
                assert False, f"Submit Fail with {app_name}"
        else:
            assert False, "Wrong App Status"
    
    def __get_initial_softid(self):
        #根据任务列表的taskid，估计最新的softid
        #丑陋方法，需要后续优化
        self.ota = self.ota_obj(0)
        task_list = self.ota.get_task_list()
        taskid_list = []
        softid_list = []
        for taskid in task_list['data']['list']:
            taskid_list.append(taskid['id'])
        for taskid in taskid_list:
            softid_list.append(self.ota.get_task_detail(taskid)["data"]["targetSoftId"])
        initial_softid = max(softid_list)
        logger.info(f"find initial softid by task list: {initial_softid}")
        return initial_softid

    def get_domain_type_by_app_name(self, app_name: str):
        app_name_list = list(app_name)
        if app_name_list[2] == "6":
            return "BGM"
        elif app_name_list[2] == "1":
            return "TCAM"
        else:
            assert False, "Wrong App Name"
            
    def get_softid_by_app_name(self, app_name: str):
        self.ota = self.ota_obj(0)
        initial_softid = self.__get_initial_softid()
        domain_type = self.get_domain_type_by_app_name(app_name=app_name)
        target_softid = 0
        for i in range(-50, 100):
            next_initial_softid = initial_softid + i
            soft_detail = self.ota.query_vehicle_soft_detail(vehicle_soft_id=next_initial_softid)       
            if soft_detail['code'] != 2001:
                for app in soft_detail['data']['appList']:
                    if app['ecuName'] == domain_type and \
                       app['appList'][0]['softName'] == app_name and \
                       soft_detail['data']['modelId'] == 61 and \
                       soft_detail['data']['versionStatus'] == 40:
                           target_softid = next_initial_softid
        return target_softid

    def rvc_door_control(self,door_code:DoorCode = DoorCode.driver_door_control, op: int = 1, position: int = 5):
        """
        单个电动门控制
        op : 动作(1:设置开度,2:关,3:全开)  3 为预留位
        userId ：是否充到目标SOC为止，为True时，只取开始时间，不用取结束时间
        position : int 开度值 前两门小角度为5，后两门小角度为7,可动态配置0~100
        """
        self.get_token_from_web()
        exec_id = str(int(time.time()*10))
        if door_code == DoorCode.All_door:
            return self.rvc_four_door_control(op=op,position=position)
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": door_code.value,
            "cmdDetail": {
                door_code.name:
                    {
                        'op':op,
                        'userId': self.uid,
                        'position': position
                    }
                              }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id
    

    def rvc_four_door_control(self, op: int = 1, position: int = 5):
        """
        单个电动门控制
        op : 动作(1:设置开度,2:关,3:全开)  3 为预留位
        userId ：是否充到目标SOC为止，为True时，只取开始时间，不用取结束时间
        position : int 开度值 前两门小角度为5，后两门小角度为7,可动态配置0~100
        """
        self.get_token_from_web()
        exec_id = str(int(time.time()*10))
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "vehicleModel": 61,
            "cmdCode": 37,
            "cmdDetail": {
                "four_door_control":
                    {
                        'op':op,
                        'userId': self.uid,
                        'driverPosition': position,
                        "passengerPosition":position,
                        "rearLeftPosition":position,
                        "rearRightPosition":position
                    }
                              }
        }
        self.send_rvc_cmd(self.cmd_to_pb(data))
        return exec_id

    def modify_download_net_type(self, task_id: int, download_net_type: int):
        self.ota = self.ota_obj(0)
        self.ota.modify_download_net_type(task_id=task_id, download_net_type=download_net_type)

    def rvc_set_subscribe_task(self, *arg):
        self.get_token_from_web()
        exec_id = str(int(time.time()*10))
        taskDetailList = []
        for Subscribe_task in arg:
            taskDetailList.append({
                    "slotID": Subscribe_task.slotID,
                    "status": Subscribe_task.status,
                    "cyclesType": Subscribe_task.cyclesType,
                    "AppointWeekday": Subscribe_task.AppointWeekday,
                    "startTime": Subscribe_task.startTime,
                    "cmdCode": Subscribe_task.cmdCode,
                    "cmdDetail": Subscribe_task.cmdDetail
                })
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "op": 1,
            "taskDetailList": taskDetailList}
        logger.info(f'aaaaadata: {data}')
        self.send_rvc_cmd(data, subscribe_flage=1)
        return exec_id

    def rvc_clear_subscribe_task(self):
        self.get_token_from_web()
        exec_id = str(int(time.time()*10))
        taskDetailList = [{"slotID": i, "status": -1} for i in range(2000)]
        data = {
            "execId": exec_id,
            "vid": self.vid,
            "op": 1,
            "taskDetailList": taskDetailList}

        self.send_rvc_cmd(data, subscribe_flage=1)
        return exec_id

    def log_search_subscribe_remote(self,base_remote_subscribe:BaseRemoteSubscribe ,keywords: str = "Success", execid:str="", begin_time: int = None, num: int = 25):
        """
        及时查询remote-vehicle-control服务的log日志
        查询开始时间为调用该方法时间，查询开始时间为调用时间 -1 秒
        结束时间为最大延迟时间。(默认为25s)
        """
        if not begin_time:
            begin_time = int(time.time()) - 1 # 预留1s的buff，避免上传时间到查询时间存在1s间隔
        if not execid:
            logger.info(f"execid:{execid}111111111111111111")
            begin_time = begin_time - 300
            fuzzy_query = ["sendCmd",'vehicleReportHandleErr',keywords, f'sub&{base_remote_subscribe.slotID}']
        elif execid:
            logger.info(f"execid:{execid}222222222222222222")
            fuzzy_query = ["sendCmd",'vehicleReportHandleErr',keywords, f'sub&{base_remote_subscribe.slotID}']
        else:
            logger.info(f"execid:{execid}99999999999999999")
            begin_time = begin_time - 300
            fuzzy_query = ["sendCmd",'vehicleReportHandleErr',keywords, execid, f'sub&{base_remote_subscribe.slotID}']

        # 新增msg和exectype对应关心检测
        # 判断execType
        if keywords in ['PreConditionOK','StartOK','AuthEscLockStartOK']:
            fuzzy_query += ['execType:2']
        else:
            fuzzy_query += ['execType:3']

        # 原远控msg查询
        logger.info(f"2222222222222:{begin_time}")
        res_data = self.log_search_result(begin_time=begin_time,fuzzy_query=fuzzy_query,num=num)
        logger.info("查询到远控结果集为: {}".format(res_data))
        if res_data['total'] != 0:
            return True
        else:
            return False
    
    def cloud_config_publish(self, host: str, config_instance_content: dict, task_name: str='soatest', timeout: int=60):
        """
        发布云配置。
        
        Args:
            host (str): 台架IP地址。
            config_instance_content (dict): 配置实例内容，字典形式，键为配置项名称，值为配置项值。
            格式如下：
            {
                "proname1": value1,
                "proname2": value2,
                ...
            }
            task_name (str, optional): 任务名称，默认为'soatest'。
            timeout (int, optional): 超时时间，默认为60秒。
        
        Returns:
            dict: 发布配置的结果信息。
        
        Raises:
            ValueError: 台架IP地址不在配置列表中。
            Exception: 发布配置失败或查询配置失败。
            TimeoutError: 发布配置超时。
        
        """
        # 配置默认
        content=[{"proname":"vehiclests.active","value":1},
                 {"proname":"data.collect.period","value":5,"comment":"1-60s"},
                 {"proname":"eolblock.active","value":1},
                 {"proname":"ecu.version.read.period","value":0,"comment":"0-2400h"},
                 {"proname":"ecu.version.block.active","value":1},
                 {"proname":"eic.charging.period","value":10,"comment":"1-300s"},
                 {"proname":"cabin.status.period","value":6,"comment":"1-300s"},
                 {"proname":"gnss.status","value":1,"comment":"1:enable, 0:disable"}]
        # 配置台架ip对应的config_instance_id和direct_package_id
        # 格式如下：{"台架ip":[config_instance_id, direct_package_id]}"}
        id_dict ={'172.23.20.15':[1460,651], 
                  '172.23.21.9': [1460,320], 
                  '172.18.128.80': [1460,652], 
                  '172.18.128.177': [1460,653], 
                  '172.18.129.146':  [1460,654]}
        
        for k, v in config_instance_content.items():
            for item in content:
                if k == item["proname"]:
                    item["value"] = v
                    break       
        id = id_dict.get(host, None)
        if not id:
            raise ValueError(f"{host} :台架ip不在配置列表中，请检查")
        config_instance_id, direct_package_id = id
        # 创建任务
        self.cloud_config = CloudConfigFeApi('staging')
        task_id = self.cloud_config.create_task_fromInstance_add_task_publish(
            configInstanceId=config_instance_id,
            directPackageId=direct_package_id,
            taskName=task_name,
            configInstanceContent=content
        )
        if not task_id:
            raise Exception(f"下发配置失败:{config_instance_content}")
        query_data = {
            "pageNo": 1,
            "pageSize": 100,
            "taskId": task_id
        }
        time.sleep(2)
        time_start = time.time()
        while True:
            if time.time() - time_start > timeout:
                raise TimeoutError(f"下发配置超时：{timeout} seconds.")
            res = self.cloud_config.subtask_query(query_data)
            if res.get('code') == 0:
                logger.info(f"下发配置查询成功, task_id: {task_id},data: {res['data']}")
                # 'resultStage': 6, 'resultStatus': 1
                if res['data']['list'][0]['resultStage'] == 6 and res['data']['list'][0]['resultStatus'] == 1:
                    logger.info(f"下发配置车端应用成功, task_id: {task_id},data: {res['data']}")
                    return res['data']['list'][0]
                else:
                    time.sleep(2)
            else:
                raise Exception(f"下发配置查询失败, task_id: {task_id}, res: {res}")
            
