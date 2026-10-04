# -*- coding: utf-8 -*-
"""
@File        : test_flash_bgm
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/3/1 13:34
@Description :

"""

import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_ecu.legacy.common.logger import logger


def exec_shell(command):
    import subprocess
    try:
        # 执行命令
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 等待命令执行完成
        process.wait()
        # 获取命令的输出和错误信息
        output = process.stdout.read()
        error = process.stderr.read()
        # 将输出和错误信息解码为字符串
        output = output.decode(encoding="utf-8")
        error = error.decode(encoding="utf-8")
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/util/clear_willow_log.py")
        output = ""
        error = str(e)
    # 返回命令的输出和错误信息
    result = {"output": output, "error": error}
    logger.info(result)
    return result


def get_sys_left_space(command=None):
    '''
    获取 剩余空间
    :return:
    '''
    if command is None:
        command = "df -h"
    # 执行查询 磁盘空间指令
    result = exec_shell(command)
    data = result["output"]
    error = result["error"]
    if not data:
        logger.error(f"获取磁盘剩余空间失败:{error}")
        return 0
    try:
        out_list = [i for i in data.split("\n")]
        aaa = [i.split() for i in out_list]
        res_lis = []
        for each_lis in aaa[1:]:
            # 处理空格
            lis = [i for i in each_lis if i.strip()]
            # 长度为6， 文件系统   容量  已用  可用 已用%  挂载点
            if len(lis) == 6:
                # 文件名称以 /dev 开头
                start_str = lis[0].startswith('/dev')
                space = float(lis[1][:-1]) > 100 and (lis[1].endswith('G') or lis[1].endswith('T'))
                if start_str and space:
                    res_lis.append(lis)
        if len(res_lis):
            use = int(float(res_lis[0][4][:-1]))
            return 100 - use
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/util/clear_willow_log.py")
        logger.error(f"解析磁盘剩余空间失败{str(e)}")
        return 0
    return 0


def delete_willow_log(**kwargs):
    '''
    删除 willow 日志
    @return:
    '''
    # 存放 willow_log 的路径
    willow_log_path = kwargs.get("willow_log_path", "/root/autotest/willow/")
    save_num = kwargs.get("save_num", 10)
    cmd = f"cd {willow_log_path};ls -lrt"

    result = exec_shell(cmd)
    data = result["output"]
    error = result["error"]
    if data:
        output_lis = data.split("\n")
        print(len(output_lis), output_lis)
        name_list = [na.split(' ')[-1] for na in output_lis[1:]]

        name_list = [i for i in name_list if i.strip()]
        logger.error(f"name_list={name_list}")
        # 需要保留的 日志
        save_log_list = []

        for namestr in name_list:
            if namestr.endswith('zip'):
                continue
            if len(save_log_list) >= save_num:
                break
            save_log_list.append(namestr)

        # 删除 文件
        for del_name in name_list:
            if del_name in save_log_list:
                continue
            path = os.path.join(willow_log_path, del_name)
            logger.info(f"删除的文件为 path={path}")
            cmd = f"rm -rf {path}"
            os.system(cmd)
    pass


def test_clear_log():
    res = get_sys_left_space()
    logger.info(f"left space {res}")
    if res < 10:
        delete_willow_log(save_num=10)
    res = get_sys_left_space()
    logger.info(f"left space {res}")
    if res < 10:
        assert 0, "清理失败"

    #


if __name__ == "__main__":
    test_clear_log()
