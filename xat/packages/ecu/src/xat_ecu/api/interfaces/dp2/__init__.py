#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :__init__.py.py
@Time         :2024/10/21 11:34
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
# 导入所有常量
from .base_common.constants.common_data import *
from .basetech.constants.common_data import *
from .cd_mcu.constants.common_data import *
from .cd_soc.constants.common_data import *
from .cd_service.constants.common_data import *
from .connectivity_vo.constants.common_data import *
from .lcu.constants.common_data import *
from .nad.constants.common_data import *
from .service_vo.constants.common_data import *

# 导入日志
from xat_ecu.legacy.common.logger import logger
