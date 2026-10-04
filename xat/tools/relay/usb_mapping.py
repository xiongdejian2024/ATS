#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :usb_mapping.py
@time         :2/29/24 14:28
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import os.path
import re
import subprocess

import serial.tools.list_ports
import serial


def get_tty_location_mapping():
    # 3-7.1 ---- ttyUSB0
    print('获取ttyUSB与LOCATION的mapping')
    tty_location_dict = {}
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} [{hwid}]")
        tty = port
        location = re.findall(r'LOCATION=(.*)', hwid)
        if location:
            location = location[0].split('/')[-1]
            tty_location_dict[location] = tty
    return tty_location_dict


def get_kernels_symlink_mapping():
    # /dev/USB_PWM --- 3-7.1
    print('获取KERNELS与SYMLINK+的mapping')
    tty_symlink_dict = {}
    if os.path.exists('/etc/udev/rules.d/99-usb-serial.rules'):
        with open('/etc/udev/rules.d/99-usb-serial.rules') as f:
            for line in f:
                print(line)
                location = re.findall(r"KERNELS==\"(.*?)\"", line)
                usb = re.findall(r"SYMLINK\+=\"(.*?)\"", line)
                if location and usb:
                    location = location[0]
                    usb = f"/dev/{usb[0]}"
                    tty_symlink_dict[usb] = location
    return tty_symlink_dict


def print_mapping():
    res = subprocess.check_output("ls -lrt /dev/USB* | awk '{print $9 $10 $11}'", shell=True)
    output = res.decode()
    print(output)
    return output


def get_mapping_error():
    error_mapping = []
    output = print_mapping()
    for line in output.split('\n'):
        if '->' in line:
            usb, tty = line.split('->')
            if not tty.startswith('ttyUSB'):
                error_mapping.append(usb)
    return error_mapping


def recover_mapping(tty, usb):
    cmd = f"sudo ln -sf {tty} {usb}"
    print(f'执行{cmd}')
    res = os.system(cmd)
    if res != 0:
        print(f"sudo ln -sf {tty} {usb}执行失败")


if __name__ == '__main__':
    tty_location_dict: dict = get_tty_location_mapping()
    kernels_symlink_dict: dict = get_kernels_symlink_mapping()
    error_mapping: list = get_mapping_error()
    if error_mapping:
        print(f'找到mapping混乱的ttyUSB')
        for usb in error_mapping:
            location = kernels_symlink_dict[usb]
            tty = tty_location_dict[location]
            recover_mapping(tty, usb)
    else:
        print('usb mapping配置正确')
    print_mapping()
