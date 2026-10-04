#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
import os
import sys
import platform


is_py2 = (sys.version_info[0] == 2)
is_py3 = (sys.version_info[0] == 3)

ISWINDOWS = (platform.system() == "Windows")
ISLINUX = (platform.system() == "Linux")
ISMAC = (platform.system() == "Darwin")

if ISWINDOWS and is_py3:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# python环境默认保存在用户根目录
AUTOTEST_DIR = os.path.join(os.path.expanduser('~'), "autotest")
if not os.path.exists(AUTOTEST_DIR):
    os.makedirs(AUTOTEST_DIR)
PYTHON_ENV_DIR = os.path.join(AUTOTEST_DIR, "python_env")

PYTHON_VERSION = "3.8.9"
PYTHON_FOLDER = "Python_{}".format(PYTHON_VERSION.replace(".", ""))

if ISWINDOWS:
    PYTHON_EXECUTABLE = os.path.join(PYTHON_ENV_DIR, "windows", PYTHON_FOLDER, "python.exe")
    PYTHON_LIB = os.path.join(PYTHON_ENV_DIR, "windows", PYTHON_FOLDER)
elif ISMAC:
    PYTHON_EXECUTABLE = os.path.join(PYTHON_ENV_DIR, "mac", PYTHON_FOLDER, "bin", "python3")
    PYTHON_LIB = os.path.join(PYTHON_ENV_DIR, "mac", PYTHON_FOLDER, "lib")
elif ISLINUX:
    PYTHON_EXECUTABLE = os.path.join(PYTHON_ENV_DIR, "linux", PYTHON_FOLDER, "bin", "python3")
    PYTHON_LIB = os.path.join(PYTHON_ENV_DIR, "linux", PYTHON_FOLDER, "lib")
