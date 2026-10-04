# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
# '''
# @filename     : test_diag_bgm_arbitrate.py
# @time         : 2024/03/15 09:46
# @author       : o_lijing.pan@external.jiduauto.com
# @description  : 诊断仲裁用例
# '''


# import allure
# import pytest
# from sdk_interface.abc_interface import *
# from test_case.bgm.case_helper.test_fota_base import TestABCBase
# from ecu_simulator.common.logmanagment.logmanager import logger

# from ecu_simulator.soa_partner.src.base_partner import *
# from ecu_simulator.soa_partner.src.partner_const import *
# from test_case.bgm.case_helper.diag_case_helper.DiagTestBase import *
# from ecu_simulator.sdk.digital_key.digital_key_class import *
# from test_case.soa.case_helper.test_base import TestBase

# class Test_Arbitrate(TestABCBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)
#         logger.info("初始化环境")
#         self.mix.init_boot_per()
#         logger.info("Fota相关配置")   
#         self.soa.update([
#                          ("FotaMasterService","client"),
#                          ("V2TRoutingForwarder","client","V2TCcpForwarder"),
#                          ("CCPMasterService", "client" ,"CcpMasterService"),
#                          ("VehicleModeService_client")
#                         ])
#         self.ssh.ccp_skip_debug([Ccp_Skip_Debug.skip_verify,
#                                  Ccp_Skip_Debug.skip_acu,
#                                  Ccp_Skip_Debug.skip_cdc])
#         self.sd_tester.reset_bgm()
#         self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
#                                     FOTA_Skip_Debug.baseline,
#                                     FOTA_Skip_Debug.before_group_1081,
#                                     FOTA_Skip_Debug.before_group_hv_ctl,
#                                     FOTA_Skip_Debug.ecm3_down_hv,
#                                     FOTA_Skip_Debug.fota_mode_requeset_acu,
#                                     FOTA_Skip_Debug.fota_mode_requeset_cdc,
#                                     FOTA_Skip_Debug.fota_mode_requeset_ecm3,
#                                     FOTA_Skip_Debug.upload_version_from_debug_file,
#                                     FOTA_Skip_Debug.CDC_UA,
#                                     FOTA_Skip_Debug.ACU_UA,
#                                     FOTA_Skip_Debug.update_precondition_check,
#                                     # FOTA_Skip_Debug.version_collect,
#                                     FOTA_Skip_Debug.cdc_acu_doip_check
#                                     ], allow_sleep=False) 
#         self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False, allow_sleep=False)
#         self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
#         self.tsp.get_remote_diag_token()
#         time.sleep(20) 

#     def before_each_func(self, ecu):
#         super().before_each_func(ecu)
#         self.ssh.set_airplane_mode(isOn.Off)
#         self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
#         self.bus_comm.set_vehspd_gear(vehspd = 0.0)
#         self.mix.back_ccp_status_to_Idle()
#         logger.info("诊断激活线拉低")
#         self.io.bgm_diag_line_down()
#         logger.info("关闭远程诊断会话")
#         self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)
#         logger.info("case开始运行*******************************************************")
 
#     def after_each_func(self, ecu):
#         logger.info("case结束运行*******************************************************")
#         super().after_each_func(ecu)
        
#     def after_class(self, ecu):
#         logger.info("初始化环境")
#         self.mix.init_boot_per() 
#         logger.info("after_class")
#         super().after_class(self, ecu)

#     @pytest.mark.sanity
#     @allure.title("验证当BGM正同时运行本地诊断和Fod版本收集任务，此时接收到其他诊断任务，会忽略新来的任务")
#     def test_caseid_1985583(self):
#         with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_", 
#                                                         keywords = ["fota update win", "concurrent services fota update,idle"],
#                                                         unexpect_keywords = "remote diag win",
#                                                         timeout = 120):
#             logger.info("发起FoD功能配置业务")
#             self.fod_bench_config['preCheckUserIn'] = 1
#             self.soa.call_vehicle_api(V2T_API.FOD, payload = self.fod_bench_config)
#             time.sleep(5)
#             logger.info("诊断激活线拉高")
#             self.io.bgm_diag_line_up()
#             logger.info("发起远程诊断业务")
#             self.tsp.send_remote_diag_cmd(cmd_type = CmdType.SessionOpen)

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于RVS版本收集，此时接收到EDR数据上传，BGM会忽略EDR数据上传任务")
#     def test_caseid_1985584(self):
#         with allure.step("RVS版本收集与EDR数据上传优先级判断"):
#             time.sleep(10)
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_",
#                                                           keywords = "Received heart beat for remote_vehicle_status",
#                                                           unexpect_keywords = ["Release daily version collection", "Received heart beat for edr_service"],
#                                                           timeout = 120):
#                 logger.info("切换UsageMode为CONVENIENCE")
#                 self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于RVS版本收集，此时接收到Fod版本收集任务，BGM会终止当前任务，从而路由Fod版本收集任务")
#     def test_caseid_1985585(self):
#         with allure.step("RVS版本收集与Fod版本收集优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_",
#                                                           keywords = ["Release daily version collection", "fota version collection win"],
#                                                           timeout = 120):
#                 logger.info("发起Fota版本收集业务")
#                 self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于RVS版本收集，此时接收到远程诊断任务，BGM会终止当前任务，从而路由远程诊断任务")
#     def test_caseid_1985586(self):
#         with allure.step("RVS版本收集与远程诊断优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_",
#                                                           keywords = ["Release daily version collection", "remote diag win"],
#                                                           timeout = 120):
#                 logger.info("发起远程诊断业务")
#                 self.tsp.send_remote_diag_cmd(cmd_type = CmdType.SessionOpen)
#             # logger.info("发起远程诊断业务")
#             # self.tsp.send_remote_diag_cmd(cmd_type = CmdType.SessionOpen) 

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于RVS版本收集，此时接收到本地诊断任务，BGM会终止当前任务，从而路由本地诊断")
#     def test_caseid_1985588(self):
#         with allure.step("RVS版本收集与本地诊断优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_",
#                                                           keywords = ["Release daily version collection", "local diag win"],
#                                                           timeout = 120):
#                 logger.info("诊断激活线拉高")
#                 self.io.bgm_diag_line_up()

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于FOTA版本收集，此时接收到RVS版本收集任务，BGM会忽略RVS版本收集任务")
#     def test_caseid_1985589(self):
#         time.sleep(10)
#         with allure.step("FOTA版本收集业务与RVS版本收集的优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_", keywords = "fota version collection win",
#                                                           unexpect_keywords = ["daily version collection win", "Release fota version collection"],
#                                                           timeout = 120):
#                 logger.info("发起Fota版本收集业务")
#                 self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
#                 logger.info("切换UsageMode为DRIVING")
#                 self.sd_tester.change_usage_mode(UsageMode.DRIVING)

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于FOTA版本收集，此时接收到远程诊断任务，BGM会终止当前任务，从而路由远程诊断任务")
#     def test_caseid_1985590(self):
#         with allure.step("FOTA版本收集业务与远程诊断的优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_",
#                                                           keywords = ["fota version collection win", "Release fota version collection", "remote diag win"],
#                                                           timeout = 120):
#                 logger.info("发起Fota版本收集业务")
#                 self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
#                 logger.info("发起远程诊断业务")
#                 self.tsp.send_remote_diag_cmd(cmd_type = CmdType.SessionOpen)

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于FOTA版本收集，此时接收到本地诊断任务，BGM会终止当前任务，从而路由本地诊断任务")
#     def test_caseid_1985592(self):
#         with allure.step("FOTA版本收集业务与本地诊断的优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_",
#                                                           keywords = ["fota version collection win", "Release fota version collection", "local diag win"],
#                                                           timeout = 120):
#                 logger.info("发起Fota版本收集业务")
#                 self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
#                 logger.info("诊断激活线拉高")
#                 self.io.bgm_diag_line_up() 

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于远程诊断，此时接收到RVS版本收集任务，BGM会终止当前任务，从而路由RVS版本收集任务")
#     def test_caseid_1985593(self):
#         with allure.step("远程诊断业务与RVS版本收集的优先级判断"):
#             time.sleep(5)
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_", keywords = "remote diag win",
#                                                           unexpect_keywords = ["daily version collection win", "Release remote diag"],
#                                                           timeout = 120):
#                 logger.info("发起远程诊断业务")
#                 self.tsp.send_remote_diag_cmd(cmd_type = CmdType.SessionOpen)
#                 logger.info("发起RVS版本收集业务")
#                 self.sd_tester.change_usage_mode(UsageMode.DRIVING)

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于远程诊断，此时接收到Fod版本收集任务，BGM会终止当前任务，从而路由Fod版本收集任务")
#     def test_caseid_1985594(self):
#         with allure.step("远程诊断业务与Fod版本收集的优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_", keywords = "remote diag win",
#                                                           unexpect_keywords = ["fota version collection win", "Release remote diag"],
#                                                           timeout = 120):
#                 logger.info("发起远程诊断业务")
#                 self.tsp.send_remote_diag_cmd(cmd_type = CmdType.SessionOpen)
#                 logger.info("发起Fota版本收集业务")
#                 self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于远程诊断，此时接收到本地诊断任务，BGM会终止当前任务，从而路由本地诊断任务")
#     def test_caseid_1985596(self):
#         with allure.step("远程诊断业务与本地诊断的优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_", 
#                                                           keywords = ["remote diag win", "Release remote diag", "local diag win"],
#                                                           timeout = 120):
#                 logger.info("发起远程诊断业务")
#                 self.tsp.send_remote_diag_cmd(cmd_type = CmdType.SessionOpen)
#                 time.sleep(5)
#                 logger.info("诊断激活线拉高")
#                 self.io.bgm_diag_line_up()

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于FoD功能配置任务，此时接收到本地诊断任务，BGM会并行执行本地诊断任务")
#     def test_caseid_1985603(self):
#         with allure.step("FoD版本收集与本地诊断的优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_", 
#                                                           keywords = ["fota update win", "concurrent services fota update,idle"],
#                                                           unexpect_keywords = ["Release fota update", "Release local diag"],
#                                                           timeout = 120):
#                 logger.info("发起FoD功能配置业务")
#                 self.fod_bench_config['preCheckUserIn'] = 1
#                 self.soa.call_vehicle_api(V2T_API.FOD, payload = self.fod_bench_config)
#                 time.sleep(5)
#                 logger.info("诊断激活线拉高")
#                 self.io.bgm_diag_line_up()


#     @pytest.mark.sanity
#     @allure.title("验证BGM处于本地诊断，此时接收到RVS版本收集任务，BGM会忽略RVS版本收集任务")
#     def test_caseid_1985604(self):
#         with allure.step("本地诊断与RVS业务的优先级判断"):
#             time.sleep(5)
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_", keywords = "local diag win", 
#                                                           unexpect_keywords = ["daily version collection win", "Release local diag"],
#                                                           timeout = 120):
#                 logger.info("诊断激活线拉高")
#                 self.io.bgm_diag_line_up() 
#                 logger.info("切换UsageMode为DRIVING")
#                 self.sd_tester.change_usage_mode(UsageMode.DRIVING)

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于本地诊断，此时接收到FOTA版本收集任务，BGM会忽略FOTA版本收集任务")
#     def test_caseid_1985605(self):
#         with allure.step("本地诊断与Fota版本收集的优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_", keywords = "local diag win",
#                                                           unexpect_keywords = ["fota version collection win", "Release local diag"],
#                                                           timeout = 120):
#                 logger.info("诊断激活线拉高")
#                 self.io.bgm_diag_line_up() 
#                 logger.info("发起Fota版本收集业务")
#                 self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于本地诊断，此时接收到远程诊断任务，BGM会忽略远程诊断任务")
#     def test_caseid_1985606(self):
#         with allure.step("本地诊断与远程诊断业务的优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_", keywords = "local diag win",
#                                                           unexpect_keywords = ["remote diag win", "Release local diag"],
#                                                           timeout = 120):
#                 logger.info("诊断激活线拉高")
#                 self.io.bgm_diag_line_up()
#                 logger.info("发起远程诊断业务")
#                 self.tsp.send_remote_diag_cmd(cmd_type = CmdType.SessionOpen)

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于本地诊断，此时接收到FoD功能配置任务，BGM会忽略FoD功能配置任务")
#     def test_caseid_1985608(self):
#         with allure.step("本地诊断与FoD版本收集的优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_", keywords = ["local diag win"],
#                                                           unexpect_keywords = ["fota update win", "Release local diag"],
#                                                           timeout = 120):
#                 logger.info("诊断激活线拉高")
#                 self.io.bgm_diag_line_up()
#                 logger.info("发起FoD功能配置业务")
#                 self.fod_bench_config['preCheckUserIn'] = 1
#                 self.soa.call_vehicle_api(V2T_API.FOD, payload = self.fod_bench_config)


# class Test_Arbitrate_SOAPartner(TestBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)
#         self.partner = S2sBaseClass([("ObtDiagService", "client")])
#         self.log_manage = LogManagement()

#     def before_each_func(self, ecu):
#         super().before_each_func(ecu, start=False)
#         sleep(0.5)
#         self.sd_tester.change_car_mode(0)
#         self.sd_tester.change_usage_mode(1)
#         self.partner.empty_all(0.5)
#         logger.info("诊断激活线拉低")
#         self.nucapp.bgm_diag_line_down()
#         logger.info(f"case开始运行*******************************************************")

#     def after_each_func(self, ecu):
#         logger.info(f"case结束运行*******************************************************")
#         self.ipdu.resume_all_bus_send()  # 信号恢复
#         self.bgmcli.stop_bgm_tcpdump()
#         self.bgmcli.delete_bgm_tcpdump_file(bgm_log_name='*.pcap')
#         if ecu.get("testresult") != "Pass":
#             logger.error("case失败，需等待10s让环境恢复")
#             sleep(10)
#         else:
#             logger.info("case成功，需等待3s让环境恢复")
#             sleep(3)
#         logger.info("诊断激活线拉高")
#         self.nucapp.bgm_diag_line_up()
#         super().after_each_func(ecu, start=False)
 
#     def after_class(self, ecu):
#         self.partner.stop_operators()
#         self.sd_tester.stop_tester_present()
#         self.sd_tester.diagnostic_client_sim_close()  # 关闭诊断仪
#         super().after_class(self, ecu)

#     @pytest.mark.smoke
#     @allure.title("验证BGM处于本地诊断，此时接收到雨刮车窗标定任务，BGM会忽略雨刮车窗标定任务")
#     def test_caseid_1985607(self):
#         with allure.step("本地诊断与雨刮车窗标定的优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_", keywords = "local diag win",
#                                                             unexpect_keywords = ["online diag win", "Release local diag"],
#                                                             timeout = 120):
#                 time.sleep(1)
#                 logger.info("诊断激活线拉高")
#                 self.nucapp.bgm_diag_line_up()
#                 self.partner.empty_all(0.5)
#                 inputSourceList = [0,1]
#                 for i in range(len(inputSourceList)):
#                     self.partner.send_method_request(OBTDIAG_SERVICE_CLIENT, "StartEOLCali", {"source":inputSourceList[i]})

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于RVS版本收集，此时接收到雨刮车窗标定任务，BGM会终止当前任务，从而路由雨刮车窗标定任")
#     def test_caseid_1985587(self):
#         with allure.step("RVS版本收集与雨刮车窗标定优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_",
#                                                           keywords = ["Release daily version collection", "online diag win"],
#                                                           unexpect_keywords = "Release online diag",
#                                                           timeout = 120):
#                 self.partner.empty_all(0.5)
#                 inputSourceList = [0,1]
#                 for i in range(len(inputSourceList)):
#                     self.partner.send_method_request(OBTDIAG_SERVICE_CLIENT, "StartEOLCali", {"source":inputSourceList[i]})
            
#     @pytest.mark.smoke
#     @allure.title("验证BGM处于智驾标定，此时接收到雨刮车窗标定任务，BGM会忽略雨刮车窗标定任务")
#     def test_caseid_1985600(self):
#         with allure.step("智驾标定与雨刮车窗标定的优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_", keywords = ["online diag win"],
#                                                             unexpect_keywords = "Release online diag",
#                                                             timeout = 120):
#                 caliRadarList = [0,1,2,3,4]
#                 caliMethodList = [1,0]
#                 for i in range(len(caliRadarList)):
#                     for j in range(len(caliMethodList)):
#                         self.partner.send_method_request(OBTDIAG_SERVICE_CLIENT, "SetRadarCaliMode",
#                                                     {"caliRadar":caliRadarList[i],"caliMethod":caliMethodList[j]})
                
#                 self.partner.empty_all(0.5)
#                 inputSourceList = [0,1]
#                 for i in range(len(inputSourceList)):
#                     self.partner.send_method_request(OBTDIAG_SERVICE_CLIENT, "StartEOLCali", {"source":inputSourceList[i]})

#     @pytest.mark.sanity
#     @allure.title("验证BGM处于雨刮车窗标定任务，此时接收到本地诊断任务，BGM会终止当前任务，从而路由本地诊断任务")
#     def test_caseid_1985601(self):
#         with allure.step("本地诊断与雨刮车窗标定的优先级判断"):
#             with self.log_manage.check_jetlog_by_keywords(log_type = "ARB_", keywords = ["online diag win", "local diag win", "Release online diag"],
#                                                             unexpect_keywords = "Release local diag",
#                                                             timeout = 120):
#                 self.partner.empty_all(0.5)
#                 inputSourceList = [0,1]
#                 for i in range(len(inputSourceList)):
#                     self.partner.send_method_request(OBTDIAG_SERVICE_CLIENT, "StartEOLCali", {"source":inputSourceList[i]})
#                 logger.info("诊断激活线拉高")
#                 self.nucapp.bgm_diag_line_up()
