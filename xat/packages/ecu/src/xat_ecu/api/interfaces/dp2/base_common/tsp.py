#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :tsp.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :云端能力模拟 实现接口
"""
import os
import sys
import time

import requests
from tqdm import tqdm
from datetime import datetime
from xat_ecu.legacy.common.logger import logger
from xat_ecu.api.interfaces.dp2.interface import CommonTsp


class Tsp(CommonTsp):

    def download_file_to_nuc(self, file_type, file_name=None, local_path="/root/", host="172.18.36.24", port=8000):
        now_time = str(time.time() * 10 ** 3).split(".")[0]
        response = requests.get(f"http://{host}:{port}/{file_type}?json=true&_={now_time}", verify=False)
        if file_name:
            if file_name not in [info["name"] for info in response.json()["files"]]:
                logger.warning(f"输入指定下载的file没有发现，请仔细核对。")
                assert False

        max_file_time = 0
        if not file_name:
            file_name = None
            try:
                for info in response.json()["files"]:
                    file_time = info["name"].split(".")[0].split("_")[1]
                    timestamp = datetime.strptime(file_time, '%Y%m%d').timestamp()
                    if timestamp > max_file_time:
                        file_name = info["name"]
                        max_file_time = timestamp
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp2/base_common/tsp.py")
                logger.error(f"获取forward文件失败：{e}")
                assert False
            if not file_name:
                logger.error(f"没有获取到mcu forward文件")
                assert False

        download_url = f"http://{host}:{port}/{file_type}/{file_name}?download=true"
        response = requests.get(download_url, verify=False, stream=True)
        local_file_path = os.path.join(local_path, file_name)
        total_size = int(response.headers.get("content-length", 0))
        progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)
        logger.info(f"开始下载文件...")
        try:
            with open(local_file_path, 'wb') as fd:
                for chunk in response.iter_content(10240):
                    if chunk:
                        fd.write(chunk)
                        progress_bar.update(len(chunk))
            logger.info(f"文件下载完成...")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp2/base_common/tsp.py")
            os.remove(local_file_path)
            raise e
        finally:
            progress_bar.close()

        return local_file_path

    def download_mcu_forwarder_to_nuc(self, host="172.18.36.24", port=8000, local_path="/root/"):
        """
        下载mcu forward工具到上位机
        :param host:
        :param port:
        :param local_path:
        :return:
        """
        return self.download_file_to_nuc(file_type="mcu_forward_tool",
                                         host=host,
                                         port=port,
                                         local_path=local_path
                                         )

    def download_partner_to_nuc(self, host="172.18.36.24", port=8000, local_path="/"):
        """
        下载dp2依赖的partner到上位机
        :param host:
        :param port:
        :param local_path:
        :return:
        """
        return self.download_file_to_nuc(file_type="partener_tool",
                                         host=host,
                                         port=port,
                                         local_path=local_path
                                         )
