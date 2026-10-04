#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: encrypt.py
@Time: 2022/6/8 12:48
@Author: lei.tao
@Software: PyCharm
@Description: Encrypt packages
@Examples: 
"""
import os
import sys

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from xat_ecu.legacy.common.logger import logger
from tools.encrypt.env import *


class Encrypt(object):
    def __init__(self, filepath):
        """
        刷写包加密成bin包
        :param file: 未加密的文件
        :return: None
        """
        self.filepath = filepath
        self.jar = "encrypt-make-dep.jar"

    def start(self):
        command = f'java -jar -DfilePath={self.filepath} -DecuName=bgm ./ ecu_simulator/interface/encrypt/{self.jar}'
        logger.info("Encrypt package command:{}".format(command))
        try:
            if ISWINDOWS:
                os.system(command)
            else:
                os.system(
                    f"export PATH=$PATH:{PYTHON_LIB} && export LD_LIBRARY_PATH=LD_LIBRARY_PATH:{PYTHON_LIB} && {command}")
            logger.info(f'Encrypt success')
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/encrypt/encrypt.py")
            logger.info(f'Encrypt failed with error {e}')


if __name__ == '__main__':
    file = '6160110055AAP.vbf'
    file_path = f'test_case/smoke_test/package/' + file
    Encrypt(file_path).start()
