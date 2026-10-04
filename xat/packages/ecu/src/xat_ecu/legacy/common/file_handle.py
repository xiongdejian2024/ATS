# -*- coding: utf-8 -*-
"""
@File        : file_handle.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022/04/04 23:41
@Description :
@Examples    :
"""

import os
import pathlib
# sat Project
current_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = __import__("xat_ecu.resources", fromlist=["LEGACY_ROOT"]).LEGACY_ROOT.as_posix()   #  不推荐使用

ecu_simulator_abspath = __import__("xat_ecu.resources", fromlist=["LEGACY_ROOT"]).LEGACY_ROOT.as_posix()    # 推荐

# os.makedirs()   可以同时创建多级目录
# os.path.exists() 方法来检测文件/文件夹是否存在：


class FileHandle:
    def __init__(self):
        pass

    @staticmethod
    def get_file_paths_from_dir(dir_path):
        file_paths = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_paths.append(os.path.join(root, file))
        return file_paths

    @staticmethod
    def get_subdir_names_from_dir(dir_path):
        subdir_names = []
        for root, dirs, files in os.walk(dir_path):
            for subdir in dirs:
                subdir_names.append(subdir)
        return subdir_names

    @staticmethod
    def get_file_name_and_paths_from_dir(dir_path):
        file_name_and_paths = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_name = os.path.splitext(file)[0]
                file_name_and_paths.append((file_name, file_path))
        return file_name_and_paths

    @staticmethod
    def get_file_names_from_dir(dir_path):
        file_names = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_name = os.path.splitext(file)[0]
                file_names.append(file_name)
        return file_names

    @staticmethod
    def get_file_names_from_dir_except_cpython(dir_path):
        file_names = FileHandle.get_file_names_from_dir(dir_path)
        file_names = [file_name for file_name in file_names if "cpython" not in file_name]
        return file_names

    @staticmethod
    def get_parent_dir():
        # sat Project
        current_path = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.environ.get("XAT_PROJECT_ROOT", str(pathlib.Path(__file__).resolve().parents[1]))
        return parent_dir

    @staticmethod
    def makedirs(path: str):
        #  parents 参数，设置为 True 可以创建多级目录；不设置则只能创建 一层
        # 主要功能：判断文件是否存在，不存在则创建，支持多级文件夹创建；
        path = pathlib.Path(path)
        if not path.is_dir():
            path.mkdir(parents=True)

