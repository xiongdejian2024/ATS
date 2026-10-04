# -*- coding: utf-8 -*-
"""
@File        : test_abc_base.py
@Author      : dejian.xiong@jiduauto.com
@Time        : 2023/11/3 14:30
@Description :
@Examples    :
"""

import os
import sys
import yaml
import re
import time
import json
import shutil

project_root = os.path.join(os.getcwd(), 'sat')
sys.path.append(project_root)

from xat_cases.legacy.common_abc_test_base import CommonABCTestBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common.common import retry_on_failure
from framework.automotive.utils.artifactory_helper import ArtifactoryHelper
from xat_ecu.legacy.interface.feishu import feishu_api
from xat_ecu.legacy.driver.ssh_interface import SshClient, ScpClient


BASE_ENVIRONMENT_PATH = "/root/deploy_fota_environment"

pre_executed_flag = False
class TestABCBase(CommonABCTestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with open('config/UA_conf.yaml', 'r') as f:
            conf = yaml.safe_load(f)
            self.BGM_Download_Req = conf['BGM_Download_Req']
            self.Task_Info_Type50 = conf['Task_Info_Type50']
            self.Task_Info_Type50_NKR = conf['Task_Info_Type50_NKR']
            self.Task_Info_Type50_CDC = conf['Task_Info_Type50_CDC']
        with open('config/FodConfig.yaml', 'r') as fn:
            fod_config = yaml.safe_load(fn)
            self.fod_e2e_config = fod_config["fod_e2e_config"]
            self.fod_bench_config = fod_config["fod_bench_config"]
        self.sd_tester.stop_tester_present()
        willow_task_id = ecu.get("task_id")
        if willow_task_id:
            self.taskid = int(willow_task_id)
            global pre_executed_flag
            if not pre_executed_flag:
                self.tsp.back_vsp_to_Idle()
                self.set_condition_for_carmode_usagemode(self)
                self.deploy_factory_packages(self)
                self.pre_get_ua_download_info(self)
                self.fota_pre_steps_willow(self)
                self.mix.fota_back_to_idle()
                self.soa.ua_back_to_idle(DOMAIN.BGM)
                self.soa.soa_partner.stop_single_partner("FotaMasterService_client")
                self.soa.soa_partner.stop_single_partner("UpdateAgentService_client_BGM_UA_Service")
                pre_executed_flag = True
        else:
            self.taskid =  self.tc_config.get("task_id")
            if not pre_executed_flag:
                self.tsp.back_vsp_to_Idle()
                self.soa.update([("FotaMasterService","client"),
                                 ("UpdateAgentService","client","BGM_UA_Service")])
                self.mix.fota_back_to_idle()
                self.soa.ua_back_to_idle(DOMAIN.BGM)
                self.soa.soa_partner.stop_single_partner("FotaMasterService_client")
                self.soa.soa_partner.stop_single_partner("UpdateAgentService_client_BGM_UA_Service")

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_up()
        self.sd_tester.stop_tester_present()
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.mix.fota_back_to_idle()
        self.soa.ua_back_to_idle(DOMAIN.BGM)
        self.tsp.back_vsp_to_Idle()
        self.io.bgm_diag_line_up()

    @retry_on_failure(max_retry_count=3)
    def fota_pre_steps_willow(self):
        """
        执行FOTA前准备步骤（Willow平台）
        
        """
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
            logger.info(f'BGM下载信息解析失败，重新获取')
            self.download_info = dict()
            self.get_bgm_tcam_download_info(self)
            self.data['TCAM_Download_Req'] = self.TCAM_Download_Req
            self.data['BGM_Download_Req'] = self.BGM_Download_Req
        else:
            bgm_download_info = self.download_info.get(f"BGM_{self.vsp_bgm_version}")
            tcam_download_info = self.download_info.get(f"TCAM_{self.vsp_tcam_version}")
            self.TCAM_Download_Req = tcam_download_info
            self.BGM_Download_Req = bgm_download_info
            if isinstance(bgm_download_info, dict) and isinstance(tcam_download_info, dict):
                logger.info(f'BGM和TCAM下载信息已上传，更新本地配置文件')
                self.download_info = None
                self.data['TCAM_Download_Req'] = tcam_download_info
                self.data['BGM_Download_Req'] = bgm_download_info
            elif isinstance(bgm_download_info, dict):
                logger.info(f'TCAM下载信息未上传，获取TCAM下载信息')
                self.mix.update_version_debug(self.taskid, [DOMAIN.TCAM])
                self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
                self.mix.back_fota_to(FOTAMasteSts.DOWNLOADING, taskid=self.taskid)
                self.TCAM_Download_Req = self.get_tcam_download_info(self)
                self.download_info[f"TCAM_{self.vsp_tcam_version}"] = self.TCAM_Download_Req
                self.data['BGM_Download_Req'] = bgm_download_info
                self.data['TCAM_Download_Req'] = self.TCAM_Download_Req
            elif isinstance(tcam_download_info, dict):
                logger.info(f'BGM下载信息未上传，获取BGM下载信息')
                self.mix.update_version_debug(self.taskid, [DOMAIN.BGM])
                self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
                self.mix.back_fota_to(FOTAMasteSts.DOWNLOADING, taskid=self.taskid)
                self.BGM_Download_Req = self.get_bgm_download_info(self)
                self.download_info[f"BGM_{self.vsp_bgm_version}"] = self.BGM_Download_Req
                self.data['TCAM_Download_Req'] = tcam_download_info
                self.data['BGM_Download_Req'] = self.BGM_Download_Req
            else:
                logger.info(f'BGM和TCAM下载信息未上传，获取BGM和TCAM下载信息')
                self.get_bgm_tcam_download_info(self)
                self.data['TCAM_Download_Req'] = self.TCAM_Download_Req
                self.data['BGM_Download_Req'] = self.BGM_Download_Req
                
        finally:
            assert self.BGM_Download_Req['downloadReq']['fileInformations'][1]['version'] == self.vsp_bgm_version, f"BGM_Download_Req与taskid：{self.taskid}版本不匹配"
            assert self.TCAM_Download_Req['downloadReq']['fileInformations'][0]['version'] == self.vsp_tcam_version, f"TCAM_Download_Req与taskid：{self.taskid}版本不匹配"
            self.write_to_artifactory(self)

        # 更新本地配置文件
        with open('config/UA_conf.yaml', 'w') as outfile:
            yaml.safe_dump(self.data, outfile)

        real_bgm_version = self.sd_tester.get_bgm_app_soft_version()
        task_bgm_version = self.BGM_Download_Req['downloadReq']['fileInformations'][1]['version']
        real_tcam_version = self.sd_tester.get_tcam_soft_version()
        logger.info(f"taskid:{self.taskid} bgm version:{task_bgm_version}, real bgm version:{real_bgm_version}")
        if not real_bgm_version == task_bgm_version:
            logger.info("current BGM version:{}, need to update".format(real_bgm_version))
            self.mix.fota_back_to_idle()
            self.mix.update_version_debug(self.taskid, [DOMAIN.BGM, DOMAIN.TCAM])
            self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
            single_record  = {
                                'BGM-Base版本': real_bgm_version,
                                'BGM-Target版本': self.vsp_bgm_version,
                                'TCAM-Base版本': real_tcam_version,
                                'TCAM-Target版本': self.vsp_tcam_version,
                                'VIN': self.tc_config.get('vin'),
                                'task id': self.taskid,
                                '成功次数': 1,
                                '总压测次数': 1,
                                '失败次数': 0,
                                '日期': round(time.time() * 1000),
                            }
            feishu_api.insert_record_to_feishu_table(data=single_record, table_name="常规OTA", document_id='TMhIwUiHtiseKMkJe1KcY5BNnxd')
        else:
            logger.info("current BGM version alredy is:{}, cancle fota".format(real_bgm_version))
        self.mix.fota_back_to_idle()

    def pre_get_ua_download_info(self):
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service")])
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

    def get_bgm_download_info(self):
        
        # 正则匹配BGM下载信息
        jet_log_bgm = self.ssh.type_commands(DeviceName.BGM,
                                        "/app/bin/zstdcat /log/jetlog_messages |grep ' UAS' | tail -n 200")
        logger.info(jet_log_bgm)
        ret_bgm = re.findall(
            r'pn:(.*?)\n.*?version:(.*?)\n.*?size:(.*?)\n.*?url:(.*?)\n.*?filename:(.*?)\n.*?signature:(.*?)\n.*?keyId:(.*?)\n.*?encKey:(.*?)\n',
            jet_log_bgm, re.S)
        logger.info(ret_bgm)
        # mode = re.findall(r'mode: (\d+)', jet_log_bgm, re.S)[-1]
        mode = "0"
        # logger.info(mode)
        
        # 更新BGM_Download_Req的json数据
        BGM_Download_Req = self.data['BGM_Download_Req']
        BGM_Download_Req['downloadReq']['fileInformations'][0]['pn'] = ret_bgm[-2][0].strip()
        BGM_Download_Req['downloadReq']['fileInformations'][0]['version'] = ret_bgm[-2][1].strip()
        BGM_Download_Req['downloadReq']['fileInformations'][0]['size'] = int(ret_bgm[-2][2].strip())
        BGM_Download_Req['downloadReq']['fileInformations'][0]['url'] = ret_bgm[-2][3].strip()
        BGM_Download_Req['downloadReq']['fileInformations'][0]['fileName'] = ret_bgm[-2][4].strip()
        BGM_Download_Req['downloadReq']['fileInformations'][0]['signature'] = ret_bgm[-2][5].strip()
        BGM_Download_Req['downloadReq']['fileInformations'][0]['keyId'] = ret_bgm[-2][6].strip()
        BGM_Download_Req['downloadReq']['fileInformations'][0]['encKey'] = ret_bgm[-2][7].strip()
        BGM_Download_Req['downloadReq']['fileInformations'][1]['pn'] = ret_bgm[-1][0].strip()
        BGM_Download_Req['downloadReq']['fileInformations'][1]['version'] = ret_bgm[-1][1].strip()
        BGM_Download_Req['downloadReq']['fileInformations'][1]['size'] = int(ret_bgm[-1][2].strip())
        BGM_Download_Req['downloadReq']['fileInformations'][1]['url'] = ret_bgm[-1][3].strip()
        BGM_Download_Req['downloadReq']['fileInformations'][1]['fileName'] = ret_bgm[-1][4].strip()
        BGM_Download_Req['downloadReq']['fileInformations'][1]['signature'] = ret_bgm[-1][5].strip()
        BGM_Download_Req['downloadReq']['fileInformations'][1]['keyId'] = ret_bgm[-1][6].strip()
        BGM_Download_Req['downloadReq']['fileInformations'][1]['encKey'] = ret_bgm[-1][7].strip()
        BGM_Download_Req['downloadReq']['keyInformation']['keyId'] = ret_bgm[-2][6].strip()
        BGM_Download_Req['downloadReq']['keyInformation']['encKey'] = ret_bgm[-2][7].strip()
        BGM_Download_Req['downloadReq']['mode'] = int(mode.strip())
        self.data['BGM_Download_Req'] = BGM_Download_Req
        logger.info(json.dumps(BGM_Download_Req, indent=4))
        return BGM_Download_Req

    def get_tcam_download_info(self):
        time.sleep(30) # 兼容UA_download_info日志出现较慢的情况

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
        self.mix.update_version_debug(self.taskid, [DOMAIN.BGM, DOMAIN.TCAM])
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        self.mix.back_fota_to(FOTAMasteSts.DOWNLOADING, taskid=self.taskid)
        self.BGM_Download_Req = self.get_bgm_download_info(self)
        self.download_info[f"BGM_{self.vsp_bgm_version}"] = self.BGM_Download_Req
        self.write_to_artifactory(self)
        self.TCAM_Download_Req = self.get_tcam_download_info(self)
        self.download_info[f"TCAM_{self.vsp_tcam_version}"] = self.TCAM_Download_Req
        
    def deploy_factory_packages(self):
        ssh_client = SshClient(host="172.18.128.154", port=22, username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____BGM_CASE_HELPER_TEST_FOTA_BASE_PY_PASSWORD', ""))
        result = ssh_client.execute(f'find {BASE_ENVIRONMENT_PATH} -type f -name "6*.zip"')
        ssh_client.close()
        logger.info(result)
        remote_factory_pkg_version = result[1].split(".zip")[1].split("/")[-1]
        logger.info("-------------------------------------")
        logger.info(remote_factory_pkg_version)
        if os.path.exists(BASE_ENVIRONMENT_PATH):
            local_zip_file_list = [f for f in os.listdir(BASE_ENVIRONMENT_PATH) if f.endswith('.zip')]
            local_factory_pkg_version = False
            if len(local_zip_file_list) == 1:
                local_factory_pkg_version = local_zip_file_list[0].split(".zip")[0]
                logger.info(local_factory_pkg_version)
            if local_factory_pkg_version == remote_factory_pkg_version:
                return
            shutil.rmtree(BASE_ENVIRONMENT_PATH)
        os.makedirs(BASE_ENVIRONMENT_PATH)
        scp_client = ScpClient(host="172.18.128.154", port=22, username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____BGM_CASE_HELPER_TEST_FOTA_BASE_PY_PASSWORD', ""))
        factory_zip_path = os.path.join(BASE_ENVIRONMENT_PATH, f"{remote_factory_pkg_version}.zip")
        scp_client.get(local_path=factory_zip_path, remote_path=factory_zip_path)
        scp_client.close()
        self.ssh.scp_local_file_to_bgm(factory_zip_path)
        self.ssh.type_commands(DeviceName.BGM, "rm -rf /data/factory_bak/*")
        self.ssh.type_commands(DeviceName.BGM, "rm -rf /data/DDM_bak/*")
        self.ssh.type_commands(DeviceName.BGM, "rm -rf /data/factory_package/*")
        self.ssh.type_commands(DeviceName.BGM, "rm -rf /data/sl/*")
        self.ssh.type_commands(DeviceName.BGM, "rm -rf /data/debug_bak.sh")
        self.ssh.type_commands(DeviceName.BGM, f"unzip /tmp/{remote_factory_pkg_version}.zip -d /data/")
            

    def set_condition_for_carmode_usagemode(self):
        self.soa.update([("CentralLockService","client")])
        time.sleep(3)
        cen_lock_sts = self.bus_comm.get_central_lock_sts()
        if cen_lock_sts == 3:
            self.bus_comm.send_nfc_cmd()
            self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)
        self.soa.soa_partner.stop_single_partner("CentralLockService_client")