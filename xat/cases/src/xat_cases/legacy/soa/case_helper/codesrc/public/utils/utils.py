#!/usr/bin/python3
# -*- coding=utf-8 -*-
# (C) Copyright Jidu Auto 2023-2023.
# @author: Edison

'''
架构元素：code/public/utils

dependencies:
    python(>=3.5)
'''

import os
import sys
import subprocess
from .log import logger, get_base_path


def get_platform():
    from platform import system

    return system()


SYSTEM_ATTR = get_platform()


def run_cmd(cmd: str, env=None, stop=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    res = None
    try:
        if get_platform() == 'Windows':
            res = subprocess.run(cmd, env=env, shell=True, check=check, stdout=stdout, stderr=stderr)
        else:
            res = subprocess.run(cmd, env=env, shell=True, check=check, stdout=stdout, stderr=stderr)
    except subprocess.CalledProcessError as e:
        res = e
        logger.error(f'Command failed with return code {e.returncode}')
        if stop:
            sys.exit(-1)
    return res


# 支持多组命令（如果需要返回值的话，建议使用run_cmd）
def run_cmds(cmds: list, env=None):
    for _cmd in cmds:
        run_cmd(_cmd, env=env)


def load_cfgs(path, encoding='utf-8') -> dict:
    from json import load

    with open(path, 'r', encoding=encoding) as f:
        data = load(f)
    return data


def clear_dir(path, keep=True):
    from shutil import rmtree

    if os.path.exists(path):
        rmtree(path)
    if keep:
        os.mkdir(path)


def do_chmod(path, mod, recursive=False):
    '''
    @desp: chmod
    @usage: do_chmod('[path]', 0o755, recursive=True)
    '''
    if not recursive:
        os.chmod(path, mod)
    else:
        for _root, dirs, files in os.walk(path):
            for d in dirs:
                do_chmod(os.path.join(_root, d), mod)
            for f in files:
                do_chmod(os.path.join(_root, f), mod)


def get_env():
    ld_library_path = os.path.join(get_base_path(), 'lib')
    path = os.path.join(get_base_path(), 'bin')

    if get_platform() == 'Windows':
        path = f'{path}; {os.environ["PATH"]}'
    else:
        path = f'{path}: {os.environ["PATH"]}'
    return {**os.environ, 'LD_LIBRARY_PATH': ld_library_path, 'PATH': path}


def save_results(workspace, component_name, contents: dict = {'errcode': 2, 'results': None}):
    '''
    用于 SOA_God 组件集成
    协议字段参考：https://wiki.jiduauto.com/pages/viewpage.action?pageId=534297660
    @param workspace: 路径
    @param component_name: 组件名，需与exe名保持一致
    @param contents: 协议体
        @field errcode: 错误码（0表示成功，1表示失败， 2表示进行中）
        @field results: 结果
    '''
    from json import dumps

    full_contents = {'header': component_name, 'body': contents}

    path = os.path.join(workspace, f"{component_name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json_str = dumps(full_contents)
        f.write(json_str)


def copy_file(source_file, destination_dir):
    '''
    @desp: 复制单个文件至目标目录下
    @param source_file: 目标文件
    @param destination_dir: 目标目录
    '''
    import shutil

    # 检查源文件是否存在
    if not os.path.isfile(source_file):
        logger.error(f"error: source file '{source_file}' does not exist")
        return
    # 检查目标目录是否存在
    if not os.path.isdir(destination_dir):
        logger.error(f"error: target file '{destination_dir}' does not exist")
        return
    # 使用shutil模块的copy2函数来拷贝文件，覆盖同名文件
    try:
        shutil.copy2(source_file, destination_dir, follow_symlinks=True)
    except Exception as e:
        logger.error(f"error: {e}")


def get_host_ip():
    '''
    @desp: 获取本机IP地址方法
    '''

    from socket import socket, AF_INET, SOCK_DGRAM

    try:
        with socket(AF_INET, SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            host_ip = s.getsockname()[0]
        logger.info(f'host ip 获取 success: {host_ip}')
        return host_ip
    except Exception as e:
        logger.error(f'host ip 获取 failed: {e}')
        return None
