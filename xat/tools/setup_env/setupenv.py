# -*- coding: utf-8 -*-
"""
@File        : setupenv.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/09/23 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""

import os
import sys

if __name__ == "__main__":
    args = sys.argv[1:]
    cmd = 'cd tools/setup_env && ./setupenv.sh'
    if args:
        args_str = " ".join(args)
        cmd += f" {args_str}"
    else:
        cmd = 'cd tools/setup_env && ./setupenv.sh'
    print(f"当前执行命令是{cmd}")
    res = os.system(cmd)
    if res != 0:
        raise SystemExit('执行setupenv.sh失败')
