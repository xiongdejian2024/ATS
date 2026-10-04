#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :partner_helper.py
@time         :2/8/24 17:10
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import os
import time
from time import sleep

from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.interface.cd_soc.cd_soc_ssh import CD_SOC_SSH
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.tools.setup_env.auto_generate_soa_partner_function import convert_service_json_to_soa_partner

from framework.automotive.utils.conftest_helper import soa_partner_path, parent_dir
from framework.automotive.utils.data_type import Domain


class PartnerHelper:
    def __init__(self):
        self.soa_partner_path = soa_partner_path
        self.parent_dir = parent_dir

    def get_soa_name_on_sil(self, domain_info: Domain):
        if (
                domain_info.single_bgm or
                domain_info.two_domain or
                domain_info.four_domain or
                domain_info.bgm_tcam_acu or
                domain_info.bgm_cdc_acu or
                domain_info.bgm_tcam_cdc
        ):
            bgmssh = BGM_SSH(connect_type='vlan')
            soa_name = bgmssh.get_soa_jidl_name()
            return soa_name
        elif domain_info.single_tcam:
            tcamssh = TCAM_SSH(connect_type='vlan')
            tcam_version_info = tcamssh.get_soa_jidl_name()
            soa_name = tcam_version_info.get("soa_name")
            return soa_name
        elif domain_info.ccu_cd:
            cd_soc_ssh = CD_SOC_SSH(connect_type='vlan')
            cd_soc_version_info = cd_soc_ssh.get_version()
            soa_name = cd_soc_version_info.get("soa_name")
            return soa_name

    def get_soa_name(self, domain_info: Domain):
        if (
                domain_info.single_bgm or
                domain_info.two_domain or
                domain_info.four_domain or
                domain_info.bgm_tcam_acu or
                domain_info.bgm_cdc_acu or
                domain_info.bgm_tcam_cdc
        ):
            bgmssh = BGM_SSH()
            soa_name = bgmssh.get_soa_jidl_name()
            return soa_name
        elif domain_info.single_tcam:
            tcamssh = TCAM_SSH(connect_type='vlan')
            tcam_version_info = tcamssh.get_soa_jidl_name()
            soa_name = tcam_version_info.get("soa_name")
            return soa_name
        elif domain_info.ccu_cd:
            cd_soc_ssh = CD_SOC_SSH(connect_type='vlan')
            cd_soc_version_info = cd_soc_ssh.get_version()
            soa_name = cd_soc_version_info.get("soa_name")
            return soa_name

    def check_soa_partner(self, soa_name):
        if os.path.exists("/root/soa_name.txt"):
            # 如果与root下的soa_name.txt的版本一致，并且sat目录下没有soa_name.txt，则直接拷贝
            with open("/root/soa_name.txt", "r") as f:
                got_root_soa_name = f.read()
            is_dir_exist = self.directory_exists_and_not_empty(f"{self.soa_partner_path}/BootesRelease")
            if not os.path.exists("../../soa_name.txt") or not is_dir_exist:
                if got_root_soa_name == soa_name:
                    try:
                        self.copy_soazip_and_unzip()
                    except exception_error.DeploySoaPartnerError:
                        return True
                    else:
                        logger.info("root目录下存在目标soazip, 不需要下载")
                        return False
                else:
                    return True
            else:
                with open("../../soa_name.txt", "r") as f:
                    got_soa_name = f.read()
                # 如果版本一致 不需要部署
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

    def copy_soazip_and_unzip(self):
        res = os.system(f'cp -f /root/soa.zip {self.soa_partner_path}')
        if res == 0:
            logger.info("cp soa success")
        else:
            err_msg = f"cp soa res is {res}, ----- run failed"
            raise exception_error.DeploySoaPartnerError(err_msg)
        res = os.system(
            f"cd {self.soa_partner_path};unzip -o soa.zip >/root/unzip_soa.log"
        )
        if res == 0:
            logger.info("unzip soa success")
            res = os.system(f"rm {self.soa_partner_path}/soa.zip")
            if res == 0:
                logger.info("rm soa success")
            else:
                err_msg = f"rm soa res is {res}, ----- run failed"
                logger.error(err_msg)
                raise exception_error.DeploySoaPartnerError(err_msg)
        else:
            err_msg = f"unzip soa res is {res}, 解压的partner文件损坏，尝试重新部署"
            rm_soa_name = f"rm -rf /root/soa_name.txt"
            res = os.system(rm_soa_name)
            if res == 0:
                logger.info("rm_soa_cmd success")
            logger.error(err_msg)
            raise exception_error.DeploySoaPartnerError(err_msg)

        # 将生成/root/soa.zip拷贝到用户的工程目录后，基于工程目录下的out/x86/bin/的服务json文件
        json_file_path = os.path.join(self.soa_partner_path, 'BootesRelease', 'out', 'x86', 'bin')
        try:
            convert_service_json_to_soa_partner(json_file_path, os.path.join(self.soa_partner_path, 'src'))
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/partner_helper.py")
            logger.warning("自动生成 soa partner 函数异常：" + e.__repr__())
        else:
            logger.info("自动生成 soa partner 函数 成功")
        # 压缩完成之后更新soa_name.txt
        res = os.system('cp -f /root/soa_name.txt ../../')
        if res == 0:
            logger.info("cp soa_name.txt success")
        else:
            err_msg = f"cp soa_name.txt res is {res}, ----- run failed"
            logger.error(err_msg)
            raise exception_error.DeploySoaPartnerError(err_msg)

    def deploy_soapartner(self, soa_name):
        # rm soa_partner
        rm_soa_cmd = f"rm -rf {self.soa_partner_path}/idl {self.soa_partner_path}/JIDLCompiler {self.soa_partner_path}/out {self.soa_partner_path}/X86 {self.soa_partner_path}/BootesRelease"
        res = os.system(rm_soa_cmd)
        if res == 0:
            logger.info("rm_soa_cmd success")
        else:
            err_msg = f"rm_soa_cmd res is {res}, ----- run failed"
            logger.error(err_msg)
            raise exception_error.DeploySoaPartnerError(err_msg)
        sleep(2)
        os.system("sync")
        sleep(3)

        start_time = time.time()

        if soa_name:
            scp_soa_partner_cmd = os.path.join(
                self.parent_dir, "tools/setup_env/scp_soa_partner.sh"
            )
            scp_soa_partner_cmd = (
                    f"cd {self.soa_partner_path};" + scp_soa_partner_cmd + " " + soa_name
            )
            logger.info("scp_soa_partner_cmd: {}".format(scp_soa_partner_cmd))
            res = os.system(scp_soa_partner_cmd)
            if res == 0:
                logger.info("scp_soa_partner_cmd success")
            else:
                err_msg = f"scp_soa_partner_cmd res is {res}, ----- run failed"
                logger.error(err_msg)
                raise exception_error.DeploySoaPartnerError(err_msg)

            res = os.system(
                f"cd {self.soa_partner_path};unzip -o soa.zip >/root/unzip_soa.log"
            )
            if res == 0:
                logger.info("unzip soa success")
                res = os.system(f"rm {self.soa_partner_path}/soa.zip")
                if res == 0:
                    logger.info("rm soa success")
                else:
                    err_msg = f"rm soa res is {res}, ----- run failed"
                    logger.error(res)
                    raise exception_error.DeploySoaPartnerError(err_msg)
            else:
                if res == 2304:
                    err_msg = f"unzip soa res is {res}, 该版本jfrog上不存在，请联系测试开发提供{soa_name}版本的partner"
                else:
                    err_msg = f"unzip soa res is {res}, ----- run failed"
                logger.error(err_msg)
                raise exception_error.DeploySoaPartnerError(err_msg)

        else:
            err_msg = f"not get soazip, not deploy_soapartner"
            logger.error(err_msg)
            raise exception_error.DeploySoaPartnerError(err_msg)

        end_time = time.time()
        if (end_time - start_time) > 5:
            with open("/root/soa_name.txt", "w") as f:
                f.write(soa_name)
            logger.info("write soa_name.txt success")
            res = os.system('cp -f /root/soa_name.txt ../../')
            if res == 0:
                logger.info("copy soa success")
            else:
                err_msg = f"copy soa res is {res}, ----- run failed"
                logger.error(err_msg)
                raise exception_error.DeploySoaPartnerError(err_msg)

        else:
            logger.info("deploy_soapartner_cmd is failed really")

    def directory_exists_and_not_empty(self, path):
        if os.path.isdir(path):
            contents = os.listdir(path)
            if contents:
                return True
        # 如果目录不存在或为空，则返回False
        logger.warning(f"{path}目录不存在或为空")
        return False
