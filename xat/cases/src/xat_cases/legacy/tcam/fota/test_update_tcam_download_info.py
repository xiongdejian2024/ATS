import os
import sys
import pytest
import allure
from time import sleep
import re
import yaml
import json

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.tcam.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *
from framework.automotive.utils.artifactory_helper import ArtifactoryHelper


@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        # super().before_class(self, ecu)
        self.taskid = ecu["task_id"]
        self.soa.update([("FotaMasterService", "client")])
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
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
        self.mix.update_version_debug(self.taskid, [DOMAIN.TCAM])
        self.ssh.update_ua_skip(DOMAIN.TCAM, allow_same_version_flash=False)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)

    def test_fota_1(self):
        soft_id = self.tsp.get_softid_from_taskid(self.taskid)
        self.vsp_bgm_version = self.tsp.get_domain_version_from_softid(soft_id, DOMAIN.BGM)
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
            raise
        else:
            tcam_download_info = self.download_info.get(f"TCAM_{self.vsp_tcam_version}")
            if tcam_download_info and isinstance(tcam_download_info, dict):
                logger.info(f'{tcam_download_info}版本TCAM下载信息已上传，更新本地配置文件')
                self.data['TCAM_Download_Req'] = tcam_download_info
            else:
                logger.info(f'TCAM下载信息未上传，获取TCAM下载信息并上传')
                self.mix.update_version_debug(self.taskid, [DOMAIN.TCAM])
                self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
                self.mix.back_fota_to(FOTAMasteSts.DOWNLOADING, taskid=self.taskid)
                self.TCAM_Download_Req = self.get_tcam_download_info()
                self.download_info[f"TCAM_{self.vsp_tcam_version}"] = self.TCAM_Download_Req
                self.data['TCAM_Download_Req'] = self.TCAM_Download_Req
                self.write_to_artifactory()
        finally:
            # 更新本地配置文件
            with open('config/UA_conf.yaml', 'w') as outfile:
                yaml.safe_dump(self.data, outfile)

    def get_tcam_download_info(self):

        # 正则匹配TCAM下载信息
        jet_log_tcam = self.ssh.type_commands(DeviceName.TCAM,
                                        '/oemapp/bin/zstdcat /mnt/sdcard/log/jetlog_messages | grep " UAS_SI:"')
        logger.info(jet_log_tcam)
        ret_tcam = re.findall(
        r'pn:(.*?)\n.*?version:(.*?)\n.*?size:(.*?)\n.*?url:(.*?)\n.*?filename:(.*?)\n.*?signature:(.*?)\n.*?keyId:(.*?)\n.*?encKey:(.*?)\n.*?mode: (\d+)\n',
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


if __name__ == "__main__":
    pass
