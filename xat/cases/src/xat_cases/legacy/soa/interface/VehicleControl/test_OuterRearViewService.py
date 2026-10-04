#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_OuterRearViewService.py
@Time         :2023/05/17 08:07:44
@Author       :lei.tao@jiduauto.com
@Description  :
"""
import allure
import pytest
from time import sleep
from socket import *
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.soa.case_helper.utils import *
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import *

@allure.feature("SOA服务接口")
@allure.story("整车控制/OuterRearViewService")
@pytest.mark.aqx
class TestOuterRearViewService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("OuterRearViewService", "client")])
        self.partner.method_default_timeout = 0.1
        self.sd_tester.tester_present()
             
    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(1)
        self.partner.stop_operators()       
        self.sd_tester.stop_tester_present()   
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkNotEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set_vehspd(0)
        self.sd_tester.change_car_mode(0)   
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [2]}) # stop打断
        self.set_MirrorAngle_All(0, 0, 0, 0) # 外后视镜角度
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', random.choice([0, 1, 2])) # NA/Unfolded/Folded
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', random.choice([0, 1, 2])) # NA/Unfolded/Folded
        self.sd_tester.change_usage_mode(random.choice([2, 11, 13]))
        self.partner.empty_all(2)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()    
        super().after_each_func(ecu, start=False)
        
    def ck_pdu(self,file_path,save_name,data_list1,data_list2):
        # todo 停止抓包
        self.bgmcli.stop_bgm_tcpdump()
        # todo 拉取日志 单个日志 不打包
        file_path=self.bgmcli.scp_bgm_log_to_local(bgm_log_name=save_name)
        # todo 删除所有 pcap 文件
        self.bgmcli.delete_bgm_tcpdump_file(bgm_log_name='*.pcap')
        
        #停止和删除 也在aftercase中增加进去
        # 列表里面为元祖（pdu的id，数据长度，信号起始bit位，信号长度，信号值），可以 是多个元祖
        # data_list = [list1]
        ret, res_dict = check_pdu(data_list1, file_path)            
        
        # data_list 格式 为列表，列表里面为元祖（pdu的id，数据长度，信号起始bit未，信号长度），可以 是多个元祖
        # data_list = [list2]  
        res_dict=get_pdu_value_and_time(data_list2, file_path)
        if ret==False :
             assert False, f"对应信号不存在" 
             
    def set_MirrorAngle_Right(self, horizon, vertical):
        ''' 设置右后视镜角度 '''
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "MirrPosnToCldAtPassMirrPosnAdjCldLeRi", horizon) # 水平
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "MirrPosnToCldAtPassMirrPosnAdjCldUpDwn", vertical) # 垂直
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views":[0]}, 
                                              {"out":[{"viewId": 0, "horizontalAngle": horizon, "verticalAngle":vertical}]}, timeout=3)
        
    def set_MirrorAngle_Left(self, horizon, vertical):
        ''' 设置左后视镜角度'''
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "MirrPosnToCldAtDrvrMirrPosnAdjCldUpDwn", vertical) # 垂直
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "MirrPosnToCldAtDrvrMirrPosnAdjCldLeRi", horizon) # 水平
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views":[1]}, 
                                              {"out":[{"viewId": 1, "horizontalAngle": horizon, "verticalAngle":vertical}]}, timeout=3)

    def set_MirrorAngle_All(self, left_vertical, left_horizon, right_vertical, right_horizon, sleeptime=0):
        ''' 设置左、右后视镜角度'''
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "MirrPosnToCldAtDrvrMirrPosnAdjCldUpDwn", left_vertical) # 垂直
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "MirrPosnToCldAtDrvrMirrPosnAdjCldLeRi", left_horizon) # 水平
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "MirrPosnToCldAtPassMirrPosnAdjCldUpDwn", right_vertical) # 垂直
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "MirrPosnToCldAtPassMirrPosnAdjCldLeRi", right_horizon) # 水平
        sleep(sleeptime)
                   
    def ck_MirrorAngle_and_GetMirrorAngle(self, id, horizon, vertical):
        ''' 获取&通知外后视镜角度'''
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'MirrorAngle', {"info":{"viewId": id, "horizontalAngle": horizon,"verticalAngle":vertical}})
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views":[id]}, {"out":[{"viewId": id, "horizontalAngle": horizon,"verticalAngle":vertical}]})
    
    def ck_no_MirrorAngle_and_GetMirrorAngle(self, id, horizon, vertical):
        ''' 获取&不通知外后视镜角度'''
        self.partner.ck_no_event(OUTERREARVIEW_SERVICE_CLIENT, 'MirrorAngle')
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views":[id]}, {"out":[{"viewId": id, "horizontalAngle": horizon,"verticalAngle":vertical}]})

    @allure.title("设置后视镜目标角度_Left_Unfolding/Folding_调用SetMirrorAngleTarget.viewId=1/2后_进入Unfolded/Folded")
    @pytest.mark.full
    def test_caseid_1988650(self):
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        for before_foldsts, after_foldsts in {3:1, 4:2}.items():
            for id in [1, 2]:
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":0,"direction":1}]})
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 3, timeout=0.5) # 对右侧后视镜下发非0的调节，验证 SOA-27541
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', before_foldsts) # Unfolding/Folding
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[1]}, 
                                                    {"out":[{"id":1,"foldStatus":before_foldsts}]}) 
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                                {"params": [{"viewId":id, "horizontalAngle":50, "verticalAngle":55}]})
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', after_foldsts) # Unfolded/Folded
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5) # 先停止100ms，再调节
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=1)  # 执行调节
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 3, timeout=0.5) # 由于右侧后视镜角度的实际位置不在有效范围，所以不执行调节 SOA-27541
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [random.choice([1, 2])]}) # stop打断
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)

    @allure.title("设置后视镜目标角度_Left_Unfolding/Folding_调用SetMirrorAngleTarget.viewId=1/2后_进入Folded/Unfolded_执行调节")
    @pytest.mark.sanity
    def test_caseid_1988665(self): # 210AQ版本
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        for before_foldsts, after_foldsts in {3:2, 4:1}.items(): # 不符合：3=>1 (Unfolding=>Unfolded) 或者 4=>2 (Folding=>Folded)
            for id in [1, 2]:
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', before_foldsts) # Unfolding/Folding
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[1]}, 
                                                    {"out":[{"id":1,"foldStatus":before_foldsts}]}) 
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                                {"params": [{"viewId":id, "horizontalAngle":50, "verticalAngle":55}]})
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', after_foldsts) # Unfolded/Folded
                sleep(1)
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=0.5)

    @allure.title("设置后视镜目标角度_Left_Unfolding/Folding_调用SetMirrorAngleTarget.viewId=1/2后_进入NA")
    @pytest.mark.full
    def test_caseid_1988666(self):
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        for before_foldsts in range(3, 8):
            for id in [1, 2]:
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', before_foldsts) # Unfolding/Folding
                foldsts=4 if before_foldsts>4 else before_foldsts
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[1]}, 
                                                    {"out":[{"id":1,"foldStatus":foldsts}]}) 
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                                {"params": [{"viewId":id, "horizontalAngle":50, "verticalAngle":55}]})
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 0) # NA
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5) # 先停止100ms，再调节
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=1)  # 执行调节
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [random.choice([1, 2])]}) # stop打断
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 4)
                sleep(0.5)

    @allure.title("设置后视镜目标角度_Left_Unfolding/Folding_多次调用SetMirrorAngleTarget.viewId=1/2后_进入Unfolded/Folded")
    @pytest.mark.sanity
    def test_caseid_1988667(self): # 多次调用取最后一次
        for before_foldsts, after_foldsts in {3:1, 4:2}.items():
            for id in [1, 2]:
                self.set_MirrorAngle_Left(horizon=50, vertical=50)
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', before_foldsts) # Unfolding/Folding
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[1]}, 
                                                    {"out":[{"id":1,"foldStatus":before_foldsts}]}) 
                for hor, ver in {50:55, 44:195, 55:54, 0:195}.items(): # 设置目标位置的参数角度超出有效范围时，对控制无影响
                    self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', random.choice([5, 6, 7])) # 信号改变，但是折叠状态仍保持last_vlaue
                    self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                                    {"params": [{"viewId":id, "horizontalAngle":hor, "verticalAngle":ver}]})
                    sleep(0.5)
                logger.info(f"打印当前值before_foldsts={before_foldsts};after_foldsts={after_foldsts};viewId={id}")
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', after_foldsts) # Unfolded/Folded
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 3, timeout=1)  # 执行调节
                self.set_MirrorAngle_Left(horizon=0, vertical=195) # 调整到目标位置 
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=1)

    @allure.title("设置后视镜目标角度_Left_打断逻辑_等待中调用SetMirrorAngleTarget.viewId=0_进入Unfolded/Folded_无影响")
    @pytest.mark.full
    def test_caseid_1988668(self):
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        for before_foldsts, after_foldsts in {3:1, 4:2}.items():
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', before_foldsts) # Unfolding/Folding
            self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[1]}, 
                                                {"out":[{"id":1,"foldStatus":before_foldsts}]}) 
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                            {"params": [{"viewId":1, "horizontalAngle":0, "verticalAngle":195}]})        
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                            {"params": [{"viewId":0, "horizontalAngle":50, "verticalAngle":55}]})
            sleep(1)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', after_foldsts) # Unfolded/Folded
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 3, timeout=1)    
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [2]}) # stop打断
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)

    @allure.title("设置后视镜目标角度_Left_打断逻辑_执行中调用SetMirrorAngleTarget.viewId=0_无影响")
    @pytest.mark.full
    def test_caseid_1988669(self):
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        for foldsts in [1, 2]:
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', foldsts) # Unfolded/Folded
            self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[1]}, 
                                                  {"out":[{"id":1,"foldStatus":foldsts}]}) 
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                         {"params": [{"viewId":1, "horizontalAngle":55, "verticalAngle":54}]})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5) # 先停止100ms，再调节  
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1)       
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                            {"params": [{"viewId":0, "horizontalAngle":0, "verticalAngle":195}]})   
            sleep(8)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1)   
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=3)

    @allure.title("设置后视镜目标角度_Left_打断逻辑_执行中遍历右后视镜的折叠状态_无影响")
    @pytest.mark.full
    def test_caseid_1988670(self): # ReView:|jetlogd start  
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                         {"params": [{"viewId":1, "horizontalAngle":55, "verticalAngle":54}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1) 
        for mirr_pass in range(8):
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', mirr_pass)  
            sleep(0.5) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1)
        self.set_MirrorAngle_Left(horizon=55, vertical=54)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=1)

    @allure.title("设置后视镜目标角度_Left_打断逻辑_执行中左后视镜的折叠状态变为Unfolding/Folding_执行被打断")
    @pytest.mark.smoke
    def test_caseid_1988671(self): # ReView:|jetlogd start  
        for foldsts_ing, foldsts_ed in {3:2, 4:1}.items():
            self.set_MirrorAngle_Left(horizon=50, vertical=50)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', random.choice([foldsts_ed, 0])) # 折叠状态满足
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                            {"params": [{"viewId":1, "horizontalAngle":55, "verticalAngle":54}]})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1) 
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', foldsts_ing)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=1) # 打断

    @allure.title("设置后视镜目标角度_Left_打断逻辑_执行中多次调用SetMirrorAngleTarget.viewId=1/2_执行被打断")
    @pytest.mark.full
    def test_caseid_1988679(self): 
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                        {"params": [{"viewId":1, "horizontalAngle":55, "verticalAngle":54}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1) 
        for id in [1, 2]:
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                             {"params": [{"viewId":id, "horizontalAngle":50, "verticalAngle":55}]})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5) # 先停止100ms，再调节  
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=1)  

    @allure.title("设置后视镜目标角度_Left_打断逻辑_执行中左后视镜的折叠状态变为NA/Unfolded/Folded_不打断_再次调用")
    @pytest.mark.sanity
    def test_caseid_1988684(self): # ReView:|jetlogd start  
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 2)
        for foldsts in range(3):
            self.set_MirrorAngle_Left(horizon=50, vertical=50)
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                            {"params": [{"viewId":1, "horizontalAngle":55, "verticalAngle":54}]})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', foldsts) # NA/Unfolded/Folded
            self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[1]}, 
                                                  {"out":[{"id":1,"foldStatus":foldsts}]}) 
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1)
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                                {"params": [{"viewId":1, "horizontalAngle":50, "verticalAngle":55}]})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5) # 先停止100ms，再调节  
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=1)       

    @allure.title("设置后视镜目标角度_UsgMod条件_等待中UsgMod不满足_折叠状态满足后不响应")
    @pytest.mark.sanity
    def test_caseid_1988685(self):
        for before_foldsts, after_foldsts in {3:1, 4:2}.items():
            self.sd_tester.change_usage_mode(random.choice([2, 11, 13]))
            self.set_MirrorAngle_Left(horizon=50, vertical=50)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', before_foldsts) 
            self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[1]}, 
                                                  {"out":[{"id":1,"foldStatus":before_foldsts}]}) 
            self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'SetMirrorAngleTarget', 
                                                {"params": [{"viewId":1, "horizontalAngle":50, "verticalAngle":55}]}, 
                                                {"out":1}) 
            self.sd_tester.change_usage_mode(random.choice([0, 1]))
            sleep(1)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', after_foldsts) 
            sleep(0.5)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=1) 

    @allure.title("设置后视镜目标角度_UsgMod条件_执行中UsgMod不满足")
    @pytest.mark.full
    def test_caseid_1988686(self): 
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                        {"params": [{"viewId":1, "horizontalAngle":55, "verticalAngle":54}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1) 
        self.sd_tester.change_usage_mode(random.choice([0, 1]))
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1)          

    @allure.title("设置后视镜目标角度_Right_Unfolding/Folding_调用SetMirrorAngleTarget.viewId=0/2后_进入Unfolded/Folded")
    @pytest.mark.sanity
    def test_caseid_1988688(self):
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        for before_foldsts, after_foldsts in {3:1, 4:2}.items():
            for id in [0, 2]:
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":1,"direction":1}]})
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 3, timeout=0.5) # 对左侧后视镜下发非0的调节，验证 SOA-27541
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', before_foldsts) # Unfolding/Folding
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[0]}, 
                                                    {"out":[{"id":0,"foldStatus":before_foldsts}]}) 
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                                {"params": [{"viewId":id, "horizontalAngle":50, "verticalAngle":55}]})
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', after_foldsts) # Unfolded/Folded
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5) # 先停止100ms，再调节
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=1)  # 执行调节
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 3, timeout=0.5) # 对左侧后视镜下发非0的调节，验证 SOA-27541
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [random.choice([0, 2])]}) # stop打断
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)

    @allure.title("设置后视镜目标角度_Right_Unfolding/Folding_调用SetMirrorAngleTarget.viewId=0/2后_进入Folded/Unfolded_执行调节")
    @pytest.mark.full
    def test_caseid_1988689(self):
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        for before_foldsts, after_foldsts in {3:2, 4:1}.items(): # 不符合：3=>1 (Unfolding=>Unfolded) 或者 4=>2 (Folding=>Folded)
            for id in [0, 2]:
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', before_foldsts) # Unfolding/Folding
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[0]}, 
                                                    {"out":[{"id":0,"foldStatus":before_foldsts}]}) 
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                                {"params": [{"viewId":id, "horizontalAngle":50, "verticalAngle":55}]})
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', after_foldsts) # Unfolded/Folded
                sleep(1)
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=0.5)

    @allure.title("设置后视镜目标角度_Right_Unfolding/Folding_调用SetMirrorAngleTarget.viewId=0/2后_进入NA")
    @pytest.mark.smoke
    def test_caseid_1988690(self):
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        for before_foldsts in range(3, 8):
            for id in [0, 2]:
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', before_foldsts) # Unfolding/Folding
                foldsts=4 if before_foldsts>4 else before_foldsts
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[0]}, 
                                                    {"out":[{"id":0,"foldStatus":foldsts}]}) 
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                                {"params": [{"viewId":id, "horizontalAngle":50, "verticalAngle":55}]})
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 0) # NA
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5) # 先停止100ms，再调节
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=1)  # 执行调节
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [random.choice([0, 2])]}) # stop打断
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 4)
                sleep(0.5)                

    @allure.title("设置后视镜目标角度_Right_Unfolding/Folding_多次调用SetMirrorAngleTarget.viewId=0/2后_进入Unfolded/Folded")
    @pytest.mark.full
    def test_caseid_1988691(self): # 多次调用取最后一次
        for before_foldsts, after_foldsts in {3:1, 4:2}.items():
            for id in [0, 2]:
                self.set_MirrorAngle_Right(horizon=50, vertical=50)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', before_foldsts) # Unfolding/Folding
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[0]}, 
                                                    {"out":[{"id":0,"foldStatus":before_foldsts}]}) 
                for hor, ver in {50:55, 44:195, 55:54, 0:195}.items(): # 设置目标位置的参数角度超出有效范围时，对控制无影响
                    self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', random.choice([5, 6, 7])) # 信号改变，但是折叠状态仍保持last_vlaue
                    self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                                    {"params": [{"viewId":id, "horizontalAngle":hor, "verticalAngle":ver}]})
                    sleep(0.5)
                logger.info(f"打印当前值before_foldsts={before_foldsts};after_foldsts={after_foldsts};viewId={id}")
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', after_foldsts) # Unfolded/Folded
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 3, timeout=1)  # 执行调节
                self.set_MirrorAngle_Right(horizon=0, vertical=195) # 调整到目标位置 
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=1)

    @allure.title("设置后视镜目标角度_Right_打断逻辑_等待中调用SetMirrorAngleTarget.viewId=1_进入Unfolded/Folded_无影响")
    @pytest.mark.full
    def test_caseid_1988692(self):
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        for before_foldsts, after_foldsts in {3:1, 4:2}.items():
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', before_foldsts) # Unfolding/Folding
            self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[0]}, 
                                                {"out":[{"id":0,"foldStatus":before_foldsts}]}) 
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                            {"params": [{"viewId":0, "horizontalAngle":0, "verticalAngle":195}]})        
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                            {"params": [{"viewId":1, "horizontalAngle":50, "verticalAngle":55}]})
            sleep(1)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', after_foldsts) # Unfolded/Folded
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 3, timeout=1)    
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [2]}) # stop打断
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)

    @allure.title("设置后视镜目标角度_Right_打断逻辑_执行中调用SetMirrorAngleTarget.viewId=1_无影响")
    @pytest.mark.full
    def test_caseid_1988693(self):
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        for foldsts in [1, 2]:
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', foldsts) # Unfolded/Folded
            self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[0]}, 
                                                  {"out":[{"id":0,"foldStatus":foldsts}]}) 
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                         {"params": [{"viewId":0, "horizontalAngle":55, "verticalAngle":54}]})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5) # 先停止100ms，再调节  
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=1)       
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                            {"params": [{"viewId":1, "horizontalAngle":0, "verticalAngle":195}]})   
            sleep(8)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=1)   
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=3)

    @allure.title("设置后视镜目标角度_Right_打断逻辑_执行中遍历左后视镜的折叠状态_无影响")
    @pytest.mark.smoke
    def test_caseid_1988694(self):
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                         {"params": [{"viewId":0, "horizontalAngle":55, "verticalAngle":54}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=1) 
        for mirr_drvr in range(8):
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', mirr_drvr)  
            sleep(0.5) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=1)
        self.set_MirrorAngle_Right(horizon=55, vertical=54)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=1)

    @allure.title("设置后视镜目标角度_Right_打断逻辑_执行中右后视镜的折叠状态变为Unfolding/Folding_执行被打断")
    @pytest.mark.full
    def test_caseid_1988695(self):
        for foldsts_ing, foldsts_ed in {3:2, 4:1}.items():
            self.set_MirrorAngle_Right(horizon=50, vertical=50)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', random.choice([foldsts_ed, 0])) # 折叠状态满足
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                            {"params": [{"viewId":0, "horizontalAngle":55, "verticalAngle":54}]})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=1) 
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', foldsts_ing)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=1) # 打断

    @allure.title("设置后视镜目标角度_Right_打断逻辑_执行中多次调用SetMirrorAngleTarget.viewId=0/2_执行被打断")
    @pytest.mark.full
    def test_caseid_1988696(self): 
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                        {"params": [{"viewId":0, "horizontalAngle":55, "verticalAngle":54}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=1) 
        for id in [0, 2]:
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                             {"params": [{"viewId":id, "horizontalAngle":50, "verticalAngle":55}]})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5) # 先停止100ms，再调节  
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=1)  

    @allure.title("设置后视镜目标角度_Right_打断逻辑_执行中左后视镜的折叠状态变为NA/Unfolded/Folded_不打断_再次调用")
    @pytest.mark.full
    def test_caseid_1988697(self): 
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 2)
        for foldsts in range(3):
            self.set_MirrorAngle_Right(horizon=50, vertical=50)
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                            {"params": [{"viewId":0, "horizontalAngle":55, "verticalAngle":54}]})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=1)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', foldsts) # NA/Unfolded/Folded
            self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[0]}, 
                                                  {"out":[{"id":0,"foldStatus":foldsts}]}) 
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=1)
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                                {"params": [{"viewId":0, "horizontalAngle":50, "verticalAngle":55}]})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5) # 先停止100ms，再调节  
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=1)       

    @allure.title("设置后视镜目标角度_All_先停止再控制的下行以太网报文校验")
    @pytest.mark.full
    def test_caseid_1988698(self):   
        self.set_MirrorAngle_All(left_vertical=80, left_horizon=80, right_vertical=110, right_horizon=100) 
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)      
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=1) 
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("PassExtrMirrAdjHmiReq", [0, 0, 1])
        self.bgm_eth_inter.ck_signal_values("DrvrExtrMirrAdjHmiReq", [0, 0, 4])        

    @allure.title("设置后视镜目标角度_All_Unfolding/Folding_调用SetMirrorAngleTarget.viewId=2后遍历折叠状态_进入NA/Folded")
    @pytest.mark.smoke
    def test_caseid_1988709(self): 
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 3) # Unfolding
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 4) # Folding 
        self.set_MirrorAngle_All(left_vertical=80, left_horizon=80, right_vertical=110, right_horizon=100, sleeptime=1)       
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})
        for foldSts_pass in range(2, 8): # 遍历右侧后视镜的折叠状态，不包含NA和Unfolded
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', foldSts_pass) 
            sleep(0.3)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        for foldSts_drvr in [1]+list(range(3, 8)): # 遍历左侧后视镜的折叠状态，不包含NA和Folded
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', foldSts_drvr) 
            sleep(0.3)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 0) # NA  右侧开始调节 
        sleep(0.3)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5) # 左侧仍未开始调节
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 2) # Folded 左侧开始调节
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1) 
        self.set_MirrorAngle_Right(horizon=90, vertical=90) # 调整到目标位置 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=1) # 右侧调节完成
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1) # 左侧仍在调节
        self.set_MirrorAngle_Left(horizon=90, vertical=90) # 调整到目标位置 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=1) # 左侧调节完成
        
    @allure.title("设置后视镜目标角度_All_打断逻辑_执行中后视镜的折叠状态变为Unfolding/Folding_再恢复至NA/Unfolded/Folded_恢复后继续调节")
    @pytest.mark.sanity
    def test_caseid_1988710(self):  
        self.set_MirrorAngle_All(left_vertical=80, left_horizon=80, right_vertical=110, right_horizon=100, sleeptime=1)  
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5) # stop 100ms
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=1) # 开始调节
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1) 
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', random.choice([3, 4])) # Unfolding/Folding 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 0) # NA
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=1) # 记忆上次的目标位置，继续调节
        sleep(8)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=1) # 单个方向调节超时，退出  
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=3)

    @allure.title("设置后视镜目标角度_重启场景_接口调用不记忆")
    @pytest.mark.full
    def test_caseid_1988711(self):          
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 3) # Unfolding
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 4) # Folding 
        self.set_MirrorAngle_All(left_vertical=80, left_horizon=80, right_vertical=110, right_horizon=100, sleeptime=1)  
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                              {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]},
                                              {"out":1}) 
        sleep(2)
        self.restart_bgm_and_connect_service(OUTERREARVIEW_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 1) # Unfolded
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 0) # NA
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[2]}, 
                                                      {"out":[{"id":0,"foldStatus":1},
                                                              {"id":1,"foldStatus":0}]}, timeout=3)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=1) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=1)   

    @allure.title("设置后视镜目标角度_重启后未收到总线信号")
    @pytest.mark.full
    def test_caseid_1987185(self): # outer_rearview_service_imp
        self.set_MirrorAngle_Right(horizon=76, vertical=52)
        self.set_MirrorAngle_Left(horizon=76, vertical=52) 
        self.ipdu.pause_bus_send("bodycan")  
        sleep(5)
        self.restart_bgm_and_connect_service(OUTERREARVIEW_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views":[0]}, 
                                              {"out":[{"viewId": 0, "horizontalAngle": 255,"verticalAngle":255}]}, timeout=1) 
        time1=time.time()
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'SetMirrorAngleTarget', 
                                              {"params": [{"viewId":2, "horizontalAngle":100, "verticalAngle":58}]}, 
                                              {"out":1}) # 重启场景 信号没来 直接返回True
        time2=time.time()
        assert time2-time1 < 2
        logger.info(f"打印当前值1")
        sleep(4) # 信号没来拿默认值255，会等待2s，2s后信号还没来，则不执行控制
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        logger.info(f"打印当前值1")
        self.ipdu.resume_bus_send("bodycan") # 恢复后，无影响
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_重启后左右后视镜角度均处于无效范围")
    @pytest.mark.full
    def test_caseid_1987186(self): 
        self.set_MirrorAngle_Right(horizon=8, vertical=192)
        self.set_MirrorAngle_Left(horizon=0, vertical=188) 
        self.restart_bgm_and_connect_service(OUTERREARVIEW_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'SetMirrorAngleTarget', 
                                              {"params": [{"viewId":0, "horizontalAngle":100, "verticalAngle":58}]}, 
                                              {"out":1}, timeout=2.2) # SOA-25481
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'SetMirrorAngleTarget', 
                                              {"params": [{"viewId":1, "horizontalAngle":100, "verticalAngle":58}]}, 
                                              {"out":1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'SetMirrorAngleTarget', 
                                              {"params": [{"viewId":2, "horizontalAngle":100, "verticalAngle":58}]}, 
                                              {"out":1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_重启后左右后视镜角度均处于有效范围_设置的目标角度均超出范围")
    @pytest.mark.full
    def test_caseid_1987187(self): # 设置目标位置的参数角度超出有效范围时，对控制无影响
        self.set_MirrorAngle_Right(horizon=76, vertical=52)
        self.set_MirrorAngle_Left(horizon=76, vertical=52)
        self.restart_bgm_and_connect_service(OUTERREARVIEW_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'SetMirrorAngleTarget', 
                                              {"params": [{"viewId":0, "horizontalAngle":180, "verticalAngle":8}]}, 
                                              {"out":1}, timeout=1)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'SetMirrorAngleTarget', 
                                              {"params": [{"viewId":1, "horizontalAngle":0, "verticalAngle":200}]}, 
                                              {"out":1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 3, timeout=0.5)

    @allure.title("设置后视镜目标角度_All_左后视镜处于无效范围")
    @pytest.mark.full
    def test_caseid_1987188(self): # 左后视镜处于无效范围，仅控制右侧后视镜
        self.set_MirrorAngle_Right(horizon=2, vertical=190)
        self.set_MirrorAngle_Left(horizon=0, vertical=192) 
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'SetMirrorAngleTarget', 
                                              {"params": [{"viewId":2, "horizontalAngle":50, "verticalAngle":55}]}, 
                                              {"out":1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5) # 以前下发1，现在改为不控制

    @allure.title("设置后视镜目标角度_All_右后视镜处于无效范围")
    @pytest.mark.full
    def test_caseid_1987189(self): # 右后视镜处于无效范围，仅控制左侧后视镜
        self.set_MirrorAngle_Left(horizon=2, vertical=190)
        self.set_MirrorAngle_Right(horizon=0, vertical=192) 
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'SetMirrorAngleTarget', 
                                              {"params": [{"viewId":2, "horizontalAngle":50, "verticalAngle":55}]}, 
                                              {"out":1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5) # 以前下发1，现在改为不控制    

    @allure.title("设置后视镜目标角度_Left_水平相同&垂直方向差值>4_调节&超时")
    @pytest.mark.sanity
    def test_caseid_1983221(self): # ExtrMirrAdjHmiReq|SetMirrorAngleTarget|StartAdjustView     outer_rearview_service_imp
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":50, "verticalAngle":55}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4
        sleep(8)   
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=1)  # 未超时
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=3)  # 超时未完成调节     
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":50, "verticalAngle":45}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 1, timeout=0.5) # 当前垂直位置比目标垂直位置大4
        sleep(8)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 1, timeout=1)  # 未超时
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=3)  # 超时未完成调节

    @allure.title("设置后视镜目标角度_Left_水平相同&垂直方向差值>4_时间内调节完成")
    @pytest.mark.full
    def test_caseid_1983222(self): 
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":50, "verticalAngle":55}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4
        sleep(4)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=0.5)
        self.set_MirrorAngle_Left(horizon=50, vertical=59)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Left_垂直相同&水平方向差值>4_调节&超时")
    @pytest.mark.sanity
    def test_caseid_1983223(self): # ExtrMirrAdjHmiReq|SetMirrorAngleTarget|StartAdjustView     outer_rearview_service_imp
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":55, "verticalAngle":50}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4
        sleep(8)   
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=1)  # 未超时
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=3)  # 超时未完成调节       
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":45, "verticalAngle":50}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 3, timeout=0.5) # 当前水平位置比目标水平位置大4
        sleep(8)   
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 3, timeout=1)  # 未超时
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=3)  # 超时未完成调节     
        
    @allure.title("设置后视镜目标角度_Left_垂直相同&水平方向差值>4_时间内调节完成")
    @pytest.mark.full
    def test_caseid_1983224(self): # ExtrMirrAdjHmiReq|SetMirrorAngleTarget|StartAdjustView     outer_rearview_service_imp
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":55, "verticalAngle":54}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4
        sleep(4)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5)
        self.set_MirrorAngle_Left(horizon=56, vertical=50)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Left_垂直&水平方向差值<4")
    @pytest.mark.full
    def test_caseid_1983225(self): # ExtrMirrAdjHmiReq|SetMirrorAngleTarget|StartAdjustView     outer_rearview_service_imp
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":46, "verticalAngle":54}]})
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'SetMirrorAngleTarget', {"params": [{"viewId":1, "horizontalAngle":46, "verticalAngle":54}]}, {"out":1})
        sleep(2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)

    @allure.title("设置后视镜目标角度_Left_垂直&水平方向差值>4_先水平再垂直_均未超时")
    @pytest.mark.sanity
    def test_caseid_1983226(self):       
        targetPos_x, targetPos_y, currentPos_x, currentPos_y=80, 80, 90, 90 
        self.set_MirrorAngle_Left(horizon=currentPos_x, vertical=currentPos_y)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                         {"params": [{"viewId":1, "horizontalAngle":targetPos_x, "verticalAngle":targetPos_y}]})
        # 先水平再垂直 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 3, timeout=0.5) # 当前水平位置比目标水平位置大4 调1发2
        self.set_MirrorAngle_Left(horizon=81, vertical=currentPos_y) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 1, timeout=0.5) # 当前垂直位置比目标垂直位置大4 调2发1
        self.set_MirrorAngle_Left(horizon=81, vertical=84) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Left_垂直&水平方向差值>4_先垂直再水平_均未超时")
    @pytest.mark.sanity
    def test_caseid_1983317(self):       
        targetPos_x, targetPos_y, currentPos_x, currentPos_y=110, 100, 90, 90 
        self.set_MirrorAngle_Left(horizon=currentPos_x, vertical=currentPos_y)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                         {"params": [{"viewId":1, "horizontalAngle":targetPos_x, "verticalAngle":targetPos_y}]})
        # 先垂直再水平 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4 调5发2
        self.set_MirrorAngle_Left(horizon=currentPos_x, vertical=96) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4 调4发4
        self.set_MirrorAngle_Left(horizon=106, vertical=96) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Left_垂直&水平方向差值>4_先垂直再水平_垂直超时")
    @pytest.mark.smoke
    def test_caseid_1983318(self):       
        targetPos_x, targetPos_y, currentPos_x, currentPos_y=110, 100, 90, 90 
        self.set_MirrorAngle_Left(horizon=currentPos_x, vertical=currentPos_y)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                         {"params": [{"viewId":1, "horizontalAngle":targetPos_x, "verticalAngle":targetPos_y}]})
        # 先垂直再水平 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4 调5发2
        sleep(8)
        # self.set_MirrorAngle_Left(horizon=currentPos_x, vertical=96) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=3)
        
    @allure.title("设置后视镜目标角度_Left_垂直&水平方向差值>4_先垂直再水平_水平超时")
    @pytest.mark.smoke
    def test_caseid_1983319(self):       
        targetPos_x, targetPos_y, currentPos_x, currentPos_y=110, 100, 90, 90 
        self.set_MirrorAngle_Left(horizon=currentPos_x, vertical=currentPos_y)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                         {"params": [{"viewId":1, "horizontalAngle":targetPos_x, "verticalAngle":targetPos_y}]})
        # 先垂直再水平 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4 调5发2
        self.set_MirrorAngle_Left(horizon=currentPos_x, vertical=96) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4 调4发4
        sleep(10)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Left_垂直相同&水平方向差值>4_调用StartAdjustViewMirror.id=1打断")
    @pytest.mark.full
    def test_caseid_1983320(self): # 与当前调节的后视镜区域一致，需要先中断当前的后视镜调节，后按照最新的控制指令进行调节
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":55, "verticalAngle":54}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":1,"direction":1}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 3, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Left_垂直相同&水平方向差值>4_调用StartAdjustViewMirror.id=0打断")
    @pytest.mark.full
    def test_caseid_1984092(self): # 与当前调节的后视镜区域不一致，不需要中断控制
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":55, "verticalAngle":54}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":0,"direction":1}]})
        sleep(2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 3, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5)
        sleep(8) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Left_垂直相同&水平方向差值>4_调用StartAdjustViewMirror.id=2打断")
    @pytest.mark.full
    def test_caseid_1984093(self): # 正在设置调节某侧后视镜角度时，若通过调用StartAdjustViewMirror打断，则只会打断同一侧的，不会打断另一个
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":55, "verticalAngle":54}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":2,"direction":2}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Left_水平相同&垂直方向差值>4_调用StopAdjustViewMirror.views=1打断")
    @pytest.mark.full
    def test_caseid_1983321(self): 
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":50, "verticalAngle":55}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [1]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Left_水平相同&垂直方向差值>4_调用StopAdjustViewMirror.views=0打断")
    @pytest.mark.full
    def test_caseid_1984094(self): 
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":50, "verticalAngle":55}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [0]})
        sleep(2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=0.5)
        sleep(8) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Left_水平相同&垂直方向差值>4_调用StopAdjustViewMirror.views=2打断")
    @pytest.mark.full
    def test_caseid_1984095(self): 
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":50, "verticalAngle":55}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [2]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
                
    @allure.title("设置后视镜目标角度_Right_水平相同&垂直方向差值>4_调节&超时")
    @pytest.mark.sanity
    def test_caseid_1983322(self): # ExtrMirrAdjHmiReq|SetMirrorAngleTarget|StartAdjustView     outer_rearview_service_imp
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":50, "verticalAngle":55}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4
        sleep(8)   
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=1)  # 未超时
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=3)  # 超时未完成调节     
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":50, "verticalAngle":45}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5) # 当前垂直位置比目标垂直位置大4
        sleep(8)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=1)  # 未超时
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=3)  # 超时未完成调节

    @allure.title("设置后视镜目标角度_Right_水平相同&垂直方向差值>4_时间内调节完成")
    @pytest.mark.full
    def test_caseid_1984096(self): 
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":50, "verticalAngle":55}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4
        sleep(4)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=0.5)
        self.set_MirrorAngle_Right(horizon=50, vertical=59)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)

    @allure.title("设置后视镜目标角度_Right_垂直相同&水平方向差值>4_调节&超时")
    @pytest.mark.full
    def test_caseid_1984097(self): 
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":55, "verticalAngle":50}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4
        sleep(8)   
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=1)  # 未超时
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=3)  # 超时未完成调节       
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":45, "verticalAngle":50}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 3, timeout=0.5) # 当前水平位置比目标水平位置大4
        sleep(8)   
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 3, timeout=1)  # 未超时
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=3)  # 超时未完成调节     
        
    @allure.title("设置后视镜目标角度_Right_垂直相同&水平方向差值>4_时间内调节完成")
    @pytest.mark.smoke
    def test_caseid_1984098(self): 
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":55, "verticalAngle":54}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4
        sleep(4)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=0.5)
        self.set_MirrorAngle_Right(horizon=56, vertical=50)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Right_垂直&水平方向差值<4")
    @pytest.mark.full
    def test_caseid_1984099(self): 
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":46, "verticalAngle":54}]})
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'SetMirrorAngleTarget', {"params": [{"viewId":0, "horizontalAngle":46, "verticalAngle":54}]}, {"out":1})
        sleep(2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Right_垂直&水平方向差值>4_先水平再垂直_均未超时")
    @pytest.mark.sanity
    def test_caseid_1984100(self): 
        targetPos_x, targetPos_y, currentPos_x, currentPos_y=80, 80, 90, 90 
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.set_MirrorAngle_Right(horizon=currentPos_x, vertical=currentPos_y)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                         {"params": [{"viewId":0, "horizontalAngle":targetPos_x, "verticalAngle":targetPos_y}]})
        # 先水平再垂直 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 3, timeout=0.5) # 当前水平位置比目标水平位置大4 调1发2
        self.set_MirrorAngle_Right(horizon=81, vertical=currentPos_y) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5) # 当前垂直位置比目标垂直位置大4 调2发1
        self.set_MirrorAngle_Right(horizon=81, vertical=84) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Right_垂直&水平方向差值>4_先垂直再水平_均未超时")
    @pytest.mark.sanity
    def test_caseid_1984102(self): 
        targetPos_x, targetPos_y, currentPos_x, currentPos_y=110, 100, 90, 90 
        self.set_MirrorAngle_Right(horizon=currentPos_x, vertical=currentPos_y)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                         {"params": [{"viewId":0, "horizontalAngle":targetPos_x, "verticalAngle":targetPos_y}]})
        # 先垂直再水平 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4 调5发2
        self.set_MirrorAngle_Right(horizon=currentPos_x, vertical=96) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4 调4发4
        self.set_MirrorAngle_Right(horizon=106, vertical=96) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)

    @allure.title("设置后视镜目标角度_Right_垂直&水平方向差值>4_先垂直再水平_垂直超时")
    @pytest.mark.full
    def test_caseid_1984111(self):       
        targetPos_x, targetPos_y, currentPos_x, currentPos_y=110, 100, 90, 90 
        self.set_MirrorAngle_Right(horizon=currentPos_x, vertical=currentPos_y)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                         {"params": [{"viewId":0, "horizontalAngle":targetPos_x, "verticalAngle":targetPos_y}]})
        # 先垂直再水平 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4 调5发2
        sleep(10)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)

    @allure.title("设置后视镜目标角度_Right_垂直&水平方向差值>4_先垂直再水平_水平超时")
    @pytest.mark.full
    def test_caseid_1984112(self):       
        targetPos_x, targetPos_y, currentPos_x, currentPos_y=110, 100, 90, 90 
        self.set_MirrorAngle_Right(horizon=currentPos_x, vertical=currentPos_y)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", 
                                         {"params": [{"viewId":0, "horizontalAngle":targetPos_x, "verticalAngle":targetPos_y}]})
        # 先垂直再水平 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4 调5发2
        self.set_MirrorAngle_Right(horizon=currentPos_x, vertical=96) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4 调4发4
        sleep(10)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Right_垂直相同&水平方向差值>4_调用StartAdjustViewMirror.id=0打断")
    @pytest.mark.full
    def test_caseid_1984113(self): # 正在设置调节某侧后视镜角度时，若通过调用StartAdjustViewMirror打断，则只会打断同一侧的，不会打断另一个
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":55, "verticalAngle":54}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":0,"direction":5}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Right_垂直相同&水平方向差值>4_调用StartAdjustViewMirror.id=1打断")
    @pytest.mark.full
    def test_caseid_1984114(self): # 正在设置调节某侧后视镜角度时，若通过调用StartAdjustViewMirror打断，则只会打断同一侧的，不会打断另一个
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":55, "verticalAngle":54}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":1,"direction":5}]})
        sleep(2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=0.5)
        sleep(8) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)

    @allure.title("设置后视镜目标角度_Right_垂直相同&水平方向差值>4_调用StartAdjustViewMirror.id=2打断")
    @pytest.mark.full
    def test_caseid_1984115(self): # 正在设置调节某侧后视镜角度时，若通过调用StartAdjustViewMirror打断，则只会打断同一侧的，不会打断另一个
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":55, "verticalAngle":54}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":2,"direction":2}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 1, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Right_水平相同&垂直方向差值>4_调用StopAdjustViewMirror.views=1打断")
    @pytest.mark.full
    def test_caseid_1984116(self): 
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":50, "verticalAngle":55}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [1]})
        sleep(2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=0.5)
        sleep(8) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Right_水平相同&垂直方向差值>4_调用StopAdjustViewMirror.views=0打断")
    @pytest.mark.full
    def test_caseid_1984117(self): 
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":50, "verticalAngle":55}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [0]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Right_水平相同&垂直方向差值>4_调用StopAdjustViewMirror.views=2打断")
    @pytest.mark.full
    def test_caseid_1984118(self): 
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":50, "verticalAngle":55}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [2]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
                                                                        
    @allure.title("设置后视镜目标角度_All_垂直&水平方向差值>4_均未超时")
    @pytest.mark.sanity
    def test_caseid_1984144(self):
        self.set_MirrorAngle_All(left_vertical=80, left_horizon=80, right_vertical=110, right_horizon=100, sleeptime=3)       
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5) # 先水平再垂直  目标水平位置比当前水平位置大4
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5) # 先垂直再水平  当前垂直位置比目标垂直位置大4
        self.set_MirrorAngle_All(left_vertical=80, left_horizon=90, right_vertical=90, right_horizon=110, sleeptime=3)              
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=0.5) # 主驾 目标垂直位置比当前垂直位置大4 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 3, timeout=0.5) # 副驾 当前水平位置比目标水平位置大4  
        self.set_MirrorAngle_All(left_vertical=90, left_horizon=90, right_vertical=90, right_horizon=90, sleeptime=3) 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_Right_调用SetMirrorAngleTarget打断")
    @pytest.mark.full
    def test_caseid_1985968(self): # ExtrMirrAdjHmiReq|SetMirrorAngleTarget|StartAdjustView     outer_rearview_service_imp
        self.set_MirrorAngle_Right(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":50, "verticalAngle":55}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=0.5) # 目标垂直位置比当前垂直位置大4
        sleep(2)     
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":50, "verticalAngle":45}]})
        sleep(8)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":50, "verticalAngle":45}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=1)  # 未超时
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=3)  # 超时未完成调节
        
    @allure.title("设置后视镜目标角度_Left_调用SetMirrorAngleTarget打断")
    @pytest.mark.full
    def test_caseid_1985969(self): # ExtrMirrAdjHmiReq|SetMirrorAngleTarget|StartAdjustView     outer_rearview_service_imp
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":55, "verticalAngle":54}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5) # 目标水平位置比当前水平位置大4
        sleep(2)     
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":45, "verticalAngle":50}]})
        sleep(8)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":50, "verticalAngle":45}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 3, timeout=1) # 当前水平位置比目标水平位置大4
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=3)  # 超时未完成调节
        
    @allure.title("设置后视镜目标角度_All_调用SetMirrorAngleTarget.id=1打断")
    @pytest.mark.smoke
    def test_caseid_1985970(self):
        self.set_MirrorAngle_All(left_vertical=80, left_horizon=80, right_vertical=110, right_horizon=100, sleeptime=3)       
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5) # 先水平再垂直  目标水平位置比当前水平位置大4
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5) # 先垂直再水平  当前垂直位置比目标垂直位置大4
        sleep(2)  
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":90, "verticalAngle":90}]})
        sleep(2)  
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5) # 第一次调用的10s计时器还未超时
        sleep(6.1)      
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5) # 第二次调用后 打断id=1的调节，重新开始10s计时
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5) # 第二次调用后 未打断id=0的调节，导致第一次调用的10s计时器已经超时
        sleep(2)  
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_All_调用SetMirrorAngleTarget.id=0打断")
    @pytest.mark.full
    def test_caseid_1985971(self):
        self.set_MirrorAngle_All(left_vertical=80, left_horizon=80, right_vertical=110, right_horizon=100, sleeptime=3)       
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5) # 先水平再垂直  目标水平位置比当前水平位置大4
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5) # 先垂直再水平  当前垂直位置比目标垂直位置大4
        sleep(2)  
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":0, "horizontalAngle":90, "verticalAngle":90}]})
        sleep(2)  
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5) # 第一次调用的10s计时器还未超时
        sleep(6.1)      
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
        sleep(2)  
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_All_垂直&水平方向差值>4_调节超时")
    @pytest.mark.full
    def test_caseid_1984147(self):
        self.set_MirrorAngle_All(left_vertical=110, left_horizon=100, right_vertical=80, right_horizon=80, sleeptime=3)       
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})
        sleep(8)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 1, timeout=0.5) # 先水平再垂直 目标垂直位置比当前垂直位置大4 
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=0.5) # 先垂直再水平 当前水平位置比目标水平位置大4  
        sleep(2)    
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_All_垂直&水平方向差值>4_调用StartAdjustViewMirror.id=0打断")
    @pytest.mark.full
    def test_caseid_1984148(self):
        self.set_MirrorAngle_All(left_vertical=80, left_horizon=80, right_vertical=110, right_horizon=100, sleeptime=3)       
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})           
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":0,"direction":5}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 2, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_All_垂直&水平方向差值>4_调用StartAdjustViewMirror.id=1打断")
    @pytest.mark.full
    def test_caseid_1984149(self):
        self.set_MirrorAngle_All(left_vertical=80, left_horizon=80, right_vertical=110, right_horizon=100, sleeptime=3)       
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})           
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":1,"direction":5}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 2, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_All_垂直&水平方向差值>4_调用StartAdjustViewMirror.id=2打断")
    @pytest.mark.full
    def test_caseid_1984150(self):
        self.set_MirrorAngle_All(left_vertical=80, left_horizon=80, right_vertical=110, right_horizon=100, sleeptime=3)       
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})           
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":2,"direction":3}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_All_垂直&水平方向差值>4_调用StopAdjustViewMirror.views=0打断")
    @pytest.mark.full
    def test_caseid_1984151(self):
        self.set_MirrorAngle_All(left_vertical=80, left_horizon=80, right_vertical=110, right_horizon=100, sleeptime=3)       
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})           
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [0]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_All_垂直&水平方向差值>4_调用StopAdjustViewMirror.views=1打断")
    @pytest.mark.full
    def test_caseid_1984152(self):
        self.set_MirrorAngle_All(left_vertical=80, left_horizon=80, right_vertical=110, right_horizon=100, sleeptime=3)       
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})           
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [1]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("设置后视镜目标角度_All_垂直&水平方向差值>4_调用StopAdjustViewMirror.views=2打断")
    @pytest.mark.full
    def test_caseid_1984153(self):
        self.set_MirrorAngle_All(left_vertical=80, left_horizon=80, right_vertical=110, right_horizon=100, sleeptime=3)       
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})           
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [2]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        
    @allure.title("调节后视镜_下行PDU校验&取值参数遍历")
    @pytest.mark.sanity
    def test_caseid_1985949(self): 
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        dict={1:3, 0:3, 2:1, 3:1, 4:4, 5:2} # 0和3 不下行以太网
        for id in range(3):
            for key, value in dict.items():                      
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":id,"direction":key}]})
                sleep(1)
                if id == 0:
                    self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', value, timeout=0.5)
                elif id == 1:
                    self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', value, timeout=0.5)
                else:
                    self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', value, timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', value, timeout=0.5)
                sleep(2)
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":id,"direction":0}]})
            sleep(1) 
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":id,"direction":3}]})
            sleep(1)    
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("PassExtrMirrAdjHmiReq", [3, 1, 4, 2, 3, 1, 4, 2])
        self.bgm_eth_inter.ck_signal_values("DrvrExtrMirrAdjHmiReq", [3, 1, 4, 2, 3, 1, 4, 2])
        
    @allure.title("调节后视镜_UsgMod遍历")
    @pytest.mark.smoke
    def test_caseid_1985950(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        dict={0:1, 1:4, 2:4} 
        for UsgMod in [2, 11, 13, 0, 1]:
            self.sd_tester.change_usage_mode(UsgMod)
            sleep(0.5)
            for key, value in dict.items():                      
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":key,"direction":value}]})
                sleep(2)
                if UsgMod in [0, 1]:
                    self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 4, timeout=0.5)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("PassExtrMirrAdjHmiReq", [3, 4, 3, 4, 3, 4])
        self.bgm_eth_inter.ck_signal_values("DrvrExtrMirrAdjHmiReq", [4, 4, 4, 4, 4, 4])        
        
    @allure.title("停止调节后视镜_下行PDU校验&取值参数遍历")
    @pytest.mark.sanity
    def test_caseid_1985951(self):  
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        for id in range(3):
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":2,"direction":2}]})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 1, timeout=0.5)
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [id]})
            if id == 0:
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 1, timeout=0.5)
            elif id == 1:
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 1, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
            else:
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        sleep(1)            
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("PassExtrMirrAdjHmiReq", [1, 0, 1, 1, 0])
        self.bgm_eth_inter.ck_signal_values("DrvrExtrMirrAdjHmiReq", [1, 1, 0, 1, 0])        
        
    @allure.title("停止调节后视镜_UsgMod遍历")
    @pytest.mark.smoke
    def test_caseid_1985953(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        for UsgMod in [2, 11, 13, 0, 1]:
            self.sd_tester.change_usage_mode(UsgMod)    
            sleep(0.5)     
            for id in range(3):           
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StartAdjustViewMirror", {"params": [{"id":2,"direction":5}]})
                sleep(1)
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [id]})
                sleep(1)
                if UsgMod in [0, 1]:
                    self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("PassExtrMirrAdjHmiReq", [2, 0, 2, 2, 0, 
                                                                      2, 0, 2, 2, 0, 
                                                                      2, 0, 2, 2, 0])
        self.bgm_eth_inter.ck_signal_values("DrvrExtrMirrAdjHmiReq", [2, 2, 0, 2, 0, 
                                                                      2, 2, 0, 2, 0, 
                                                                      2, 2, 0, 2, 0])     
        
    @allure.title("设置后视镜目标角度_返回值校验")
    @pytest.mark.full
    def test_caseid_1985956(self):
        for UsgMod in [2, 11, 13, 0, 1]:
            self.sd_tester.change_usage_mode(UsgMod)  
            sleep(0.5)   
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":1, "horizontalAngle":46, "verticalAngle":54}]})  
            value = 1 if UsgMod in [2, 11, 13] else 0
            self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'SetMirrorAngleTarget', 
                                                  {"params": [{"viewId":1, "horizontalAngle":46, "verticalAngle":54}]}, 
                                                  {"out":value})
            
    @allure.title("设置后视镜目标角度_UsgMod=0/1_不执行调节")
    @pytest.mark.full
    def test_caseid_1985959(self):
        self.set_MirrorAngle_All(left_vertical=110, left_horizon=100, right_vertical=80, right_horizon=80, sleeptime=3)      
        for UsgMod in [0, 1]:
            self.sd_tester.change_usage_mode(UsgMod) 
            sleep(1)    
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})
            sleep(1)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
            # self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 1) # 不按照此值下发
            # self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4)
            
    @allure.title("设置后视镜目标角度_UsgMod=2/11/13_执行调节")
    @pytest.mark.full
    def test_caseid_1985960(self):
        self.set_MirrorAngle_All(left_vertical=110, left_horizon=100, right_vertical=80, right_horizon=80, sleeptime=3)  
        for UsgMod in [2, 11, 13]:
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "StopAdjustViewMirror", {"views": [2]})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 0, timeout=0.5)
            self.sd_tester.change_usage_mode(UsgMod) 
            sleep(1)     
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {"params": [{"viewId":2, "horizontalAngle":90, "verticalAngle":90}]})
            sleep(1)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'DrvrExtrMirrAdjHmiReq', 1, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13,'PassExtrMirrAdjHmiReq', 4, timeout=0.5)

    @allure.title('展开后视镜_Unfold.isAutoUnFold=False_周期报文校验')
    @pytest.mark.sanity
    def test_caseid_1981104(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 4)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 4)  
        sleep(2)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Unfold', {"views":[2], "isAutoUnFold": False}, {"out":0}) 
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('ExtrMirrFoldHmiReq', [1, 1, 1, 0])
        self.bgm_eth_inter.ck_period_time('ExtrMirrFoldHmiReq', 0.08, deviation=0.5)

    @allure.title('展开后视镜_Unfold.isAutoUnFold=False_重启后未收到总线信号')
    @pytest.mark.full
    def test_caseid_1987200(self):
        # 满足前置
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 2)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 4)  
        sleep(1)
        self.ipdu.pause_bus_send("bodycan")  
        sleep(2)
        self.restart_bgm_and_connect_service(OUTERREARVIEW_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        sleep(2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Unfold', {"views":[2], "isAutoUnFold": False}, {"out":1}) 
        self.ipdu.resume_bus_send("bodycan")
        sleep(2.5)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Unfold', {"views":[2], "isAutoUnFold": False}, {"out":0}) 
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('ExtrMirrFoldHmiReq', [1, 1, 1, 0])
        # self.bgm_eth_inter.ck_period_time('ExtrMirrFoldHmiReq', 0.08, deviation=0.5) # 启动后抓包偏差过大

    @allure.title('折叠后视镜_fold.isAutoUnFold=False_重启后未收到总线信号')
    @pytest.mark.full
    def test_caseid_1987201(self):
        # 满足前置
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 2)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 3)  
        sleep(1)
        self.ipdu.pause_bus_send("bodycan")  
        sleep(2)
        self.restart_bgm_and_connect_service(OUTERREARVIEW_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        sleep(2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Fold', {"views":[2], "isAutoUnFold": False}, {"out":1})
        sleep(1)
        self.ipdu.resume_bus_send("bodycan")
        sleep(2.5)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Fold', {"views":[2], "isAutoUnFold": False}, {"out":0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('ExtrMirrFoldHmiReq', [1, 1, 1, 0])
        self.bgm_eth_inter.ck_period_time('ExtrMirrFoldHmiReq', 0.08, deviation=0.5)
        
    @allure.title('展开后视镜_Unfold.isAutoUnFold=False_后视镜状态遍历')
    @pytest.mark.sanity
    @pytest.mark.failed
    def test_caseid_1981105(self):
        sts={4:[1, 2, 4], 2:[2, 4], 1:[4]}
        for left in range(5):
            for right in range(5):                
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', left)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', right)  
                sleep(2)
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, 'Unfold', {"views":[2], "isAutoUnFold": False})
                if left in [1, 2, 4] :
                    if right in sts[left]:                                          
                        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'ExtrMirrFoldHmiReq', 1, timeout=0.5) # check次数为3次，在5s内完成
                        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'ExtrMirrFoldHmiReq', 0, timeout=0.5)
                        sleep(3)
        
    @allure.title('展开后视镜_Unfold.isAutoUnFold=False_打断')
    @pytest.mark.full
    def test_caseid_1981107(self):
        file_path, save_name = self.bgmcli.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 4)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 4)  
        sleep(2)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Unfold', {"views":[2], "isAutoUnFold": False}, {"out":0}) 
        sleep(0.1)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Unfold', {"views":[2], "isAutoUnFold": False}, {"out":1})  
        sleep(3)
        data_list = [(5152, 1, 0, 1)]
        res_dict = self.stop_tcpdump_and_copy_and_calculate(save_name, data_list)
        assert res_dict[data_list[0]][0][1]==1
        assert res_dict[data_list[0]][1][1]==1
        assert res_dict[data_list[0]][2][1]==1
        assert res_dict[data_list[0]][3][1]==0
        
    @allure.title('展开后视镜_Unfold.isAutoUnFold=True_周期报文校验')
    @pytest.mark.sanity
    def test_caseid_1981108(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Unfold', {"views":[2], "isAutoUnFold": True}, {"out":0}) 
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'MirrOpenClsReq', 2, check_time=3) # check次数为3次，在5s内完成
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'MirrOpenClsReq', 0)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('MirrOpenClsReq', [2, 2, 2, 0])
        self.bgm_eth_inter.ck_period_time('MirrOpenClsReq', 0.08, deviation=0.5)
        # data_list = [(30009, 1, 1, 2)]
        # res_dict = self.stop_tcpdump_and_copy_and_calculate(save_name, data_list)
        # ck_pdu_period_time(res_dict, 30009, 0.08, deviation=0.5)  
        
    @allure.title('展开后视镜_Unfold.isAutoUnFold=True_打断')
    @pytest.mark.full
    def test_caseid_1981110(self):
        file_path, save_name = self.bgmcli.start_bgm_tcpdump()
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Unfold', {"views":[2], "isAutoUnFold": True}, {"out":0}) 
        sleep(0.1)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Unfold', {"views":[2], "isAutoUnFold": True}, {"out":1})  
        sleep(3)
        data_list = [(30009, 1, 1, 2)]
        res_dict = self.stop_tcpdump_and_copy_and_calculate(save_name, data_list)
        assert res_dict[data_list[0]][0][1]==2
        assert res_dict[data_list[0]][1][1]==2
        assert res_dict[data_list[0]][2][1]==2
        assert res_dict[data_list[0]][3][1]==0 
        
    @allure.title('折叠后视镜_fold.isAutoUnFold=True_周期报文校验')
    @pytest.mark.sanity
    def test_caseid_1913296(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Fold', {"views":[2], "isAutoUnFold": True}, {"out":0}) 
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'MirrOpenClsReq', 1, check_time=3) # check次数为3次，在5s内完成
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'MirrOpenClsReq', 0)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('MirrOpenClsReq', [1, 1, 1, 0])
        self.bgm_eth_inter.ck_period_time('MirrOpenClsReq', 0.08, deviation=0.5)
        
        
    @allure.title('折叠后视镜_fold.isAutoUnFold=True_打断')
    @pytest.mark.full
    def test_caseid_102940(self):
        file_path, save_name = self.bgmcli.start_bgm_tcpdump()
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Fold', {"views":[2], "isAutoUnFold": True}, {"out":0}) 
        sleep(0.1)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Fold', {"views":[2], "isAutoUnFold": True}, {"out":1})  
        sleep(3)
        data_list = [(30009, 1, 1, 2)]
        res_dict = self.stop_tcpdump_and_copy_and_calculate(save_name, data_list)
        assert res_dict[data_list[0]][0][1]==1
        assert res_dict[data_list[0]][1][1]==1
        assert res_dict[data_list[0]][2][1]==1
        assert res_dict[data_list[0]][3][1]==0 
        
    @allure.title('折叠后视镜_fold.isAutoUnFold=False_周期报文校验')
    @pytest.mark.sanity
    def test_caseid_1913293(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 3)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 3)  
        sleep(2)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Fold', {"views":[2], "isAutoUnFold": False}, {"out":0}) 
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('ExtrMirrFoldHmiReq', [1, 1, 1, 0])
        self.bgm_eth_inter.ck_period_time('ExtrMirrFoldHmiReq', 0.08, deviation=0.5)
        
    @allure.title('折叠后视镜_fold.isAutoUnFold=False_后视镜状态遍历')
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1913294(self):
        file_path, save_name = self.bgmcli.start_bgm_tcpdump()
        sts={1:[1, 3], 2:[3], 3:[2, 3, 1]}
        for left in range(5):
            for right in range(5):                
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', left)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', right)  
                sleep(2)
                self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, 'Fold', {"views":[2], "isAutoUnFold": False})
                if left in [1, 2, 3] :
                    if right in sts[left]:                                          
                        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'ExtrMirrFoldHmiReq', 1, timeout=0.5) # check次数为3次，在5s内完成
                        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'ExtrMirrFoldHmiReq', 0, timeout=0.5)
                        sleep(3)
        data_list = [(5152, 1, 0, 1)]
        res_dict = self.stop_tcpdump_and_copy_and_calculate(save_name, data_list)
        
    @allure.title('折叠后视镜_fold.isAutoUnFold=False_打断')
    @pytest.mark.full
    def test_caseid_1913295(self):
        file_path, save_name = self.bgmcli.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 3)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 3)  
        sleep(2)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Fold', {"views":[2], "isAutoUnFold": False}, {"out":0}) 
        sleep(0.1)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'Fold', {"views":[2], "isAutoUnFold": False}, {"out":1})  
        sleep(3)
        data_list = [(5152, 1, 0, 1)]
        res_dict = self.stop_tcpdump_and_copy_and_calculate(save_name, data_list)
        assert res_dict[data_list[0]][0][1]==1
        assert res_dict[data_list[0]][1][1]==1
        assert res_dict[data_list[0]][2][1]==1
        assert res_dict[data_list[0]][3][1]==0
        
    @allure.title('设置后视镜自动折叠_SetAutoFoldUnfold.isOn=False')
    @pytest.mark.sanity
    def test_caseid_1981116(self): 
        file_path, save_name = self.bgmcli.start_bgm_tcpdump() 
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, 'SetAutoFoldUnfold', {"params":[{"id":2,"isOn":False}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'ExtrMirrFoldSetgIdPen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'ExtrMirrFoldSetgMirrPass', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'ExtrMirrFoldSetgMirrDrvr', 1, timeout=0.5)
        sleep(3)
        data_list = [(5154, 3, 3, 4), (5154, 3, 16, 1), (5154, 3, 8, 1)]
        res_dict = self.stop_tcpdump_and_copy_and_calculate(save_name, data_list)
        # ck_pdu_period_time(res_dict, 5154, 0.5, deviation=0.3) 
        for key in data_list:
            assert len(res_dict[key]) > 1
        
    @allure.title('设置后视镜自动折叠_SetAutoFoldUnfold.isOn=True')
    @pytest.mark.sanity
    def test_caseid_1981117(self):        
        file_path, save_name = self.bgmcli.start_bgm_tcpdump() 
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, 'SetAutoFoldUnfold', {"params":[{"id":2,"isOn":True}]})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'ExtrMirrFoldSetgIdPen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'ExtrMirrFoldSetgMirrPass', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'ExtrMirrFoldSetgMirrDrvr', 0, timeout=0.5)
        sleep(3)
        data_list = [(5154, 3, 3, 4), (5154, 3, 16, 1), (5154, 3, 8, 1)]
        res_dict = self.stop_tcpdump_and_copy_and_calculate(save_name, data_list)
        # ck_pdu_period_time(res_dict, 5154, 0.5, deviation=0.3) 
        for key in data_list:
            assert len(res_dict[key]) > 1     
            
    @allure.title('获取&通知后视镜自动折叠状态_取值遍历')
    @pytest.mark.sanity
    def test_caseid_1981119(self):    
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, 'SetAutoFoldUnfold', {"params":[{"id":2,"isOn":False}]})
        for isOn in [True, False]:
            self.partner.empty_all(2)
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, 'SetAutoFoldUnfold', {"params":[{"id":2,"isOn":isOn}]})   
            self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'AutoFoldUnfoldStatus', {"id":2,"isOn":isOn})           
            self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetAutoFoldUnfold', {"views":[2]}, {"out":[{"id":2,"isOn":isOn}]})    
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, 'SetAutoFoldUnfold', {"params":[{"id":2,"isOn":False}]})
        self.partner.ck_no_event(OUTERREARVIEW_SERVICE_CLIENT, 'AutoFoldUnfoldStatus', timeout=3)           
            
    @allure.title('设置后视镜加热状态_isOn=True/False')
    @pytest.mark.sanity
    def test_caseid_1981476(self):    
        file_path, save_name = self.bgmcli.start_bgm_tcpdump() 
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        sleep(3)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        sleep(3)
        data_list = [(5018, 3, 1, 2), (5018, 3, 9, 2), (5018, 3, 17, 2)]
        res_dict = self.stop_tcpdump_and_copy_and_calculate(save_name, data_list)
        assert res_dict[data_list[0]][0][1]==0
        assert res_dict[data_list[1]][0][1]==1
        assert res_dict[data_list[2]][0][1]==1
        for key in data_list:
            assert res_dict[key][1][1]==0
        
    @allure.title('获取&通知后视镜下翻状态_Left')
    @pytest.mark.smoke
    def test_caseid_103005(self):   
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "MirrDwnStsAtDrvr", 3)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewTiltStatus', {"views":[1]}, {"out":[{"id":1,"tiltStatus":3}]}, timeout=3)
        self.partner.empty_all()
        for left in range(8):            
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "MirrDwnStsAtDrvr", left)
            value=left if left<5 else 4
            if left<5:
                self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewTiltStatus', {"id":1, "status":value})
            else:
                self.partner.ck_no_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewTiltStatus')
            self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewTiltStatus', {"views":[1]}, {"out":[{"id":1,"tiltStatus":value}]})  
        
    @allure.title('获取&通知后视镜下翻状态_Right')
    @pytest.mark.sanity
    def test_caseid_1981315(self): # can MirrDwnStsAt|ViewTiltStatus
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "MirrDwnStsAtPass", 3)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewTiltStatus', {"views":[0]}, {"out":[{"id":0,"tiltStatus":3}]}, timeout=3)
        self.partner.empty_all()
        for right in range(8):     
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "MirrDwnStsAtPass", right)
            value=right if right<5 else 4
            if right<5:
                self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewTiltStatus', {"id":0, "status":value})
            else:
                self.partner.ck_no_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewTiltStatus')
            self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewTiltStatus', {"views":[0]}, {"out":[{"id":0,"tiltStatus":value}]})  
            
    @allure.title('获取&通知后视镜下翻状态_All')
    @pytest.mark.sanity
    def test_caseid_1981317(self): 
        for left in [1, 3]:
            for right in [0, 2, 4]:
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "MirrDwnStsAtPass", right)
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "MirrDwnStsAtDrvr", left)
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewTiltStatus', {"views":[2]}, 
                                                      {"out":[{"id":0,"tiltStatus":right}, {"id":1,"tiltStatus":left}]}, timeout=3)
        
    @allure.title('获取&通知后视镜下翻状态_信号丢失')
    @pytest.mark.full
    def test_caseid_103018(self):   
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "MirrDwnStsAtPass", 2)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "MirrDwnStsAtDrvr", 2)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewTiltStatus', {"views":[2]}, 
                                              {"out":[{"id":0,"tiltStatus":2}, {"id":1,"tiltStatus":2}]}, timeout=3)
        self.partner.empty_all()
        self.ipdu.pause_bus_send("bodycan")  
        sleep(2)
        self.partner.ck_no_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewTiltStatus')
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewTiltStatus', {"views":[2]}, 
                                              {"out":[{"id":0,"tiltStatus":2}, {"id":1,"tiltStatus":2}]})
        self.ipdu.resume_bus_send("bodycan")  
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewTiltStatus', {"views":[2]}, 
                                              {"out":[{"id":0,"tiltStatus":2}, {"id":1,"tiltStatus":2}]})
        
    def ck_ViewFault_and_GetViewFault(self, faultId=0, faultMsg="", viewId=2):
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewFault', {"faults":[{"faultId":faultId,"faultMsg":faultMsg,"viewId":viewId}]})
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFault', {}, {"out":[{"faultId":faultId,"faultMsg":faultMsg,"viewId":viewId}]})  
        
    @allure.title('获取&通知后视镜故障_折叠展开故障&调节故障遍历_Left') 
    @pytest.mark.sanity
    def test_caseid_103003(self):  
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "DrvrMirrorAdjErrorFb", 0)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "DrvrMirrorFoldErrorFb", 0)
        self.partner.empty_all(2)
        for fold in [1, 0]:
            for adj in [1, 0]:                
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "DrvrMirrorAdjErrorFb", adj)
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "DrvrMirrorFoldErrorFb", fold)
                if fold ==0 and adj ==0:
                    self.ck_ViewFault_and_GetViewFault()
                elif fold==1 and adj ==1:
                    self.ck_ViewFault_and_GetViewFault(faultId=2, viewId=1)
                    self.ck_ViewFault_and_GetViewFault(faultId=1, viewId=1)
                elif fold==1 and adj ==0:
                    self.ck_ViewFault_and_GetViewFault(faultId=1, viewId=1)
                elif fold==0 and adj ==1:
                    self.ck_ViewFault_and_GetViewFault(faultId=2, viewId=1)
                
    @allure.title('获取&通知后视镜故障_折叠展开故障&调节故障遍历_Right') 
    @pytest.mark.sanity
    def test_caseid_1981359(self):  
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "PassMirrorFoldErrorFb", 0)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "PassMirrorAdjErrorFb", 0)
        self.partner.empty_all(2)
        for fold in [1, 0]:
            for adj in [1, 0]:                
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "PassMirrorAdjErrorFb", adj)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "PassMirrorFoldErrorFb", fold)
                if fold ==0 and adj ==0:
                    self.ck_ViewFault_and_GetViewFault()
                elif fold==1 and adj ==1:
                    self.ck_ViewFault_and_GetViewFault(faultId=2, viewId=0)
                    self.ck_ViewFault_and_GetViewFault(faultId=1, viewId=0)
                elif fold==1 and adj ==0:
                    self.ck_ViewFault_and_GetViewFault(faultId=1, viewId=0)
                elif fold==0 and adj ==1:
                    self.ck_ViewFault_and_GetViewFault(faultId=2, viewId=0)        
                    
    @allure.title('获取&通知后视镜故障_信号丢失Left') 
    @pytest.mark.full
    def test_caseid_1981360(self):  
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "DrvrMirrorAdjErrorFb", 1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "DrvrMirrorFoldErrorFb", 1)       
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFault', {}, 
                                              {"out":[{'faultId': 2, 'faultMsg': '', 'viewId': 1}, {'faultId': 1, 'faultMsg': '', 'viewId': 1}]}, timeout=3)  
        self.partner.empty_all()
        self.ipdu.pause_bus_send("bodycan")  
        sleep(2)
        self.partner.ck_no_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewFault')
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFault', {}, 
                                              {"out":[{'faultId': 2, 'faultMsg': '', 'viewId': 1}, {'faultId': 1, 'faultMsg': '', 'viewId': 1}]})  
        self.ipdu.resume_bus_send("bodycan")  
        self.partner.ck_no_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewFault')
                        
    @allure.title('获取&通知后视镜故障_信号丢失Right') 
    @pytest.mark.full
    def test_caseid_1981361(self):  
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "PassMirrorFoldErrorFb", 1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "PassMirrorAdjErrorFb", 1) 
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFault', {}, 
                                              {"out":[{'faultId': 2, 'faultMsg': '', 'viewId': 0}, {'faultId': 1, 'faultMsg': '', 'viewId': 0}]}, timeout=3)  
        self.partner.empty_all()
        self.ipdu.pause_bus_send("bodycan")  
        sleep(2)
        self.partner.ck_no_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewFault')
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFault', {}, 
                                              {"out":[{'faultId': 2, 'faultMsg': '', 'viewId': 0}, {'faultId': 1, 'faultMsg': '', 'viewId': 0}]})  
        self.ipdu.resume_bus_send("bodycan")  
        self.partner.ck_no_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewFault')       

    @allure.title("获取&通知外后视镜折叠状态_包含左和右外后视镜折叠状态")
    @pytest.mark.sanity
    def test_caseid_1983466(self): # can MirrFoldStsAt|OuterRearViewFoldStatus
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 1)   
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[2]}, 
                                                      {"out":[{"id":0,"foldStatus":1},{"id":1,"foldStatus":1}]}, timeout=2) 
        last_mirrDrvr, last_mirrPass=1, 1        
        for mirr_drvr in range(8):
            for mirr_pass in range(8):
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', mirr_drvr)
                self.partner.empty_all(1)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', mirr_pass)   
                mirrDrvr=4 if mirr_drvr>4 else mirr_drvr
                mirrPass=4 if mirr_pass>4 else mirr_pass
                logger.info(f"打印当前返回值: last_mirrDrvr={last_mirrDrvr}, last_mirrPass={last_mirrPass}, mirrDrvr={mirrDrvr}, mirrPass={mirrPass}")
                if mirrDrvr!=last_mirrDrvr or mirrPass!=last_mirrPass:
                    self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewFoldStatus',
                                              {"status":[{"id":1,"value":mirrDrvr,"validity":0}, {"id":0,"value":mirrPass,"validity":0}]})
                else:
                    self.partner.ck_no_event(OUTERREARVIEW_SERVICE_CLIENT, "OuterRearViewFoldStatus")
                # 获取外后视镜折叠状态（不带功能安全需求参数）
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[1]}, 
                                                      {"out":[{"id":1,"foldStatus":mirrDrvr}]}) 
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[0]}, 
                                                      {"out":[{"id":0,"foldStatus":mirrPass}]}) 
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[2]}, 
                                                      {"out":[{"id":0,"foldStatus":mirrPass},
                                                              {"id":1,"foldStatus":mirrDrvr}]}) 
                # 获取外后视镜折叠状态（带功能安全需求参数）
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatusValidity', {"views":[1]},  
                                                      {"out":[{"value": {"id":1, "foldStatus":mirrDrvr}, "foldStatusValidity": 0}]})
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatusValidity', {"views":[0]},  
                                                      {"out":[{"value": {"id":0, "foldStatus":mirrPass}, "foldStatusValidity": 0}]})
                self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatusValidity', {"views":[2]},  
                                                      {"out":[{"value": {"id":0, "foldStatus":mirrPass}, "foldStatusValidity": 0}, 
                                                              {"value": {"id":1, "foldStatus":mirrDrvr}, "foldStatusValidity": 0}]})                 
                last_mirrDrvr, last_mirrPass=mirrDrvr, mirrPass
       
    @allure.title("获取&通知外后视镜折叠状态_包含左和右外后视镜折叠状态_信号丢失")
    @pytest.mark.full
    def test_caseid_1983467(self):  # can MirrFoldStsAt|MirrFoldStsAtDrvr_TimeOut|OuterRearViewFoldStatus 
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 2)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 2)   
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatusValidity', {"views":[2]}, 
                                              {"out":[{"value": {"id":0, "foldStatus":2}, "foldStatusValidity": 0},
                                                      {"value": {"id":1, "foldStatus":2}, "foldStatusValidity": 0}]}, timeout=3)                    
        self.partner.empty_all()  
        self.ipdu.stop_send_pdu('bodycan', 0x030) # MirrFoldStsAtDrvr            
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewFoldStatus', 
                                  {"status":[{"id":1,"value":2,"validity":4}, {"id":0,"value":2,"validity":0}]}, timeout=2.5)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatusValidity', {"views":[2]}, 
                                              {"out":[{"value": {"id":0, "foldStatus":2}, "foldStatusValidity": 0}, 
                                                      {"value": {"id":1, "foldStatus":2}, "foldStatusValidity": 4}]})  
        self.ipdu.stop_send_pdu('bodycan', 0x010) # MirrFoldStsAtPass
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewFoldStatus', 
                                  {"status":[{"id":1,"value":2,"validity":4}, {"id":0,"value":2,"validity":4}]}, timeout=2.5)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatusValidity', {"views":[2]}, 
                                              {"out":[{"value": {"id":0, "foldStatus":2}, "foldStatusValidity": 4}, 
                                                      {"value": {"id":1, "foldStatus":2}, "foldStatusValidity": 4}]})  
        self.ipdu.resume_bus_send("bodycan") 
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewFoldStatus', 
                                  {"status":[{"id":1,"value":2,"validity":0}, {"id":0,"value":2,"validity":0}]})
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatusValidity', {"views":[2]}, 
                                              {"out":[{"value": {"id":0, "foldStatus":2}, "foldStatusValidity": 0}, 
                                                      {"value": {"id":1, "foldStatus":2}, "foldStatusValidity": 0}]})  

    @allure.title("获取&通知外后视镜角度_包含左和右外后视镜角度")
    @pytest.mark.sanity
    def test_caseid_1983477(self):
        self.set_MirrorAngle_Left(horizon=100, vertical=100)
        self.set_MirrorAngle_Right(horizon=20, vertical=20)    
        self.partner.empty_all()    
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "MirrPosnToCldAtDrvrMirrPosnAdjCldUpDwn", 102) # 主驾垂直
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewMirrorAngle', 
                                  {"info":[{"viewId":1,"horizontalAngle":100,"verticalAngle":102},
                                           {"viewId":0,"horizontalAngle":20,"verticalAngle":20}]})
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views":[0]}, 
                                              {"out":[{"viewId": 0, "horizontalAngle": 20,"verticalAngle":20}]})
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views":[1]}, 
                                              {"out":[{"viewId": 1, "horizontalAngle": 100,"verticalAngle":102}]})
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views":[2]}, 
                                              {"out":[{"viewId": 1, "horizontalAngle": 100,"verticalAngle":102},
                                                      {"viewId": 0, "horizontalAngle": 20,"verticalAngle":20}]})        
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "MirrPosnToCldAtDrvrMirrPosnAdjCldLeRi", 98) # 主驾水平
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewMirrorAngle', 
                                  {"info":[{"viewId":1,"horizontalAngle":98,"verticalAngle":102},
                                           {"viewId":0,"horizontalAngle":20,"verticalAngle":20}]})
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "MirrPosnToCldAtPassMirrPosnAdjCldUpDwn", 18) # 副驾垂直
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewMirrorAngle', 
                                  {"info":[{"viewId":1,"horizontalAngle":98,"verticalAngle":102},
                                           {"viewId":0,"horizontalAngle":20,"verticalAngle":18}]})        
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "MirrPosnToCldAtPassMirrPosnAdjCldLeRi", 22) # 副驾水平
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewMirrorAngle', 
                                  {"info":[{"viewId":1,"horizontalAngle":98,"verticalAngle":102},
                                           {"viewId":0,"horizontalAngle":22,"verticalAngle":18}]})
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views":[0]}, 
                                              {"out":[{"viewId": 0, "horizontalAngle": 22,"verticalAngle":18}]})
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views":[1]}, 
                                              {"out":[{"viewId": 1, "horizontalAngle": 98,"verticalAngle":102}]})
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views":[2]}, 
                                              {"out":[{"viewId": 1, "horizontalAngle": 98,"verticalAngle":102},
                                                      {"viewId": 0, "horizontalAngle": 22,"verticalAngle":18}]})        
        self.set_MirrorAngle_All(left_vertical=101, left_horizon=99, right_vertical=19, right_horizon=21, sleeptime=3)       
        self.partner.ck_no_event(OUTERREARVIEW_SERVICE_CLIENT, "OuterRearViewMirrorAngle")
        
    @allure.title("通知外后视镜角度_包含左和右外后视镜角度_信号丢失")
    @pytest.mark.full
    def test_caseid_1983478(self):
        self.set_MirrorAngle_Left(horizon=50, vertical=50)
        self.set_MirrorAngle_Right(horizon=50, vertical=50)  
        self.partner.empty_all()
        self.ipdu.pause_bus_send("bodycan")  
        sleep(2)
        self.partner.ck_no_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewMirrorAngle')   
        self.ipdu.resume_bus_send("bodycan") 
        self.partner.ck_no_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewMirrorAngle')        
            
    @allure.title("通知外后视镜折叠状态_包含左和右外后视镜折叠状态_重启后事件上报")
    @pytest.mark.full
    def test_caseid_1983469(self): 
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 0)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 0) 
        self.set_MirrorAngle_Left(horizon=0, vertical=0)
        self.set_MirrorAngle_Right(horizon=0, vertical=0)  
        sleep(2)  
        self.restart_bgm_and_connect_service(OUTERREARVIEW_SERVICE_CLIENT)  
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 0)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 0) 
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatusValidity', {"views":[2]}, 
                                              {"out":[{"value": {"id":0, "foldStatus":0}, "foldStatusValidity": 0},
                                                      {"value": {"id":1, "foldStatus":0}, "foldStatusValidity": 0}]}, timeout=1)   
        # outer_rearview_service_imp|reboot reason|OuterRearViewFoldStatus  
        # 通知外后视镜折叠状态_包含左和右外后视镜折叠状态
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewFoldStatus', 
                                  {"status":[{"id":1,"value":0,"validity":0}, {"id":0,"value":0,"validity":0}]})  

    @allure.title("服务启动默认值")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1984566(self): 
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 3)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 3)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "DrvrMirrorAdjErrorFb", 1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "PassMirrorFoldErrorFb", 1)
        self.set_MirrorAngle_Left(horizon=180, vertical=180) # 外后视镜角度
        self.set_MirrorAngle_Right(horizon=180, vertical=180) # 外后视镜角度
        self.sd_tester.change_car_mode(0) # carmode=0、5
        self.sd_tester.change_usage_mode(2) #usgMod=2、11、13
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr02, "MirrDefrstAtDrvSts", 1) # 避免下发On时，命中HmiDefrstrElecStsMirrr=0
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "MirrDefrstAtPassSts", 1)
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetHeat", {"params": [{"id": 2, "isOn": True}]}) # 后视镜加热状态
        self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, 'SetAutoFoldUnfold', {"params":[{"id":2,"isOn":False}]})   # 后视镜自动折叠设置状态  
        sleep(3)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetAutoFoldUnfold', {"views": [2]},
                                              {"out": [{"id": 2, "isOn": False}]})   
        self.restart_bgm_and_connect_service(OUTERREARVIEW_SERVICE_CLIENT, resume_all_bus=False)    
        # 获取外后视镜折叠状态_带功能安全需求参数 
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatusValidity', {"views":[2]}, 
                                              {"out":[{"value": {"id":0, "foldStatus":0}, "foldStatusValidity": 0}, 
                                                      {"value": {"id":1, "foldStatus":0}, "foldStatusValidity": 0}]})  
        # 获取外后视镜折叠状态_不带功能安全需求参数 
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[2]}, 
                                              {"out":[{"id":0,"foldStatus":0},{"id":1,"foldStatus":0}]})
        # 获取外后视镜角度
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views": [2]},
                                              {"out": [{"viewId": 0, "horizontalAngle": 255, "verticalAngle": 255},
                                                       {"viewId": 1, "horizontalAngle": 255, "verticalAngle": 255}]})  
        # # 获取后视镜加热状态 200AP版本该接口删除
        # self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetHeat', {"views": [2]},
        #                                       {"out": [{"id": 2, "isOn": False}]})                        
        # 获取后视镜下翻状态
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewTiltStatus', {"views":[2]}, 
                                              {"out":[{"id":0,"tiltStatus":0}, {"id":1,"tiltStatus":0}]}) 
        # 获取后视镜自动折叠设置状态 记忆值 2.0修改为不记忆
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetAutoFoldUnfold', {"views": [2]},
                                              {"out": [{"id": 2, "isOn": True}]})
        # 获取后视镜故障
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFault', {}, {"out":[{'faultId': 0, 'faultMsg': '', 'viewId': 2}]})  

    @allure.title("启动场景event")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1984570(self): # DrvModEscOffDrvModEscOff|EscStEscSt
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', 0) # 外后视镜折叠状态
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', 0)   
        self.set_MirrorAngle_All(0, 0, 0, 0) # 外后视镜角度
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "MirrDwnStsAtDrvr", 0) # 后视镜下翻状态
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "MirrDwnStsAtPass", 0) 
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "DrvrMirrorAdjErrorFb", 0) # 外后视镜故障
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "DrvrMirrorFoldErrorFb", 0)  
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "PassMirrorFoldErrorFb", 0)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "PassMirrorAdjErrorFb", 0)  
        #  ViewFoldStatus 外后视镜折叠状态_不带功能安全需求参数
        # HeatStatus  
        self.partner.empty_all(3)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFoldStatus', {"views":[2]}, 
                                              {"out":[{"id":0,"foldStatus":0},{"id":1,"foldStatus":0}]}) # 获取外后视镜折叠状态
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views": [2]},
                                              {"out": [{"viewId": 0, "horizontalAngle": 0, "verticalAngle": 0},
                                                       {"viewId": 1, "horizontalAngle": 0, "verticalAngle": 0}]}) # 外后视镜角度 
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewTiltStatus', {"views": [2]},
                                              {"out": [{"id": 0, "tiltStatus": 0}, {"id": 1, "tiltStatus": 0}]}) # 后视镜下翻状态
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetAutoFoldUnfold', {"views": [2]},
                                              {"out": [{"id": 2, "isOn": True}]}) # 后视镜自动折叠设置状态
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFault', {}, 
                                              {"out":[{'faultId': 0, 'faultMsg': '', 'viewId': 2}]})  # 外后视镜故障  
        
        self.restart_bgm_and_connect_service(OUTERREARVIEW_SERVICE_CLIENT)
        sleep(2)
        # # 通知外后视镜折叠状态（不带功能安全需求参数）200AP版本该接口删除
        # self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, "ViewFoldStatus", {"id":0,"status":0})
        # self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, "ViewFoldStatus", {"id":1,"status":0})         
        # # 通知外后视镜折叠状态（带功能安全需求参数 200AP版本该接口删除
        # self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewFoldStatusValidity', {"id": 0, "status":{"value":0,"validity":0}})
        # self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewFoldStatusValidity', {"id": 1, "status":{"value":0,"validity":0}})
        # 通知外后视镜折叠状态（包含左和右外后视镜折叠状态）
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewFoldStatus', 
                                  {"status":[{"id":1,"value":0,"validity":0}, {"id":0,"value":0,"validity":0}]})
        # # 通知外后视镜角度  200AP版本该接口删除
        # self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'MirrorAngle', 
        #                           {"info":{"viewId": 0, "horizontalAngle": 0,"verticalAngle":0}})
        # self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'MirrorAngle', 
        #                           {"info":{"viewId": 1, "horizontalAngle": 0,"verticalAngle":0}})
        # 通知外后视镜角度（包含左和右外后视镜角度）
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewMirrorAngle', 
                                  {"info":[{"viewId":1,"horizontalAngle":0,"verticalAngle":0},
                                           {"viewId":0,"horizontalAngle":0,"verticalAngle":0}]})
        # # 通知后视镜加热状态 200AP版本该接口删除
        # self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'HeatStatus', {"id":2,"status":False})  
        # 通知后视镜加热（包含加热状态和加热工作状态）
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewHeatStatus', 
                                  {"sts":{"workSts":False,"heatSts":0}}) 
        # # 通知后视镜下翻状态 
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewTiltStatus', {"status":0})
        # self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewTiltStatus', {"id":1, "status":0})
        # self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewTiltStatus', {"id":0, "status":0})
        # 通知后视镜自动折叠设置状态 v2.0 不区分左右后视镜
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'AutoFoldUnfoldStatus', 
                                  {"id":2,"isOn":True})
        # 通知外后视镜故障  
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'ViewFault', 
                                  {"faults":[{'faultId': 0, 'faultMsg': '', 'viewId': 2}]})
        
    @allure.title("BGM首次下线默认配置")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1984564(self):
        # 删除数据库
        bgmssh = BGM_SSH()
        bgmssh.type_commands("sudo rm -rf /data/s2s_service/s2s_service.db3", root_permission=True)
        sleep(1)
        bgmssh.type_commands("ls -l /data/s2s_service")
        sleep(5)
        self.restart_bgm_and_connect_service(OUTERREARVIEW_SERVICE_CLIENT, resume_all_bus=False)    
        # 获取外后视镜折叠状态_不带功能安全需求参数
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, "GetViewFoldStatus", {"views": [2]},
                                              {"out": [{"id": 0, "foldStatus": 0, "clientId": 255},
                                                       {"id": 1, "foldStatus": 0, "clientId": 255}]})
        # 获取外后视镜折叠状态_带功能安全需求参数 
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, "GetViewFoldStatusValidity", {"views": [2]},
                                              {"out": [{"value": {"id":0, "foldStatus":0, "clientId": 255}, "foldStatusValidity": 0}, 
                                                       {"value": {"id":1, "foldStatus":0, "clientId": 255}, "foldStatusValidity": 0}]})
        # # 获取后视镜加热状态 200AP版本该接口删除
        # self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetHeat', {"views": [2]},
        #                                       {"out": [{"id": 2, "isOn": False}]})
        # 获取外后视镜角度
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetMirrorAngle', {"views": [2]},
                                              {"out": [{"viewId": 0, "horizontalAngle": 255, "verticalAngle": 255},
                                                       {"viewId": 1, "horizontalAngle": 255, "verticalAngle": 255}]})
        # 获取后视镜下翻状态
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewTiltStatus', {"views": [2]},
                                              {"out": [{"id": 0, "tiltStatus": 0}, {"id": 1, "tiltStatus": 0}]})
        # 获取后视镜自动折叠设置状态 
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetAutoFoldUnfold', {"views": [2]},
                                              {"out": [{"id": 2, "isOn": True}]})
        # 获取后视镜故障
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetViewFault', {}, 
                                              {"out":[{'faultId': 0, 'faultMsg': '', 'viewId': 2}]})  
            
######################################################################################################################################################## 
@allure.feature("SOA服务接口")
@allure.story("整车控制/OuterRearViewService")
@pytest.mark.aqx
@pytest.mark.mock_tcp
class TestOuterRearViewServiceMockMcu(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, tcp_down_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("OuterRearViewService", "client")])
        self.partner.wait_for_service_reconnect(OUTERREARVIEW_SERVICE_CLIENT)
    
    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
    
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.partner.empty_all()

    @allure.title("获取&通知外后视镜电加热状态_包含加热状态和加热工作状态_取值遍历")
    @pytest.mark.full
    def test_caseid_1983495(self): 
        for value in [1, 2, 3, 4, 5, 0]:
            self.bgm_eth_inter.set_signal("HmiDefrstrElecStsMirrr", value, send_pdu_immediately=True)
            sleep(1)
            workSts=1 if value in [1, 5] else 0
            self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewHeatStatus', {"sts":{"workSts":workSts,"heatSts":value}})   
            self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetOuterRearViewHeatStatus', {"views": [2]},
                                                 {"out": [{"id":2,"sts":{"workSts":workSts,"heatSts":value}}]})      

    @allure.title("获取&通知外后视镜电加热状态_包含加热状态和加热工作状态_Other&服务启动默认值")
    @pytest.mark.full
    def test_caseid_1983499(self): 
        self.bgm_eth_inter.set_signal("HmiDefrstrElecStsMirrr", 4, send_pdu_immediately=True)
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetOuterRearViewHeatStatus', {"views": [2]},
                                                {"out": [{"id":2,"sts":{"workSts":0,"heatSts":4}}]}) 
        self.bgm_eth_inter.set_signal("HmiDefrstrElecStsMirrr", 7, send_pdu_immediately=True)
        self.partner.ck_s2s_event(OUTERREARVIEW_SERVICE_CLIENT, 'OuterRearViewHeatStatus', {"sts":{"workSts":255,"heatSts":255}})   
        self.partner.send_request_and_ck_resp(OUTERREARVIEW_SERVICE_CLIENT, 'GetOuterRearViewHeatStatus', {"views": [2]},
                                                {"out": [{"id":2,"sts":{"workSts":255,"heatSts":255}}]})
