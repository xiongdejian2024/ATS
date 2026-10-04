# -*- coding: utf-8 -*-
"""
@File        : cybertron_api.py
@Author      : 
@Time        : 2024-11-06 16:00
@Description : 封装赛博坦平台相关的接口

"""
import json
import time
import base64

import requests
import diskcache

from xat_ecu.legacy.common.logger import logger
from groot2 import AuthManager

# 缓存过期时间, 单位: 秒
CACHE_EXPIRE = 3
# 赛博坦平台账号
CYBERTRON_USER_NAME = 'b196aHVhbmd6aHVhbmcuaHVhbmc='
# 赛博坦平台密码
CYBERTRON_PASSWORD = __import__("os").environ.get('XAT_CREDENTIAL_ECU__INTERFACE_CYBERTRON_CYBERTRON_API_PY_CYBERTRON_PASSWORD', "")
# 赛博坦平台URL前缀
URL_PREFIX = "https://platform-vehicle.jidustaging.com/api/vehicle-platform/admin"
# URL前缀，获取token时用到
ENDPOINT = "https://passport.jidustaging.com/api/passportb"


class CybertronApi:

    def __init__(self, env_name="staging"):
        self.env_name = env_name
        self.user_name = base64.b64decode(CYBERTRON_USER_NAME).decode('utf-8')
        self.password = base64.b64decode(CYBERTRON_PASSWORD).decode('utf-8')
        
        self.url_prefix = URL_PREFIX
        
        self.headers = {
            "authorization": self.get_token(),
            "Content-Type": "application/json;charset=UTF-8",
        }

    def get_token(self):
        """获取 cybertron 平台 passportb token

        Returns:
            str: cybertron token.
        """
        with diskcache.Cache("/tmp/cybertron_cache_data") as cache:
            data = cache.get("cybertron_cache_data")
            if (
                data is None
                or "timestamp" not in data
                or time.time() - data["timestamp"] >= CACHE_EXPIRE
            ):
                # 如果缓存不存在或已过期，重新获取数据
                logger.debug("get cybertron token from passportb")
                userinfo = {
                    "user_name": self.user_name,
                    "password": self.password,
                    "client_id": "0c39c12e8c134d47",
                    "endpoint": ENDPOINT,
                    "client_secret": __import__("os").environ.get('XAT_CREDENTIAL_ECU__INTERFACE_CYBERTRON_CYBERTRON_API_PY_CLIENT_SECRET', "")
                }
                data = AuthManager().get_vehicle_platform_token(env_name=self.env_name, userinfo=userinfo)
                logger.info(f"get_vehicle_platform_token {data=}")
                if "token" in data:
                    cybertron_token = data["token"]
                    # 更新缓存
                    cache.set(
                        "cybertron_cache_data",
                        {"cybertron_token": cybertron_token, "timestamp": time.time()},
                    )
                    return cybertron_token
                else:
                    logger.error(f"get cybertron token error: {data}")
                    return None
            else:
                # 如果缓存存在且未过期，直接返回缓存中的数据
                logger.debug("get cybertron token from local disk cache")
                return data["cybertron_token"]
    
    def _post(self, path: str, data: dict):
        """发送 post 请求

        Args:
            path (str): 请求路径.
            data (dict): post body.

        Returns:
            dict: response.
        """
        url = f"{self.url_prefix}{path}"
        ret = requests.post(url=url, data=json.dumps(data), headers=self.headers)
        json_ret = ret.json()
        return json_ret
    
    def _get(self, path: str):
        """发送 get 请求

        Args:
            path (str): 请求路径.

        Returns:
            dict: response.
        """
        url = f"{self.url_prefix}{path}"
        ret = requests.get(url=url, headers=self.headers)
        json_ret = ret.json()
        return json_ret

    def get_platform_info_by_vin(self, vin: str):
        """获取车辆综合信息列表页

        Args:
            vin (str): 车辆VIN.

        Returns:
            dict: 车辆综合信息.
        """
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "vin": vin
        }
        ret_json = self._post(path="/vehicleInfo/queryPage", data=data)
        if ret_json.get('msg') == "成功":
            logger.info(f"获取车辆综合信息成功，{ret_json=}")
            return ret_json.get('data').get('info')[0]
        else:
            logger.error(f'获取车辆综合信息失败，{ret_json=}')
            
            
    def get_car_by_platform_id(self, platform_id):
        """获取车辆基本信息

        Args:
            platform_id (str): cybertron平台platform_id.

        Returns:
            dict: 车辆基本信息.
        """
        ret_json = self._get(path=f"/vehicleInfo/query/{platform_id}")
        if ret_json.get('msg') == "成功":
            logger.info(f"获取车辆详情成功，{ret_json=}")
            return ret_json.get('data')
        else:
            logger.error(f'获取车辆详情失败，{ret_json=}')

    def get_platform_id_by_vin(self, vin: str):
        """获取cybertron平台platform_id

        Args:
            vin (str): 车辆VIN.

        Returns:
            int: platform_id.
        """
        logger.info(f"get_platform_id_by_vin {vin}")
        car_info = self.get_platform_info_by_vin(vin=vin)
        return car_info.get('id')

    def get_ecu_by_vin(self, vin: str):
        """获取车辆ecu信息

        Args:
            vin (str): 车辆VIN.

        Returns:
            dict: 车辆ecu信息.
        """
        logger.info(f"get_ecu_by_vin {vin=}")
        platform_id = self.get_platform_id_by_vin(vin=vin)
        data = {
            'id': platform_id
        }
        ret_json = self._post(path="/vehicleEcu/queryList", data=data)
        if ret_json.get('msg') in ["成功", ""]:
            logger.info(f"获取车辆ecu信息成功，{ret_json=}")
            return ret_json.get('data').get('ecuList')
        else:
            logger.error(f'获取车辆ecu信息失败，{ret_json=}')
            return None

    def get_car_status(self, vin: str, type: int = 3, platform_id: str = ""):
        """获取车辆详情

        """
        if not platform_id:
            platform_id = self.get_platform_id_by_vin(vin=vin)
        data = {
            "id": platform_id,
            "type": type
        }
        ret_json = self._post(path="/vehicle/shadow/show", data=data)
        if ret_json.get('msg') == "success":
            # logger.info(f"获取车辆详情成功，{ret_json=}")
            car_info = dict()
            car_info['platform_id'] = platform_id
            logger.info(ret_json.get('data'))
            for i in ret_json.get('data'):
                for t in i.get("items")[0]:
                    car_info[t.get('label')] = t.get('value')
                car_info[i.get('groupName')] = i.get('updateTime')
            return car_info
        else:
            logger.error(f'获取车辆详情失败，{ret_json=}')

    def get_vehicle_use_model(self, vin: str):
        """获取车辆使用模式

        Args:
            vin (str): 车辆VIN.

        Returns:
            str: 车辆使用模式.
        """
        vehicle_status_list = self.get_vehicle_status(vin=vin)[-1].get('data')
        veh_model_list = []
        for i in vehicle_status_list:
            for sta_name, sta_value in i.items():
                if sta_value == "车辆模式":
                    # logger.info(i['items'][0])
                    for model in i['items'][0]:
                        veh_model_list.append(model)
                else:
                    continue
        if len(veh_model_list) < 1:
            return None
        for i in veh_model_list:
            for key,value in i.items():
                if value == "使用模式":
                    veh_use_model = i['value']
                    logger.info(i['value'])
                    return veh_use_model
            
        
    def get_vehicle_status(self, vin: str,platform_id: str = ""):
        """获取车辆实时状态

        """
        if not platform_id:
            platform_id = self.get_platform_id_by_vin(vin=vin)
        data = {
            "id": platform_id,
            "type": 1}
        ret_json = self._post(path="/vehicle/shadow/show", data=data)
        if ret_json.get('msg') == "success":
            # logger.info(f"获取车辆详情成功，{ret_json=}")
            return True, ret_json
        else:
            logger.error(f'获取车辆详情失败，{ret_json=}')
            return False, ret_json


    def get_car_info(self, vin: str):
        """获取车辆当前状态(部分信息)
        Args:
            vin (str): 车辆VIN.

        Returns:
            dict: 车辆当前状态信息(部分信息).
        """
        car_info = self.get_platform_info_by_vin(vin=vin)
        car_status = self.get_car_status(vin=vin)
        car_info.update(car_status)
        # logger.info(f"{car_info=}")
        return car_info

    def get_car_base(self, vin: str, platform_id: str = "", type: int = 1):
        """获取车辆当前状态(详细信息)
        
        """
        if not platform_id:
            platform_id = self.get_platform_id_by_vin(vin=vin)
        car_base = self.get_car_by_platform_id(platform_id=platform_id)
        car_status = self.get_car_status(vin=vin, type=type)
        car_mile = self.get_car_status(vin=vin)
        car_base.update(car_status)
        car_base.update(car_mile)
        return car_base
    
    def get_vid_by_vin(self, vin):
        """根据车辆VIN获取车辆VID

        Args:
            vin (str): 车辆VIN.

        Returns:
            str: 车辆VID.
        """
        return self.get_car_info(vin=vin).get('vid')
    

if __name__ == "__main__":
    cy_helper = CybertronHelper()
    cy_helper.get_car_status(vin='L6T79T4E4PD000308', type=4)
    cy_helper.get_platform_info_by_vin(vin='L6T79T4E4PD000308')
    cy_helper.get_vehicle_status(vin='L6T79T4E4PD000308')
    cy_helper.get_vehicle_use_model(vin='L6T79T4E4PD000308')
    
    # vin_list = ['L6T79T4E4PD000308']
    # platform_vehicle = CybertronHelper()
    # for vin in vin_list:
    #     car_info = platform_vehicle.get_ecu_by_vin(vin=vin)
    #     logger.info(car_info)