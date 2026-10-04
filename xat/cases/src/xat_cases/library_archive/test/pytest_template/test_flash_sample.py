# -*- coding: utf-8 -*-
"""
@File        : test_flash_sample.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022/8/26 11:00
@Description : 
@Examples    :
"""

import os
import re
import sys
import argparse
import json

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))
import pytest
import time
from xat_ecu.legacy.testsdk.test_willow_flash_tcam import TestUdsFlashDoipSimTcam
from xat_ecu.legacy.testsdk.test_willow_flash_bgm import TestUdsFlashDoipSimBgm
import json
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.sdk_tools import *

os.system("mkdir ../report")
os.system("touch ../report/report_summary.json")

# path_json = "../../../task.json"
willow_path=get_willow_file_path()
if willow_path:
    path_json=os.path.join(willow_path, "task.json")
else:
    path_json="task.json"

logger.info(f'path_json {path_json}')
if os.path.exists(path_json):
    with open(path_json, "r") as f:
        task_dict = json.load(f)
        file_url = task_dict.get("img_url")
        keyinfo = task_dict.get("keyinfo")
        file_url1 = task_dict.get("img_url1")
        keyinfo1 = task_dict.get("keyinfo1")
        flash_flag = task_dict.get("flash_flag")
        img_url_boot = task_dict.get("img_url_boot")
        keyinfo_boot = task_dict.get("keyinfo_boot")
        mcu_ver = task_dict.get("mcu_ver", '').upper().replace(' ', '')
        blt_ver = task_dict.get("blt_ver", '').upper().replace(' ', '')
        switch_ver = task_dict.get("switch_ver", '').upper().replace(' ', '')
        switch_ver_b = task_dict.get("switch_ver_b", '').upper().replace(' ', '')  # f 样以后
        inputTestScriptCMD = task_dict.get("inputTestScriptCMD")


def get_run_count(inputTestScriptCMD):
    try:
        msg = inputTestScriptCMD.lower().split('--')
        aa = [i.replace(' ', '') for i in msg if i.startswith("count")]
        if aa:
            count = int(aa[0].split('=')[-1])
        else:
            count = 1
    except Exception as e:
        count = 1
    return count


retry_flag = get_run_count(inputTestScriptCMD)
logger.info(f"retry_flag, {retry_flag}")


class TestFlash:
    @pytest.mark.flashtcam
    def test_flashtcam(self):
        global retry_flag
        if retry_flag:
            tcamflash = TestUdsFlashDoipSimTcam()
            tcamflash.tcam_file_url = file_url
            tcamflash.keyinfo = keyinfo
            if (flash_flag == 'False') or (
                    file_url == "https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/v0.5.5/2022091620/6110110055BN.bin"):
                logger.warning("===================== not get tcam version, exit ===================")
            else:
                try:
                    tcamflash.test_tcam_updata(standard=True)
                    retry_flag = 0
                    os.system("rm ./*.bin")
                    os.system("rm ./*.keyinfo")
                    with open("../report/report_summary.json", "w") as f:
                        report_summary = {"start": True}
                        json.dump(report_summary, f)
                except Exception as e:
                    with open("../report/report_summary.json", "w") as f:
                        report_summary = {"start": False}
                        json.dump(report_summary, f)
                    logger.error("TCAM FLASH ERROR IS {}".format(str(e)))
                    retry_flag -= 1
                    assert retry_flag
                finally:
                    time.sleep(300)
        else:
            logger.info("The tcam has been upgraded successfully, and it does not need to be upgraded again")

    @pytest.mark.flashtcamrepeat
    @pytest.mark.repeat(20)
    def test_flashtcamrepeat(self):
        try:
            tcamflash = TestUdsFlashDoipSimTcam()
            # tcamflash.tcam_file_url = "https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/v0.5.5/2022083121/6110110055BI.bin"
            # tcamflash.keyinfo = "${XAT_CREDENTIAL_SCAN_610486766ADD0CB3CDD7}"
            tcamflash.tcam_file_url = file_url
            tcamflash.keyinfo = keyinfo
            tcamflash.test_tcam()
        except Exception as e:
            logger.error("TCAM FLASH ERROR IS {}".format(str(e)))
        finally:
            time.sleep(300)

    @pytest.mark.flashtcam_special
    def test_flashtcam_special(self):
        # For the purpose of improving the success rate of Flash, discard some checks
        global retry_flag
        if retry_flag:
            tcamflash = TestUdsFlashDoipSimTcam()
            tcamflash.tcam_file_url = file_url
            tcamflash.keyinfo = keyinfo
            if (flash_flag == 'False') or (
                    file_url == "https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/v0.5.5/2022091620/6110110055BN.bin"):
                logger.warning("===================== not get bgm version, exit ===================")
            else:
                try:
                    tcamflash.test_tcam_updata(standard=False)
                    retry_flag = 0
                    os.system("rm ./*.bin")
                    os.system("rm ./*.keyinfo")
                    with open("../report/report_summary.json", "w") as f:
                        report_summary = {"start": True}
                        json.dump(report_summary, f)
                except Exception as e:
                    with open("../report/report_summary.json", "w") as f:
                        report_summary = {"start": False}
                        json.dump(report_summary, f)
                    logger.error("TCAM FLASH ERROR IS {}".format(str(e)))
                    retry_flag -= 1
                    assert retry_flag
                finally:
                    time.sleep(300)
        else:
            logger.info("The tcam has been upgraded successfully, and it does not need to be upgraded again")

    @pytest.mark.flashboot
    def test_flashboot(self):
        global retry_flag
        if retry_flag:
            bgmflash = TestUdsFlashDoipSimBgm()
            # bgmflash.bgm_file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/release_build/v0.5.5/2022083020/6160110055BV.bin"
            # bgmflash.keyinfo = "${XAT_CREDENTIAL_SCAN_69EB182FABD93C36E9A0}"
            bgmflash.bgm_file_url = img_url_boot
            bgmflash.keyinfo = keyinfo_boot
            if (flash_flag == 'False') or (
                    img_url_boot == "https://repo.jidudev.com/artifactory/BGMSoftware/release_build/v0.6.0/2022092518/6160110060AO.bin"):
                logger.warning("===================== not get bgm version, exit ===================")
            else:
                try:
                    bgmflash.test_bgm_updata()

                    retry_flag = 0
                    os.system("rm ./*.bin")
                    os.system("rm ./*.keyinfo")
                    with open("../report/report_summary.json", "w") as f:
                        report_summary = {"start": True}
                        json.dump(report_summary, f)


                except Exception as e:

                    with open("../report/report_summary.json", "w") as f:
                        report_summary = {"start": False}
                        json.dump(report_summary, f)
                    logger.error("BGM FLASH ERROR IS {}".format(str(e)))
                    retry_flag -= 1
                    assert retry_flag
                finally:
                    time.sleep(1)
        else:
            logger.info("The bgm has been upgraded successfully, and it does not need to be upgraded again")

    @pytest.mark.flashbgm
    def test_flashbgm(self):
        global retry_flag
        if retry_flag:
            bgmflash = TestUdsFlashDoipSimBgm()
            # bgmflash.bgm_file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/release_build/v0.5.5/2022083020/6160110055BV.bin"
            # bgmflash.keyinfo = "${XAT_CREDENTIAL_SCAN_69EB182FABD93C36E9A0}"
            bgmflash.bgm_file_url = file_url
            bgmflash.keyinfo = keyinfo
            if (flash_flag == 'False') or (
                    file_url == "https://repo.jidudev.com/artifactory/BGMSoftware/release_build/v0.6.0/2022092518/6160110060AO.bin"):
                logger.warning("===================== not get bgm version, exit ===================")
            else:
                err_flag = True
                try:
                    bgmflash.test_bgm_updata()

                    retry_flag = 0
                    os.system("rm ./*.bin")
                    os.system("rm ./*.keyinfo")
                    with open("../report/report_summary.json", "w") as f:
                        report_summary = {"start": True}
                        json.dump(report_summary, f)

                    mcu_version, boot_version = bgmflash.get_bgm_mcu_and_boot_ver()
                    if mcu_ver and mcu_ver != mcu_version:
                        logger.error(f"mcu 的版本号不匹配，本应为{mcu_ver}，实际获取的为{mcu_version}")
                        err_flag = False
                    if blt_ver and blt_ver != boot_version:
                        logger.error(f" boot 的版本号不匹配，本应为{blt_ver}，实际获取的为{boot_version}")
                        err_flag = False
                    switch_version = bgmflash.get_bgm_switch_ver()
                    # switch_ver
                    if (switch_ver or switch_ver_b) and switch_version not in [switch_ver, switch_ver_b]:
                        logger.error(
                            f" switch 的版本号不匹配，本应为{switch_ver, switch_ver_b}，实际获取的为{switch_version}")
                        err_flag = False

                except Exception as e:
                    with open("../report/report_summary.json", "w") as f:
                        report_summary = {"start": False}
                        json.dump(report_summary, f)
                    logger.error("BGM FLASH ERROR IS {}".format(str(e)))
                    retry_flag -= 1
                    assert retry_flag
                finally:
                    assert err_flag
                    time.sleep(1)
        else:
            logger.info("The bgm has been upgraded successfully, and it does not need to be upgraded again")

    @pytest.mark.flashbgm_special
    def test_flashbgm_special(self):
        # For the purpose of improving the success rate of Flash, discard some checks
        global retry_flag
        if retry_flag:
            bgmflash = TestUdsFlashDoipSimBgm()
            bgmflash.bgm_file_url = file_url
            bgmflash.keyinfo = keyinfo
            if (flash_flag == 'False') or (
                    file_url == "https://repo.jidudev.com/artifactory/BGMSoftware/release_build/v0.6.0/2022092518/6160110060AO.bin"):
                logger.warning("===================== not get bgm version, exit ===================")
            else:
                try:
                    bgmflash.test_bgm_updata(standard=False)
                    retry_flag = 0
                    os.system("rm ./*.bin")
                    os.system("rm ./*.keyinfo")
                    with open("../report/report_summary.json", "w") as f:
                        report_summary = {"start": True}
                        json.dump(report_summary, f)
                except Exception as e:
                    with open("../report/report_summary.json", "w") as f:
                        report_summary = {"start": False}
                        json.dump(report_summary, f)
                    logger.error("BGM FLASH ERROR IS {}".format(str(e)))
                    retry_flag -= 1
                    assert retry_flag
                finally:
                    time.sleep(60)
        else:
            logger.info("The bgm has been upgraded successfully, and it does not need to be upgraded again")

    @pytest.mark.flashbgmrepeat
    @pytest.mark.repeat(20)
    def test_flashbgmrepeat(self):
        try:
            bgmflash = TestUdsFlashDoipSimBgm()
            # bgmflash.bgm_file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/release_build/v0.5.5/2022083020/6160110055BV.bin"
            # bgmflash.keyinfo = "${XAT_CREDENTIAL_SCAN_69EB182FABD93C36E9A0}"
            bgmflash.bgm_file_url = file_url
            bgmflash.keyinfo = keyinfo
            bgmflash.test_bgm()
        except Exception as e:
            logger.error("BGM FLASH ERROR IS {}".format(str(e)))
        finally:
            time.sleep(300)

    @pytest.mark.flashbgmperforman
    @pytest.mark.bgm_a2b
    def test_flashbgm_a2b(self):
        try:
            bgmflash = TestUdsFlashDoipSimBgm()
            bgmflash.bgm_file_url = file_url
            bgmflash.keyinfo = keyinfo
            bgmflash.test_bgm()
            time.sleep(60)
            bgmflash.bgm_file_url1 = file_url1
            bgmflash.keyinfo1 = keyinfo1
            bgmflash.test_bgm()
        except Exception as e:
            logger.error("BGM FLASH ERROR IS {}".format(str(e)))
            time.sleep(180)
            assert False
        finally:
            time.sleep(180)

    @pytest.mark.flashtcamperforman
    @pytest.mark.tcam_a2b
    def test_flashtcam_a2b(self):
        try:
            tcamflash = TestUdsFlashDoipSimTcam()
            tcamflash.tcam_file_url = file_url
            tcamflash.keyinfo = keyinfo
            tcamflash.test_tcam()
            time.sleep(300)
            tcamflash.tcam_file_url = file_url1
            tcamflash.keyinfo = keyinfo1
            tcamflash.test_tcam()
        except Exception as e:
            logger.error("TCAM FLASH ERROR IS {}".format(str(e)))
            time.sleep(180)
            assert False
        finally:
            time.sleep(180)
