# -*- coding: utf-8 -*-
"""
@File        : bgm_adb.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/03/09 5:10 PM
@Description : description about this file
@Examples    : example of how to use it
"""

import sys
import os
import time
project_root = __import__("xat_ecu.resources", fromlist=["LEGACY_ROOT"]).LEGACY_ROOT.as_posix()
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.driver.adb_client import *


class BgmAdb():
    def __init__(self, host, port):
        Adb(host, port)
