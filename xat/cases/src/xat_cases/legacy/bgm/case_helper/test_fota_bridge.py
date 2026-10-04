# -*- coding: utf-8 -*-
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


pre_executed_flag_bridge = False
class TestABCBase(CommonABCTestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # willow_soft_id = ecu.get("soft_id")
        # if willow_soft_id:
        #     self.softid = int(willow_soft_id)
        # else:
        #     self.softid =  self.tc_config.get("soft_id")
        # self.bridge_version = self.tsp.get_bgm_version_from_soft_detail(soft_id=self.softid)
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
            global pre_executed_flag_bridge
            if not pre_executed_flag_bridge:
                self.pre_get_type50_info(self)
                self.get_type50_info(self)
                self.mix.fota_back_to_idle()
                self.soa.ua_back_to_idle(DOMAIN.BGM)
                self.tsp.back_vsp_to_Idle()
                self.soa.soa_partner.stop_single_partner("FotaMasterService_client")
                self.soa.soa_partner.stop_single_partner("UpdateAgentService_client_BGM_UA_Service")
                pre_executed_flag_bridge = True
        else:
            self.taskid =  self.tc_config.get("task_id")
            if not pre_executed_flag_bridge:
                self.soa.update([("FotaMasterService","client"),
                                 ("UpdateAgentService","client","BGM_UA_Service")])
                self.mix.fota_back_to_idle()
                self.soa.ua_back_to_idle(DOMAIN.BGM)
                self.tsp.back_vsp_to_Idle()
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
        self.io.bgm_diag_line_up()

    def pre_get_type50_info(self):
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
        self.mix.update_version_debug(self.taskid, [DOMAIN.BGM])
        with open('config/UA_conf.yaml', 'r') as f:
            self.data = yaml.safe_load(f)

    @retry_on_failure(max_retry_count=3)
    def get_type50_info(self):
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        jet_log = self.ssh.type_commands(DeviceName.BGM,
                                         "/app/bin/zstdcat /log/jetlog_messages |grep 'parseJsonData:task info from tsp' | tail -n 1")
        match = re.search(r'parseJsonData:task info from tsp: ({.*}), size:', jet_log)
        if match:
            type50 = json.loads(match.group(1))
            self.data['Task_Info_Type50'] = type50
            with open('config/UA_conf.yaml', 'w') as file:
                yaml.dump(self.data, file, default_flow_style=False)
        else:
            assert False, "can't find type50 in base before class"