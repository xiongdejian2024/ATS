import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.tcam.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("UpdateAgentService","client","TCAM_UA_Service")])
        sleep(20)
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @allure.title("TCAM升级")    
    def test_fota_caseid_1979790(self):
        while True:
            time.sleep(5)
            ua_status = self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status)
            ua_preUpdateStatus = self.soa.get_ua_status(DOMAIN.TCAM,UA_EVENT.PreUpdateStatus)
            if ua_status == 0:
                logger.info("UA Status == 1, 【Start Download】")
                self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, self.TCAM_Download_Req)
            elif ua_status == 1:
                logger.info("UA Status == 1, Still Downloading")
                time.sleep(10)
            elif ua_status == 2 and ua_preUpdateStatus == 0:
                logger.info("UA Status == 2, 【Pre Update】")
                self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.PreUpdate)
            elif ua_status == 2 and ua_preUpdateStatus == 1:
                logger.info("UA Status == 2, Still Decrypting")
                time.sleep(10)
            elif ua_status == 2 and ua_preUpdateStatus == 2:
                logger.info("UA Status == 2, 【Start Update】")
                self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartUpdate)
            elif ua_status == 3:
                logger.info("UA Status == 3, Still Installing")
                time.sleep(30)
            elif ua_status == 4:
                logger.info("UA Status == 4, 【Start Active】")
                self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.Activate)
                time.sleep(240)
            elif ua_status == 6:
                logger.info("UA Status == 6, 【Finish Update】")
                self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.FinishUpdate)
                break
            elif ua_status == 8:
                logger.info("UA Status == 8, Still Activating")
                time.sleep(30)
            else:
                logger.error(f"UA Status {ua_status} Abnormal")

            
if __name__ == "__main__":
    pass
      
    




