
'''
Author: liu.yang
Date: 2023-02-01 19:05:06
LastEditors: Do not edit
LastEditTime: 2023-07-27 20:54:55
FilePath: /yangliu/sat/xat_cases/legacy/bgm/case_helper/fota_case_helper/tsp_helper.py
'''
import os
import sys,time

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))
sys.path.append(os.path.join(current_path, "../../../.."))
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
from xat_ecu.legacy.common.logger import logger
# from groot2.cloud.biz.fota.portal_task_manager import FotaPortalTaskManager
from groot2.cloud.biz.fota.portal_task_manager import FotaPortalTaskManager

class Tsp_Helper:
    # 封装了 fota-云端 交互相关接口
    def __init__(self, task_id, vid, vin):
        self.ota = FotaPortalTaskManager(task_id=task_id,user_name='public_fota_test',password=__import__("os").environ.get('XAT_CREDENTIAL____BGM_CASE_HELPER_FOTA_CASE_HELPER_TSP_HELPER_PY_PASSWORD', ""))
        self.task_id = task_id 
        self.vid = vid
        self.vin = vin

    def cancel_fota_task(self):
        # 取消云端fota任务
        task_info = self.ota.get_sub_task_vehicles(vin=self.vin)
        ids = task_info['data']['list'][0]['id']
        cancel_result = self.ota.cancel(id_list = [ids], reason = "Script call")
        
        # if cancel_result["msg"] == "success":
        #     logger.info("succeed to cancel task")
        #     return True
        # else:
        #     logger.info("fail to cancel task")
        #     return False
        retry_count = 0
        while True:
            time.sleep(2)
            if cancel_result["msg"] == "success":
                logger.info("succeed to cancel task")
                return True
            elif cancel_result["msg"] == "fail":
                logger.info("fail to cancel task")
                return False
            else:
                cancel_result = self.ota.cancel(id_list = [ids], reason = "Script call")
                retry_count = retry_count + 1
                time.sleep(2)
                logger.error(f"cancle times :{retry_count}, content is 【{cancel_result}】")
                if retry_count > 10:
                    logger.error("reach Max retry times")
                    break

    def repub_fota_task(self):
        task_info = self.ota.get_sub_task_vehicles(vin=self.vin)
        ids = task_info['data']['list'][0]['id']
        # repub = self.ota.repub()
        repub = self.ota.re_deploy_vehicle_task([ids])
        retry_count = 0
        while True:
            time.sleep(2)
            if repub["msg"] == "success":
                logger.info("succeed to repub task")
                return True
            elif repub["msg"] == "fail":
                logger.info("fail to repub task")
                return False
            else:
                repub = self.ota.re_deploy_vehicle_task([ids])
                retry_count = retry_count + 1
                time.sleep(2)
                logger.error(f"repub times :{retry_count}, content is 【{repub}】")
                if retry_count > 10:
                    logger.error("reach Max retry times")
                    break

    def till_vsp_status_to(self, target_status):
        while True:
            curr_status = self.get_fota_status()
            if curr_status == target_status:
                return True
            else:
                time.sleep(3)
                logger.info(f"Current VSP Satus is {curr_status}")
        
    def reset_fota_task(self):
        # 重置云端fota任务
        task_info = self.ota.get_sub_task_vehicles(vin=self.vin)
        ids = task_info['data']['list'][0]['id']
        reset = self.ota.reset(ids)
        time.sleep(2)
        # if reset["msg"] == "success":
        #     logger.info("succeed to reset task")
        #     return True
        # else:
        #     logger.info("fail to reset task")
        #     return False
        retry_count = 0
        while True:
            time.sleep(2)
            if reset["msg"] == "success":
                logger.info("succeed to reset task")
                return True
            elif reset["msg"] == "重置失败":
                logger.info("fail to reset task")
                return False
            else:
                reset = self.ota.reset(ids)
                retry_count = retry_count + 1
                time.sleep(2)
                logger.error(f"reset times :{retry_count}, content is 【{reset}】")
                if retry_count > 10:
                    logger.error("reach Max retry times")
                    break
        
    def get_fota_status(self):
        """
            查看当前任务状态
            {"code":14,"msg":"推送中"},
            {"code":15,"msg":"推送成功"},
            {"code":16,"msg":"推送失败"},
            {"code":4,"msg":"下载中"},
            {"code":5,"msg":"下载成功"},
            {"code":8,"msg":"升级中"},
            {"code":10,"msg":"升级失败"},
            {"code":20,"msg":"FOTA取消"},
            {"code":18,"msg":"FOTA成功"},
            {"code":19,"msg":"FOTA失败"}
        """
        sub_tasks = self.ota.get_sub_task_vehicles(vin=self.vin, deliver_city="", debug=True)
        # fota_status = sub_tasks["data"]["list"][0]['vehicleUpgradeStatusTxt']
        update_status = sub_tasks["data"]["list"][0]['vehicleUpgradeStatus']
        logger.info(f"vsp fota status is {update_status}")
        return update_status
        # sub_tasks = self.ota.get_sub_task_vehicles(vin=self.vin, deliver_city=315336)
        # fota_status =  sub_tasks["data"]["list"][0]['vehicleUpgradeStatusTxt']
        # logger.info(f"vsp fota status is {fota_status}")
        # return sub_tasks["data"]["list"][0]['vehicleUpgradeStatus']

    def get_error_code(self):
        sub_tasks = self.ota.get_sub_task_vehicles(vin=self.vin, deliver_city="", debug=True)
        logger.info(sub_tasks)
        error_code = sub_tasks["data"]["list"][0]['vehicleUpgradeCode']
        if error_code:
            logger.info(f"ERROR CODE is {error_code}")
        else:
            logger.info("/////////////////")
        return error_code
    
    def is_fota_failed(self):
        # 查看当前
        if self.get_fota_status == 16:
            logger.info("push task fail，please check task")
            return True
        elif self.get_fota_status == 10:
            logger.info("update fail，please see see log")
            return True
        else:
            logger.info("fota is ok, let's go on")
            return False
        
    def get_task_name(self):
        task_name = self.ota.get_sub_tasks()["data"]["list"][0]["vehicleDescription"]
        return task_name    
        
if __name__ == "__main__":
    tsp169 = Tsp_Helper(task_id=8128,vid="f3b258e2e847e71e20fd01fe33b7900b",vin="JDS0ATESTBENCH074")
    tsp169.repub_fota_task()
    tsp169.reset_fota_task()
    tsp169.cancel_fota_task()
    
    
    # tsp169.repub_fota_task()
    # tsp.repub_fota_task()