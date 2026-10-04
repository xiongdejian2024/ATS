import copy
import os
import sys
import pytest
import allure
import time
import yaml
import datetime
import traceback
import json

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.feishu.feishu_api import feishu_api

# 台架列表
bench_list = ["JDS0ATESTBENCH050"]
# 定义时间范围的开始和结束
start_time = datetime.time(22, 40)
end_time = datetime.time(3, 20)
vehicle_config = {}
@allure.feature("基础架构")
@allure.story("FOTA")
@pytest.mark.stress_test
class TestFota(TestABCBase):
    def before_class(self, ecu):
        # super().before_class(self, ecu)
        with open('config/taskid_vin.json', 'r') as file:
            self.vehicle_task_info = json.load(file)
        self.vehicle_task_info = {int(k): v for k, v in self.vehicle_task_info.items()}
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=100, low_volt_soc=90)
        self.mix.set_enter_boot_condition(UsageMode.CONVENIENCE, low_volt_power=14, vehspd=0)
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        # super().after_class(self, ecu)
        pass

    @allure.title("E2E_Normal_Vehicle_Base")  
    @pytest.mark.parametrize("case_id",[
                            pytest.param(1983175, id="1983175", marks=[pytest.mark.sanity]),
                            pytest.param(1993380, id="1993380", marks=[pytest.mark.sanity]),
                            pytest.param(1993381, id="1993381", marks=[pytest.mark.sanity]),
                            pytest.param(1993382, id="1993382", marks=[pytest.mark.sanity]),
                        ])  
    def test_fota_caseid_(self, case_id):
        self.io.bgm_diag_line_down()
        self.feishu = feishu_api()
        vehicle_test_result = dict()
        vin_record_info = dict()
        valid_result_flag = dict()
        version_info = dict()
        trigger_update_flag = dict()
        appointment_record = dict()
        update_failed_record = dict()
        last_check_time = datetime.datetime.now()
        with open("config/SOA_QA_Vehicle.yaml", "r") as file:
            SOA_QA_Vehicle = yaml.safe_load(file)
        for task_id_ in self.vehicle_task_info:
            task_id_ = int(task_id_)
            soft_id = self.tsp.get_softid_from_taskid(task_id_)
            bgm_version = self.tsp.get_domain_version_from_softid(soft_id=soft_id,domain_name=DOMAIN.BGM)
            tcam_version = self.tsp.get_domain_version_from_softid(soft_id=soft_id,domain_name=DOMAIN.TCAM)
            version_info[task_id_] = [bgm_version, tcam_version]
        while True:
            try:
                now = datetime.datetime.now().time()
                # 判断当前时间是否在时间范围内
                is_between_times = now >= start_time or now <= end_time
                with open('config/taskid_vin.json', 'r') as file:
                    current_vehicle_task_info = json.load(file)
                current_vehicle_task_info = {int(k): v for k, v in current_vehicle_task_info.items()}
                if current_vehicle_task_info != self.vehicle_task_info:
                    logger.info(f"压测任务改变，当前任务信息：{current_vehicle_task_info}")
                    self.vehicle_task_info = current_vehicle_task_info
                    for task_id_ in self.vehicle_task_info:
                        task_id_ = int(task_id_)
                        soft_id = self.tsp.get_softid_from_taskid(task_id_)
                        bgm_version = self.tsp.get_domain_version_from_softid(soft_id=soft_id,domain_name=DOMAIN.BGM)
                        tcam_version = self.tsp.get_domain_version_from_softid(soft_id=soft_id,domain_name=DOMAIN.TCAM)
                        version_info[task_id_] = [bgm_version, tcam_version]
                    vin_record_info.clear()
                for task_id, vin_lst in self.vehicle_task_info.items():
                    task_id = int(task_id)
                    for vin in vin_lst:
                        time.sleep(5)
                        if not vin in vin_record_info:
                            single_record  = {
                                'BGM-Base版本': version_info[task_id][0],
                                'BGM-Target版本': version_info[task_id][0],
                                'TCAM-Base版本': version_info[task_id][1],
                                'TCAM-Target版本': version_info[task_id][1],
                                'VIN': vin,
                                'task id': task_id,
                                '升级方式': ['平刷'],
                                '失败次数': 0,
                                '总压测次数': 0,
                                '成功次数': 0,
                                '日期': 1721232000000,
                                '环境': ['实车'],
                                '问题详情': "NA"
                            }
                            if vin not in bench_list:
                                appointment_record[vin] = copy.copy(single_record)
                            update_failed_record[vin] = copy.copy(single_record)
                            self.update_feishu_access_token()
                            single_record["日期"] = round(time.time() * 1000)
                            _, record_id = self.feishu.add_record_in_table(table_id="tblD6s278dLS5uU5", data=single_record)
                            logger.info(record_id)
                            if record_id:
                                vin_record_info[vin] = record_id
                                valid_result_flag[vin] = True
                                trigger_update_flag[vin] = None
                                copy_single_record = copy.copy(single_record)
                                del copy_single_record["问题详情"]
                                del copy_single_record["环境"]
                                vehicle_test_result[record_id] = copy_single_record
                        vsp_status, sub_tasks = self.tsp.get_vsp_fota_status(task_id=task_id, vin=vin) 
                        task_info = f"=========== VIN—{vin}, TaskId—{task_id}, "
                        if vsp_status == 15:
                            logger.info(f"{task_info}推送中 ===========")
                            if "有外部更高优先级的功能介入，停止收集版本" in sub_tasks["data"]["list"][0]['remark']:
                                logger.info(f"VIN—{vin}, TaskId—{task_id}, 版本收集被打断，取消当前FOTA任务")
                                logger.info(sub_tasks)
                                self.tsp.trigger_vsp_fota(VSP.Cancel, task_id, vin)
                                time.sleep(5)
                        elif vsp_status == 4:
                            logger.info(f"{task_info}下载中 ===========")
                            trigger_update_flag[vin] = True
                        elif vsp_status == 5:
                            logger.info(f"{task_info}下载成功 ===========")
                            if is_between_times:
                                continue
                            if trigger_update_flag[vin] or trigger_update_flag[vin] is None:
                                single_Vehicle = SOA_QA_Vehicle.get(vin)
                                tel = single_Vehicle.get("tel")
                                vid = single_Vehicle.get("vid")
                                if tel and vid and vin not in bench_list:
                                    self.tsp.trigger_update_by_real_app(vid =vid, tel=tel)
                                    time.sleep(180)
                                    trigger_update_flag[vin] = False
                            else:
                                self.vehicle_task_info[task_id].remove(vin)
                                with open('config/taskid_vin.json', 'w') as file:
                                    json.dump(self.vehicle_task_info, file)
                                logger.info(f"{vin}触发app升级失败，停止当前车辆压测")
                        elif vsp_status == 8:
                            logger.info(f"{task_info}升级中 ===========")
                            valid_result_flag[vin] = True
                        elif vsp_status == 18:
                            logger.info(f"{task_info}FOTA成功 ===========")
                            single_Vehicle = SOA_QA_Vehicle.get(vin)
                            vid = single_Vehicle.get("vid")
                            upgrade_info = self.tsp.get_lastet_status(task_id=task_id, vin=vin, vid=vid)
                            timeline_node_list = upgrade_info["data"]["timelineNodeList"]
                            for timeline_node in timeline_node_list:
                                if timeline_node["message"] == "任务自动救援":
                                    logger.info(f"VIN—{vin}, TaskId—{task_id}, 检查到任务自动救援")
                                    rescue_fail_time = datetime.datetime.strptime(timeline_node["time"], "%Y-%m-%d %H:%M:%S")
                                    if rescue_fail_time >= last_check_time:
                                        update_failed_record[vin]["问题详情"] = "任务自动救援"
                                        update_failed_record[vin]["总压测次数"] = 1
                                        update_failed_record[vin]["成功次数"] = 1
                                        update_failed_record[vin]["日期"] = round(rescue_fail_time.timestamp() * 1000)
                                        self.update_feishu_access_token()
                                        self.feishu.add_record_in_table(table_id="tblD6s278dLS5uU5", data=update_failed_record[vin])


                                if "重刷成功" in timeline_node["message"]:
                                    logger.info(f"VIN—{vin}, TaskId—{task_id}, 检查到重刷成功")
                                    retry_fail_time = datetime.datetime.strptime(timeline_node["time"], "%Y-%m-%d %H:%M:%S")
                                    if retry_fail_time >= last_check_time:
                                        update_failed_record[vin]["问题详情"] = "重刷成功"
                                        update_failed_record[vin]["总压测次数"] = 1
                                        update_failed_record[vin]["成功次数"] = 1
                                        update_failed_record[vin]["日期"] = round(retry_fail_time.timestamp() * 1000)
                                        self.update_feishu_access_token()
                                        self.feishu.add_record_in_table(table_id="tblD6s278dLS5uU5", data=update_failed_record[vin])
                                last_check_time = datetime.datetime.now()

                            if valid_result_flag.get(vin):
                                valid_result_flag[vin] = False
                                if trigger_update_flag[vin] and vin not in bench_list:
                                    appointment_record[vin]["总压测次数"] = 1
                                    appointment_record[vin]["成功次数"] = 1
                                    appointment_record[vin]["升级方式_暂存"] = ["夜间升级"]
                                    appointment_record[vin]["夜间升级"] = "是"
                                    appointment_record[vin]["日期"] = round(time.time() * 1000)
                                    self.update_feishu_access_token()
                                    self.feishu.add_record_in_table(table_id="tblD6s278dLS5uU5", data=appointment_record[vin])
                                else:
                                    record_id = vin_record_info[vin]
                                    vehicle_test_result[record_id]["总压测次数"] += 1
                                    vehicle_test_result[record_id]["成功次数"] += 1
                                    vehicle_test_result[record_id]["日期"] = round(time.time() * 1000)
                                    self.update_feishu_access_token()
                                    self.feishu.update_record_in_table(table_id="tblD6s278dLS5uU5", record_id=record_id, data=vehicle_test_result[record_id])
                            time.sleep(50)
                            self.tsp.trigger_vsp_fota(VSP.Repub, task_id, vin)
                        elif vsp_status == 19:
                            logger.info(f"{task_info}FOTA失败 ===========")
                            if valid_result_flag.get(vin):
                                valid_result_flag[vin] = False
                                if trigger_update_flag[vin] and vin not in bench_list:
                                    appointment_record[vin]["总压测次数"] = 1
                                    appointment_record[vin]["失败次数"] = 1
                                    appointment_record[vin]["升级方式_暂存"] = ["夜间升级"]
                                    appointment_record[vin]["夜间升级"] = "是"
                                    appointment_record[vin]["日期"] = round(time.time() * 1000)
                                    self.update_feishu_access_token()
                                    self.feishu.add_record_in_table(table_id="tblD6s278dLS5uU5", data=appointment_record[vin])
                                else:
                                    record_id = vin_record_info[vin]
                                    vehicle_test_result[record_id]["总压测次数"] += 1
                                    vehicle_test_result[record_id]["失败次数"] += 1
                                    vehicle_test_result[record_id]["日期"] = round(time.time() * 1000)
                                    self.update_feishu_access_token()
                                    self.feishu.update_record_in_table(table_id="tblD6s278dLS5uU5", record_id=record_id, data=vehicle_test_result[record_id])
                        elif vsp_status == 20:
                            logger.info(f"{task_info}FOTA取消, Repub Task ===========")
                            self.tsp.trigger_vsp_fota(VSP.Repub, task_id, vin)
                        else:
                            logger.info(f"{task_info}VSP status is {vsp_status} ===========")
            except Exception as e:
                logger.error("An exception occurred: %s", traceback.format_exc())
    
    def update_feishu_access_token(self):
        self.feishu.get_tenant_access_token()
        self.feishu.get_app_access_token()
        self.feishu.get_user_access_token()
        self.feishu.get_bitable_app_access_token(document_id='TMhIwUiHtiseKMkJe1KcY5BNnxd')

if __name__ == "__main__":
    pass