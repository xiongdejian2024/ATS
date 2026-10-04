import os
import sys
import pytest
import allure
import re
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("基础架构")
@allure.story("remote_rescue")
class Test_Remote_Rescue(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("VehicleModeService_client")])
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
                                    FOTA_Skip_Debug.start_download,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ])
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.sd_tester.reset_bgm()
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.stop_tester_present()
        self.io.bgm_diag_line_down()
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_epb_sts(sts=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.full
    @allure.title("四域重启_重启指令调用成功_重启失败_诊断仲裁失败【5204】")
    def test_remote_rescue_caseid_1987997(self):
        self.io.bgm_diag_line_up()
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords=['CheckState:restart failed',
                                                                                            'data: {"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":0},"responseCode":"5204"',
                                                                                            'data: {"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":0},"responseCode":"52F1"'], timeout=100):
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.ResetDomain)

    @pytest.mark.full
    @allure.title("四域重启_重启指令调用成功_重启失败_下切失败【5203】")
    def test_remote_rescue_caseid_1987998(self):
        self.io.bgm_diag_line_down()
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_epb_sts(sts=3)
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords=['CheckState:restart failed',
                                                                                                'data: {"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":0},"responseCode":"5203"',
                                                                                                'data: {"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":0},"responseCode":"52F1"'], timeout=30):
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.ResetDomain)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        
    @pytest.mark.full
    @allure.title("四域重启_重启指令调用成功_重启失败_在FOTA升级中【5202】")
    def test_remote_rescue_caseid_1987999(self):
        # self.mix.back_fota_to(fota_sts=FOTAMasteSts.UPDATE, taskid=self.taskid)
        # with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords=['CheckState:restart failed',
        #                                                                                     'data: {"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":0},"responseCode":"5202"',
        #                                                                                     'data: {"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":0},"responseCode":"52F1"'], timeout=100):
        #     self.tsp.trigger_remote_rescue(rescue_type=RescueType.ResetDomain)
        # self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        # self.mix.fota_back_to_idle()
        pass #SOA-29289

    @pytest.mark.full
    @allure.title("四域重启_重启指令调用成功_服务调用失败")
    def test_remote_rescue_caseid_1988001(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.UPDATE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords=['IsInit:Not Available Service : ObtDiagService',
                                                                                                'data: {"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":0},"responseCode":"5001"',
                                                                                                'data: {"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":0},"responseCode":"52F1"'], timeout=100):
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.ResetDomain)
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        self.mix.fota_back_to_idle()
        pass 

    @pytest.mark.full
    @allure.title("四域重启_重启指令调用成功_重启失败_档位不在P挡【5201】")
    def test_remote_rescue_caseid_1988000(self):
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.set_epb_sts(sts=0)
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords=['CheckState:restart failed',
                                                                                            'data: {"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":0},"responseCode":"5201"',
                                                                                            'data: {"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":0},"responseCode":"52F1"'], timeout=100):
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.ResetDomain)

    @pytest.mark.sanity
    @allure.title("四域重启_重启指令调用成功_重启成功【52F1】")
    def test_remote_rescue_caseid_1988003(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords=['{"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":1},"responseCode":"52F1"',
                                                                                            'send data failed, ret: 613'], timeout=100):
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.ResetDomain)
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='changeState:change state: init ==> rescue', timeout=300):
            pass #重启等待TCAM 恢复网络
        
    @pytest.mark.smoke
    @allure.title("四域重启_当前无执行中的重启指令")
    def test_remote_rescue_caseid_1988004(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords=['{"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":1},"responseCode":"52F1"',
                                                                                            'changeState:change state: init ==> rescue'], timeout=300):
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.ResetDomain)

#     @pytest.mark.full
    @allure.title("四域重启_当前有执行中的重启指令【5002】")
    def test_remote_rescue_caseid_1988005(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='data: {"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":0},"responseCode":"5002"', timeout=60):
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.ResetDomain)
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.ResetDomain)
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='changeState:change state: init ==> rescue', timeout=300):
            pass #重启等待TCAM 恢复网络

    @pytest.mark.smoke
    @allure.title("四域重启_指令下发")
    def test_remote_rescue_caseid_1988006(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='data: {"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":0},"responseCode":"50F1"', timeout=60):
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.ResetDomain)
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='changeState:change state: init ==> rescue', timeout=300):
            pass #重启等待TCAM 恢复网络

# @allure.feature("基础架构")
# @allure.story("remote_rescue")
# class Test_Remote_Rescue_SOAError(TestABCBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)
        
#     def before_each_func(self, ecu):
#         super().before_each_func(ecu)
#         self.io.bgm_diag_line_down()
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         self.bus_comm.set_epb_sts(sts=3)
#         self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
 
#     def after_each_func(self, ecu):
#         super().after_each_func(ecu)
       
#     def after_class(self, ecu):
#         super().after_class(self, ecu)
        
#     @pytest.mark.full
#     @allure.title("四域重启_重启指令调用成功_服务调用失败")
#     def test_remote_rescue_caseid_1988001(self):
#         try:
#             self.io.bgm_power_off()
#             self.soa.update([('ObtDiagService_server')])
#             sleep(10)
#             self.io.bgm_power_on()
#             sleep(30)
#             self.soa.soa_partner.stop_single_partner("ObtDiagService_server")
#             with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords=['IsInit:Not Available Service : ObtDiagService',
#                                                                                                 'data: {"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":0},"responseCode":"5001"',
#                                                                                                 'data: {"cmd":2,"cmdDetail":{"inhibitControl":0,"resetControl":0},"responseCode":"52F1"'], timeout=100):
#                 self.tsp.trigger_remote_rescue(rescue_type=RescueType.ResetDomain)
#         finally:
#             self.sd_tester.reset_bgm()           

if __name__ == "__main__":
    pass