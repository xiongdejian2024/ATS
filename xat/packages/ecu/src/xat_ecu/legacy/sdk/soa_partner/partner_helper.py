
import os
import sys
import time
from time import sleep
import pexpect
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.sdk_tools import exec_shell

current_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = __import__("xat_ecu.resources", fromlist=["LEGACY_ROOT"]).LEGACY_ROOT.as_posix()


def check_soa_partner(soa_partner_path, soa_name):
    """检查是否需要升级soa partner"""
    soa_name_path = os.path.join(soa_partner_path, "soa_name.txt")
    logger.info(f"soa_name_path:{soa_name_path}")
    if os.path.exists(soa_name_path):
        with open(soa_name_path, "r") as f:
            got_soa_name = f.read()
        if got_soa_name == soa_name:
            logger.info("soa_name is same, not to deploy soa partner")
            return False
        elif "SOA_" == soa_name:
            logger.info("没有获取到 soa_name, not to deploy soa partner")
            return False
        else:
            return True
    else:
        return True


def deploy_soa_partner(soa_partner_path, soa_name):
    """
    删除旧的soa partner，下载并解压缩云端的soa partner，解压缩完毕后删除下载的zip包
    """
    soa_partner_deploy_path = os.path.join(soa_partner_path, "BootesRelease")
    rm_soa_cmd = f"rm -rf {soa_partner_deploy_path}"
    logger.info(f"开始删除旧的soa partner：{rm_soa_cmd}")
    logger.info(current_path)
    res = exec_shell(rm_soa_cmd)["error"]
    if res == "":
        logger.info("rm_soa_cmd success")
    else:
        logger.error("rm_soa_cmd res is {}, ----- run failed".format(res))
    sleep(2)
    exec_shell("sync")
    sleep(3)

    start_time = time.time()

    if soa_name:
        ARTIFACTORY_URL = "https://repo.jidudev.com/artifactory/SOASDK/SoaAutoTestPackages"
        ARTIFACTORY_USERNAME = "public_soa_bgm_tcam"
        ARTIFACTORY_PASSWORD = __import__("os").environ.get('XAT_CREDENTIAL_ECU__SDK_SOA_PARTNER_PARTNER_HELPER_PY_ARTIFACTORY_PASSWORD', "")
        OUTPUT_FILE = "soa.zip"
        DOWNLOAD_PATH = f"{ARTIFACTORY_URL}/{soa_name}/{OUTPUT_FILE}"
        MAX_RETRIES = 3
        curl_cmd = f"curl -u ${XAT_CREDENTIAL_SCAN_581AFA1EA9F7FA9DEA61} -o './{OUTPUT_FILE}' '{DOWNLOAD_PATH}'"
        scp_soa_partner_cmd = f"cd {soa_partner_path};{curl_cmd}"
        logger.info("scp_soa_partner_cmd: {}".format(scp_soa_partner_cmd))
        while MAX_RETRIES > 0:
            start = time.time()
            res = exec_shell(scp_soa_partner_cmd)["error"]
            end = time.time()
            duration = end - start
            logger.info(f"当前artifactory下载时间：{duration}")
            if duration > 5:
                logger.info("scp_soa_partner_cmd success")
                download_result_flag = True
                break
            else:
                MAX_RETRIES = MAX_RETRIES - 1
                logger.error("scp_soa_partner_cmd res is {}, ----- run failed".format(res))
                exec_shell(f"cd {soa_partner_path};rm -rf soa.zip")
        else:  # Artifactory下载失败
            cmd = f"scp root@172.18.128.5:/root/soazip/{soa_name}/soa.zip {soa_partner_path}"
            logger.info(f"scp 下载命令：{cmd}")
            process = pexpect.spawn(cmd, timeout=300)
            expect_list = [
                'yes/no',
                'password:',
                pexpect.EOF,
                pexpect.TIMEOUT,
            ]
            index = process.expect(expect_list)
            logger.info(f'匹配到: {index} => {expect_list[index]}')
            if index == 0:
                process.sendline("yes")
                expect_list = [
                    'password:',
                    pexpect.EOF,
                    pexpect.TIMEOUT,
                ]
                index = process.expect(expect_list)
                logger.info(f'匹配到: {index} => {expect_list[index]}')
                if index == 0:
                    process.sendline('jidu123')
                    process.interact()
                    download_result_flag = True
                else:
                    download_result_flag = False
                    logger.info('EOF or TIMEOUT')
            elif index == 1:
                process.sendline('jidu123')
                process.interact()
                download_result_flag = True
            else:
                download_result_flag = False
                logger.info('EOF or TIMEOUT')
        logger.info(f"下载结果{download_result_flag}")
        if download_result_flag:  # 下载成功，开始解压缩，并删除下载的zip包
            res = exec_shell(f"cd {soa_partner_path};unzip -o soa.zip >{soa_partner_path}/unzip_soa.log")["error"]
            if res == "":
                logger.info("unzip soa success")
                res = exec_shell(f"rm {soa_partner_path}/soa.zip;rm -rf {soa_partner_path}/idl")["error"]
                if res == "":
                    logger.info("rm soa success")
                else:
                    logger.error("rm soa res is {}, ----- run failed".format(res))
            else:
                logger.error("unzip soa res is {}, ----- run failed".format(res))
    else:
        logger.error("not get soazip, not deploy_soapartner")

    end_time = time.time()
    if (end_time - start_time) > 5:  # 从zip包的下载、解压缩、删除zip包的总时间大于5秒钟
        with open(f"{soa_partner_path}/soa_name.txt", "w") as f:
            f.write(soa_name)  # 保存soa partner的版本至soa_name.txt
        logger.info("write soa_name.txt success")
    else:
        logger.info("deploy_soapartner_cmd is failed really")
