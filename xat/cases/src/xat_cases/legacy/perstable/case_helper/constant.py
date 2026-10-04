# encoding=utf-8
import os
import shutil
import sys
import platform
import json


# work path
WORK_PATH = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir))
JOB_PATH = os.path.dirname(WORK_PATH)
REPORT_FOLDER = os.path.join(JOB_PATH, "report")
LOG_PATH = os.path.join(REPORT_FOLDER, "soa_perstab_log")
BGM_LOG_PATH = os.path.join(LOG_PATH, "bgm_log")
TCAM_LOG_PATH = os.path.join(LOG_PATH, "tcam_log")
BGM_COREDUMP_PATH = os.path.join(LOG_PATH, "bgm_coredump")
TCAM_COREDUMP_PATH = os.path.join(LOG_PATH, "tcam_coredump")

if not os.path.exists(REPORT_FOLDER):
    os.mkdir(REPORT_FOLDER)
    os.mkdir(os.path.join(REPORT_FOLDER, "allure_report"))

if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

if not os.path.exists(BGM_LOG_PATH):
    os.mkdir(BGM_LOG_PATH)

if not os.path.exists(TCAM_LOG_PATH):
    os.mkdir(TCAM_LOG_PATH)

if not os.path.exists(BGM_COREDUMP_PATH):
    os.mkdir(BGM_COREDUMP_PATH)

if not os.path.exists(TCAM_COREDUMP_PATH):
    os.mkdir(TCAM_COREDUMP_PATH)

# get args from platform
task_json = os.path.join(JOB_PATH, 'task.json')
with open(task_json, 'r') as f:
    testParameter = json.load(f)
