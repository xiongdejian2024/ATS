# -*- coding: utf-8 -*-
"""
@File        : test_fota_base.py
@Author      : dejian.xiong@jiduauto.com
@Time        : 2023/11/3 14:30
@Description :
@Examples    :
"""

import os
import sys
import yaml
import re
import json


project_root = os.path.join(os.getcwd(), 'sat')
sys.path.append(project_root)

from xat_cases.legacy.common_abc_test_base import CommonABCTestBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common.common import retry_on_failure
from framework.automotive.utils.artifactory_helper import ArtifactoryHelper


pre_executed_flag = False
class TestABCBase(CommonABCTestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.sd_tester.stop_tester_present()
        self.vin = self.tc_config.get("vin")
        auto_flag, taskid = self.mix.whether_auto_creat_task(ecu, vin=self.vin)
        if auto_flag:
            ecu["task_id"] = str(taskid)
            logger.info(f"成功传递taskid:{ecu['task_id']}")
        with open('config/UA_conf.yaml', 'r') as f:
            conf = yaml.safe_load(f)
        self.TCAM_Download_Req = conf['TCAM_Download_Req']
        global pre_executed_flag
        if not pre_executed_flag:
            willow_task_id = ecu.get("task_id")
            fota_tcam_version = ecu.get("fota_tcam_version")
            if willow_task_id:
                    self.taskid = int(willow_task_id.strip())
                    self.pre_get_ua_download_info(self)
                    self.fota_pre_steps_willow(self)
                    self.mix.fota_back_to_idle()
                    self.soa.ua_back_to_idle(DOMAIN.TCAM)
                    self.tsp.back_vsp_to_Idle()
                    self.soa.soa_partner.stop_single_partner("FotaMasterService_client")
                    self.soa.soa_partner.stop_single_partner("UpdateAgentService_client_TCAM_UA_Service")
            elif fota_tcam_version:
                if len(fota_tcam_version.strip()) == 13:
                    logger.info(f"current argument for fota_tcam_version: {fota_tcam_version}")
                    ArtifactoryHelper.download_UA_info()
                    with open('UA_download_info.json', 'r') as f:
                        self.download_info = json.load(f)
                    logger.info(f"当前云端UA_download_info为：{self.download_info}")
                    self.TCAM_Download_Req = self.download_info.get(f"TCAM_{fota_tcam_version}")
                    if self.TCAM_Download_Req and isinstance(self.TCAM_Download_Req, dict):
                        conf['TCAM_Download_Req'] = self.TCAM_Download_Req
                        with open('config/UA_conf.yaml', 'w') as outfile:
                            yaml.safe_dump(conf, outfile)
                    else:
                        raise ValueError(f"当前云端不存在{fota_tcam_version}版本TCAM_download_info")
                else:
                    raise ValueError("invalid argument for fota_tcam_version")
            pre_executed_flag = True

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.stop_tester_present()

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.sd_tester.reset_tcam()
        logger.info("reset env for ua")

    @retry_on_failure(max_retry_count=3)
    def fota_pre_steps_willow(self):
        """
        TCAM用例前置步骤
        """
        soft_id = self.tsp.get_softid_from_taskid(self.taskid)
        self.vsp_tcam_version = self.tsp.get_domain_version_from_softid(soft_id, DOMAIN.TCAM)
        ArtifactoryHelper.download_UA_info()
        with open('config/UA_conf.yaml', 'r') as f:
            self.data = yaml.safe_load(f)
        try:
            # 解析JSON数据
            with open('UA_download_info.json', 'r') as f:
                self.download_info = json.load(f)
            logger.info(f"当前云端UA_download_info为：{self.download_info}")
        except:
            logger.info(f'TCAM下载信息解析失败，重新获取')
            self.download_info = dict()
            self.get_bgm_tcam_download_info(self)
            self.data['TCAM_Download_Req'] = self.TCAM_Download_Req
        else:
            tcam_download_info = self.download_info.get(f"TCAM_{self.vsp_tcam_version}")
            self.TCAM_Download_Req = tcam_download_info
            if tcam_download_info and isinstance(tcam_download_info, dict):
                logger.info(f'TCAM下载信息已上传，更新本地配置文件')
                self.download_info = None
                self.data['TCAM_Download_Req'] = tcam_download_info
            else:
                logger.info(f'TCAM下载信息未上传，获取TCAM下载信息')
                self.mix.update_version_debug(self.taskid, [DOMAIN.TCAM])
                self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
                self.mix.back_fota_to(FOTAMasteSts.DOWNLOADING, taskid=self.taskid)
                time.sleep(30) # 兼容UA_download_info日志出现较慢的情况
                self.TCAM_Download_Req = self.get_tcam_download_info(self)
                self.download_info[f"TCAM_{self.vsp_tcam_version}"] = self.TCAM_Download_Req
                self.data['TCAM_Download_Req'] = self.TCAM_Download_Req
        finally:
            assert self.TCAM_Download_Req['downloadReq']['fileInformations'][0]['version'] == self.vsp_tcam_version, f"TCAM_Download_Req与taskid：{self.taskid}版本不匹配"
            self.write_to_artifactory(self)

        # 更新本地配置文件
        with open('config/UA_conf.yaml', 'w') as outfile:
            yaml.safe_dump(self.data, outfile)

        self.mix.fota_back_to_idle()

    def pre_get_ua_download_info(self):
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","TCAM_UA_Service")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ], allow_sleep=False)
        self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False)

    def get_tcam_download_info(self):

        # 正则匹配TCAM下载信息
        jet_log_tcam = self.ssh.type_commands(DeviceName.TCAM,
                                        '/oemapp/bin/zstdcat /mnt/sdcard/log/jetlog_messages | grep " UAS_SI:"')
        logger.info(jet_log_tcam)
        ret_tcam = re.findall(
        r'pn:(.*?)\n.*?version:(.*?)\n.*?size:(.*?)\n.*?url:(.*?)\n.*?filename:(.*?)\n.*?signature:(.*?)\n.*?keyId:(.*?)\n.*?encKey:(.*?)\n.*?mode: (\d+)',
        jet_log_tcam, re.S)[-1]
        logger.info(ret_tcam)

        # 更新TCAM_Download_Req的json数据
        TCAM_Download_Req = self.data['TCAM_Download_Req']
        TCAM_Download_Req['downloadReq']['fileInformations'][0]['pn'] = ret_tcam[0].strip()
        TCAM_Download_Req['downloadReq']['fileInformations'][0]['version'] = ret_tcam[1].strip()
        TCAM_Download_Req['downloadReq']['fileInformations'][0]['size'] = int(ret_tcam[2].strip())
        TCAM_Download_Req['downloadReq']['fileInformations'][0]['url'] = ret_tcam[3].strip()
        TCAM_Download_Req['downloadReq']['fileInformations'][0]['fileName'] = ret_tcam[4].strip()
        TCAM_Download_Req['downloadReq']['fileInformations'][0]['signature'] = ret_tcam[5].strip()
        TCAM_Download_Req['downloadReq']['fileInformations'][0]['keyId'] = ret_tcam[6].strip()
        TCAM_Download_Req['downloadReq']['fileInformations'][0]['encKey'] = ret_tcam[7].strip()
        TCAM_Download_Req['downloadReq']['keyInformation']['keyId'] = ret_tcam[6].strip()
        TCAM_Download_Req['downloadReq']['keyInformation']['encKey'] = ret_tcam[7].strip()
        TCAM_Download_Req['downloadReq']['mode'] = int(ret_tcam[8].strip())
        self.data['TCAM_Download_Req'] = TCAM_Download_Req
        logger.info(json.dumps(TCAM_Download_Req, indent=4))
        return TCAM_Download_Req

    def write_to_artifactory(self):
        if self.download_info and isinstance(self.download_info, dict):
            download_info_dict = {k: v for k, v in sorted(self.download_info.items(), key=lambda item: item[0])}
            download_info = json.dumps(download_info_dict)
            with open('UA_download_info.json', 'w') as f:
                f.write(download_info)
            ArtifactoryHelper.upload_UA_info()

    def get_bgm_tcam_download_info(self):
        self.mix.update_version_debug(self.taskid, [DOMAIN.TCAM])
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        self.mix.back_fota_to(FOTAMasteSts.DOWNLOADING, taskid=self.taskid)
        time.sleep(30) # 兼容UA_download_info日志出现较慢的情况
        self.TCAM_Download_Req = self.get_tcam_download_info(self)
        self.download_info[f"TCAM_{self.vsp_tcam_version}"] = self.TCAM_Download_Req