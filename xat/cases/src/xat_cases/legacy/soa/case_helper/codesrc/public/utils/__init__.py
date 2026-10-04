#!/usr/bin/python3
# -*- coding=utf-8 -*-
# (C) Copyright Jidu Auto 2023-2023.
# @author: Edison

"""
架构元素：code/public/utils

dependencies:
    python(>=3.5)
"""

from .log import logger, get_base_path
from .utils import *
from .disk_manager import DiskCleaner
from .connection import RemoteTools, RemoteToolsAdb
from .conf_parser import load_settings, load_custom_settings


if __name__ == "__main__":
    logger.info(get_base_path())
