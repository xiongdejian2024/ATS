import os
import sys
import pytest
import allure
import yaml
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_e2e import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
       
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
 
    def test_fota_caseid_004(self):
        # softid_vinList_dic = {'5480': ['L6T79P2N2PP002437']}
        taskid_vinList_dic = {}
        for soft_id, vin_list in self.e2e_info.items():
            for vin in vin_list:
                logger.info(f"========== {soft_id}, {vin} ==========")
                cur_taskid = 0
                check_result = self.tsp.check_task_existence(vin=vin, soft_id=soft_id)
                if check_result[0]:
                    #当前有有效任务
                    cur_taskid = check_result[1]
                    logger.info(f"{vin}: {soft_id} 存在有效任务:{cur_taskid}")
                    consuming_flag = self.tsp.is_task_consuming(task_id=cur_taskid, vin=vin)
                    if consuming_flag:
                        logger.info(f"当前有效任务:{cur_taskid}正在消费")
                        if f"{cur_taskid}" in taskid_vinList_dic:
                            taskid_vinList_dic[f"{cur_taskid}"].append(f"{vin}")
                        else:
                           taskid_vinList_dic[f"{cur_taskid}"] = [f"{vin}"]
                    else: 
                       assert False, f"{vin} 非当前任务正在消费"
                else:
                    #当前无有效任务
                    logger.info(f"{vin}: {soft_id} 不存在有效任务")
                    self.tsp.create_vsp_task(vin=vin,
                                         skip_ecu=get_skip_ecu_list(vin=vin),
                                         target_soft_id=soft_id)
                    cur_taskid = self.tsp.check_task_existence(vin=vin, soft_id=soft_id)[1]
                    logger.info(f"{vin}: {soft_id} 新建有效任务:{cur_taskid}")
                    consuming_flag = self.tsp.is_task_consuming(task_id=cur_taskid, vin=vin)
                    if consuming_flag:
                        logger.info(f"新建，当前有效任务:{cur_taskid}正在消费")
                        if f"{cur_taskid}" in taskid_vinList_dic:
                            taskid_vinList_dic[f"{cur_taskid}"].append(f"{vin}")
                        else:
                           taskid_vinList_dic[f"{cur_taskid}"] = [f"{vin}"]
                    else: 
                       assert False, f"{vin} 非当前任务正在消费"  
        logger.info(f"【taskid && vin】:\n{taskid_vinList_dic}")
        with open('config/taskid_vin.json', 'w') as file:
            json.dump(taskid_vinList_dic, file)
           
def get_skip_ecu_list(vin):
    with open('config/SOA_QA_Vehicle.yaml', 'r') as f:
        conf = yaml.safe_load(f)
    if vin in conf:
        skip_ecu_list = conf[vin]['faulty_ecu']
        logger.info(skip_ecu_list)
    else:
        assert False, f"Not Found vin:{vin}"
    return skip_ecu_list
        
if __name__ == "__main__":
    pass

    




