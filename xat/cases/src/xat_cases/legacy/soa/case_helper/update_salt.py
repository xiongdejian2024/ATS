# -*- coding: utf-8 -*-

import json
import os
import re
import time
# from ecu_simulator.driver.can_listener import current_path
# project_root = os.path.dirname(os.path.dirname(current_path))
# print(project_root)

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat/venv/lib/python3.8/site-packages')
soa_partner_base = os.path.join(project_root, 'ecu_simulator', 'soa_partner')
idl_base = os.path.join(soa_partner_base, 'BootesRelease', 'idl')
backup_dir = os.path.join(soa_partner_base, 'backup')
BootesRelease_dir = os.path.join(soa_partner_base, 'BootesRelease')



def get_set_salt(key, value):
    print(f"开始修改salt.json文件，key:{key}, value:{value}")
    salt_path = os.path.join(project_root, "ecu_simulator/soa_partner/BootesRelease/out/x86/conf/salt.json")
    with open(salt_path, mode="r", encoding="utf-8") as salt:
        result = json.load(salt)
        print(result)
        if key in ["aes_key", "aes_iv", "cmac_key"]:
            result.update({key: value})
        else:
            print(f"键 {key} 不存在")
            return False

    with open(salt_path, mode="w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)
        print(f"修改成功，key：{key}, value:{value}")
        return True


def update_security_level(jidl_name="account_service.jidl", interface_name="NotifyAccountsAuthority",
                          new_security_level=1):
    """针对某个服务的接口修改加密等级"""
    flag, abs_path = _get_file_in_dir(idl_base, jidl_name)  # 如果flag为True，则abs_path为jidl文件的绝对路径
    if not flag:
        raise FileNotFoundError(f"未找到{jidl_name}文件")
    else:
        print(f"读取JIDL文件：{abs_path}")
        data_list = []
        with open(abs_path, "r") as f:
            for line in f.readlines():
                data_list.append(line)
        # 遍历查找接口
        for i, data in enumerate(data_list):
            if f" {interface_name}(" in data:  # 查找接口有无特定的加密等级
                index_for_method_or_event = False
                for index in [i - 1, i - 2, i - 3]:  # 在接口往上三行找security
                    if "@event" in data_list[index] or "@method" in data_list[index]:
                        index_for_method_or_event = index
                    if "@security" in data_list[index]:
                        data_list[index] = re.sub(r"\d", str(new_security_level), data_list[index])
                        break
                else:  # 在没有被break中断的情况下执行，说明这个接口没有特定加密等级
                    # 强行加一行
                    null_count = len(data) - len(data.lstrip())  # 计算左侧缩进
                    data_list.insert(index_for_method_or_event + 1, f'{" " * null_count}@security({new_security_level})\n')
                break
        else:
            raise KeyError(f"{abs_path}未找到接口{interface_name}")
        print(f"==========开始更新{jidl_name}文件==========")
        with open(abs_path, "w") as f:  # todo
            for data in data_list:
                f.write(data)
        time.sleep(1)


def run_cmd(cmd):
    """执行指定指令"""
    res = os.system(cmd)
    if res == 0:
        print(f"执行{cmd} 成功")
    else:
        raise OSError(f"执行 {cmd} 失败")


def backup_service(idl_name):
    """
    针对指定服务编译前先备份服务
    param idl_name: 特定idl文件名称，如KeyService.jidl
    """
    flag, abs_path = _get_file_in_dir(idl_base, idl_name)  # 如果flag为True，则abs_path为jidl文件的绝对路径
    if not flag:
        raise FileNotFoundError(f"未找到{idl_name}文件")
    dst = os.path.join(backup_dir, 'bin')
    if not os.path.isdir(dst):
        os.makedirs(dst)
    run_cmd(f"cd {soa_partner_base};cp {abs_path} backup")
    origin_dir = f"BootesRelease/out/x86/bin/{idl_name.replace('.jidl', '')}"
    dst_back_dir = os.path.join(backup_dir, f"bin/{idl_name.replace('.jidl', '')}")
    if os.path.isdir(dst_back_dir):
        run_cmd(f'rm -rf {dst_back_dir}')
    run_cmd(f"cd {soa_partner_base};mv {origin_dir} backup/bin/")


def backup_partner_config():
    """备份BootesRelease/out/x86/conf/目录"""
    if not os.path.isdir(backup_dir):
        os.makedirs(backup_dir)
    origin_dir = f"BootesRelease/out/x86/conf/"
    run_cmd(f"cd {soa_partner_base};cp -r {origin_dir} backup/")


def reset_soa_partner():
    """
    恢复soa partner构建目录，建议放在after class 里
    """
    if os.path.isdir(backup_dir):
        for dir_name in os.listdir(backup_dir):
            curr_dir = os.path.join(backup_dir, dir_name)
            if ".jidl" in dir_name:
                flag, abs_path = _get_file_in_dir(idl_base, dir_name)  # 如果flag为True，则abs_path为jidl文件的绝对路径
                if not flag:
                    raise FileNotFoundError(f"未找到{dir_name}文件")
                run_cmd(f"cd {soa_partner_base};mv {curr_dir} {os.path.dirname(abs_path)}")
            else:
                run_cmd(f"cd {soa_partner_base};cp -r {curr_dir} BootesRelease/out/x86/bin")  # todo
    else:
        print("没有找到备份目录，无法恢复")


def rebuild_soa_partner(jidl_file=""):
    """
    针对单个jidl进行编译
    jidl_file：需要构建的JIDL文件名称，如KeyService.jidl
    """
    result = os.popen(f"cd {BootesRelease_dir};./CarinaToolsUtils/bin/soa_partner -r ./ -s CarinaX86_64/ build {jidl_file};sync")
    for data in result.readlines():
        print(data, end='')
        if 'res 0' in data:
            print(f"{jidl_file} 编译成功")  # todo
            break
    else:
        raise OSError(f"{jidl_file} 编译失败")


def _get_file_in_dir(dir_path, jidl_name):
    """
    内部函数：获取目录下的所有文件
    """
    if not os.path.exists(dir_path):
        print(f"文件不存在")
        return
    listName = os.listdir(dir_path)
    for fileDirName in listName:
        abspath = os.path.join(dir_path, fileDirName)
        if os.path.isfile(abspath):
            if jidl_name in abspath:
                return True, abspath
        if os.path.isdir(abspath):
            result2, detail2 = _get_file_in_dir(abspath, jidl_name)
            if result2:
                return result2, detail2
    else:
        return False, "JIDL 文件不存在"


if __name__ == '__main__':
    # backup_service("DoorService.jidl")
    # update_security_level("DoorService.jidl", "FrntLeftDoorSts", 1)
    # update_security_level("DoorService.jidl", "GetAntiPinch", 0)
    rebuild_soa_partner("DoorService.jidl")
    pass