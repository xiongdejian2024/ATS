import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common.common import set_bench_vlan9_ip

@allure.feature("基础架构")
@allure.story("FOTA")
class Test_factory_ota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("AcuModeManagerService","server")])
        self.ssh.update_skip_debug([
                                    FOTA_Skip_Debug.cdc_acu_doip_check
                                    ])
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.fota_back_to_idle()
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == 0
        self.io.bgm_diag_line_down()
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        self.io.set_door(Drvr=Door.close,Pass=Door.close,LeRe=Door.close,RiRe=Door.close,Trunk=Door.close)
        self.mix.set_factory_ota_condition(display_hv_soc=250,low_volt_power=11.5,local_diag_sts=DiagActLineSts.DisActive)   
            
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.io.set_door(Drvr=Door.close,Pass=Door.close,LeRe=Door.close,RiRe=Door.close,Trunk=Door.close)

    @pytest.mark.smoke
    @allure.title("FOTA升级结束_退出刷新模式")
    def test_fota_caseid_1982643(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_UPDATE)
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1fff, data::10 81',
                                                                                  'send stack raw data, addr:1fff, data::10 81',
                                                                                  'send stack raw data, addr:1fff, data::10 81',
                                                                                  'send stack raw data, addr:1fff, data::10 81',
                                                                                  'send stack raw data, addr:1fff, data::10 81',
                                                                                  'send stack raw data, addr:1fff, data::10 81',
                                                                                  'send stack raw data, addr:1fff, data::10 81',
                                                                                  'send stack raw data, addr:1fff, data::10 81'], timeout=480):
            pass

    @pytest.mark.smoke        
    @allure.title("FOTA升级结束_清除DTC_14 FF FF FF")
    def test_fota_caseid_1982638(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_UPDATE)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => factory_exit_ota', timeout=1500):
            pass
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1fff, data::14 ff ff ff',
                                                                                  'send stack raw data, addr:1fff, data::14 ff ff ff',
                                                                                  'send stack raw data, addr:1fff, data::14 ff ff ff'], timeout=300):
            pass
    
    @pytest.mark.sanity
    @allure.title("FOTA升级结束_删除软件包")
    def test_fota_caseid_1982624(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_SUCCESSFUL)
        assert self.ssh.check_file_existence(DeviceName.BGM,path="/update/factory",filename="*.bin") == False        
    
    @pytest.mark.sanity
    @allure.title("FOTA升级结束_DID F153写入")
    def test_fota_caseid_1982627(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_UPDATE)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => factory_exit_ota', timeout=1500):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['SetFotaStateToBgmMcuCb:result:1'], timeout=300):
            pass

    @pytest.mark.smoke
    @allure.title("FOTA升级结束_升级成功")
    def test_fota_caseid_1982626(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_SUCCESSFUL)
        assert self.soa.get_fota_UpdateErrorInfo()
        assert self.soa.get_fota_UpdateProcess(MASTER_UpdateProcess_EVENT.progress) == 100
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['onTimer:Send 3E 80',
                                                                                              'SetVFCReqDiagnosticCb: VfcType :23 ActState :2'],timeout=60):
            pass

    @pytest.mark.smoke
    @allure.title("FOTA升级结束_切carmode肯定响应")
    def test_fota_caseid_1982623(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_FAILED)
        time.sleep(15) #升级结束后执行退出流程需等待约10S，才会执行切carmode操作
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL,car_mode_sub=0)

    @pytest.mark.full
    @allure.title("FOTA升级结束_切carmode否定响应")
    def test_fota_caseid_1982622(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_UPDATE)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => factory_exit_ota', timeout=1500):
            pass
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1002, data::2f d1 34 03 00',
                                                                                'send stack raw data, addr:1002, data::2f d1 34 03 00',
                                                                                'send stack raw data, addr:1002, data::2f d1 34 03 00'],timeout=300):
            pass
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
    
    @pytest.mark.full
    @allure.title("FOTA升级结束_雨刮车窗标定诊断仲裁失败")
    def test_fota_caseid_1982620(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_SUCCESSFUL)
        self.io.bgm_diag_line_up()
        with self.log_manage.check_jetlog_by_keywords(log_type="CALI_DIAGP: ", keywords=['StartEOLCali',
                                                                                        'UpdateNotifyEOLCaliInfoEvent:{"Device":0,"Status":2,"ErrorCode":1,"NRC":0}',
                                                                                        'UpdateNotifyEOLCaliInfoEvent:{"Device":1,"Status":2,"ErrorCode":1,"NRC":0}',
                                                                                        'Arb failed, abort'],timeout=60):
            pass        
    
    @pytest.mark.full
    @allure.title("FOTA升级结束_雨刮车窗标定切usagemode失败")
    def test_fota_caseid_1982619(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_SUCCESSFUL)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        with self.log_manage.check_jetlog_by_keywords(log_type="CALI_DIAGP: ", keywords=['StartEOLCali',
                                                                                        'UpdateNotifyEOLCaliInfoEvent:{"Device":0,"Status":2,"ErrorCode":255,"NRC":0}',
                                                                                        'UpdateNotifyEOLCaliInfoEvent:{"Device":1,"Status":2,"ErrorCode":255,"NRC":0}',
                                                                                        'ChangeToActive failed, abort'],timeout=60):
            pass      
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)

    @pytest.mark.full
    @allure.title("FOTA升级结束_标定开始前开启状态大于30S")
    def test_fota_caseid_1982614(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_SUCCESSFUL)
        self.io.set_door(Drvr=Door.open)
        with self.log_manage.check_jetlog_by_keywords(log_type="CALI_DIAGP: ", keywords=['StartEOLCali',
                                                                                        'UpdateNotifyEOLCaliInfoEvent:{"Device":0,"Status":2,"ErrorCode":255,"NRC":0}',
                                                                                        'UpdateNotifyEOLCaliInfoEvent:{"Device":1,"Status":2,"ErrorCode":255,"NRC":0}',
                                                                                        'Doors not closed, abort'],timeout=60): 
            pass
        self.bus_comm.set_five_door_opener_sts(door_opener=DoorOpenerSts.FullClsd)            
    
    @pytest.mark.full
    @allure.title("FOTA升级结束_标定开始前开启状态小于于30S")
    def test_fota_caseid_1982613(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_SUCCESSFUL)
        self.io.set_door(Drvr=Door.open)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='StartEOLCali:',timeout=60):
            pass
        time.sleep(15) #需要保持门开启状态
        with self.log_manage.check_jetlog_by_keywords(log_type=" CALI_DIAGP:", keywords=['UpdateNotifyEOLCaliInfoEvent:{"Device":1,"Status":3,"ErrorCode":0,"NRC":0}',
                                                                                         'UpdateNotifyEOLCaliInfoEvent:{"Device":0,"Status":2,"ErrorCode":3,"NRC":0}',],timeout=60):
            self.io.set_door(Drvr=Door.close)

    @pytest.mark.smoke        
    @allure.title(" FOTA升级结束_结果记录_DID F154")
    def test_fota_caseid_1982639(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_SUCCESSFUL)
        self.mix.check_factory_F154_results()
        self.sd_tester.write_did_and_check(TA.BGM_SOC,0xf154,SESSION.EXTENDED,UnLock.L5,'666666','62f154666666')   

    @pytest.mark.V_2_1_ONLY
    @pytest.mark.smoke        
    @allure.title(" 升级SRS退出流程_等待10S（累计等待30S）发送重启指令")
    def test_fota_caseid_1987580(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_TASK)
        self.diag_mock.update_0x22_data(ecu_name="SRS", did="F1AA", data_info_update=[0x88, 0x94, 0x52, 0x10, 0x92, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="SRS", did="F1AE", data_info_update=[0x61, 0x50, 0x31, 0x01, 0x00, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:exit_ota => factory_exit_ota',
                                                                                    'SendRawData:raw data: :[ 10 81 ]',
                                                                                    'findEcuFromTaskinfo:has find in task ecu id: 5031, found: 1'],timeout=1500):
            pass
        time.sleep(25) #检测到本次任务中存在SRS升级需等待30S进行重启SRS
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='SendRawData:raw data: :[ 11 01 ]',timeout=60):
            pass

    @pytest.mark.V_2_1_ONLY
    @pytest.mark.smoke        
    @allure.title(" 升级SRS退出流程_重启SRS肯定响应")
    def test_fota_caseid_1987579(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_TASK)
        self.diag_mock.update_0x22_data(ecu_name="SRS", did="F1AA", data_info_update=[0x88, 0x94, 0x52, 0x10, 0x92, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="SRS", did="F1AE", data_info_update=[0x61, 0x50, 0x31, 0x01, 0x00, 0x20, 0x41, 0x41])
        self.diag_mock.update_0x11_data(ecu_name="SRS", reset_type={0x01: [0x01]})
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:exit_ota => factory_exit_ota',
                                                                                    'SendRawData:raw data: :[ 10 81 ]',
                                                                                    'findEcuFromTaskinfo:has find in task ecu id: 5031, found: 1'],timeout=1500):
            pass
        time.sleep(25) #检测到本次任务中存在SRS升级需等待30S进行重启SRS 启动检索需要约3S
        with self.log_manage.check_jetlog_by_keywords(log_type=" diag_client:", keywords=['tx 1c01:11 01',
                                                                                   'rx 1c01:51 01'],timeout=60):
            pass
        time.sleep(2) #重启SRS后需等待5s,进行版本校验 启动检索需要约3S
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='CheckCarMode:get car mode ret:0 car mode:0',timeout=300):
            pass
        sleep(30) #等待标定结束
        
    @pytest.mark.V_2_1_ONLY
    @pytest.mark.V_2_0
    @pytest.mark.smoke        
    @allure.title(" 升级SRS退出流程_重启SRS持续否定响应")
    def test_fota_caseid_1987578(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_TASK)
        self.diag_mock.update_0x22_data(ecu_name="SRS", did="F1AA", data_info_update=[0x88, 0x94, 0x52, 0x10, 0x92, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="SRS", did="F1AE", data_info_update=[0x61, 0x50, 0x31, 0x01, 0x00, 0x20, 0x41, 0x41])
        self.diag_mock.update_0x11_data(ecu_name="SRS", reset_type={0x01: {"NRC": 0x22}})
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:exit_ota => factory_exit_ota',
                                                                                    'SendRawData:raw data: :[ 10 81 ]',
                                                                                    'findEcuFromTaskinfo:has find in task ecu id: 5031, found: 1'],timeout=1500):
            pass
        time.sleep(25) #检测到本次任务中存在SRS升级需等待30S进行重启SRS,启动检索需要约3S
        with self.log_manage.check_jetlog_by_keywords(log_type='-E "fota: | diag_client:"', keywords=[' tx 1c01:11 01',
                                                                                                    ' rx 1c01:7f 11 22',
                                                                                                    ' tx 1c01:11 01',
                                                                                                    ' rx 1c01:7f 11 22',
                                                                                                    ' tx 1c01:11 01',
                                                                                                    ' rx 1c01:7f 11 22',
                                                                                                    'ResetSRSExitCb:reset srs result: 0after reset srs  waiting 5s to start version collection',
                                                                                                    'CheckCarMode:get car mode ret:0 car mode:0'],timeout=300):
            pass
        sleep(30) #等待标定结束
        
    @pytest.mark.V_2_1_ONLY
    @pytest.mark.full        
    @allure.title(" 升级SRS退出流程_重启SRS持续无响应")
    def test_fota_caseid_1987577(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_TASK)
        self.diag_mock.update_0x22_data(ecu_name="SRS", did="F1AA", data_info_update=[0x88, 0x94, 0x52, 0x10, 0x92, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="SRS", did="F1AE", data_info_update=[0x61, 0x50, 0x31, 0x01, 0x00, 0x20, 0x41, 0x41])
        self.diag_mock.update_0x11_data(ecu_name="SRS", reset_type={0x01: {"NRC":"no_reply"}})
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:exit_ota => factory_exit_ota',
                                                                                    'SendRawData:raw data: :[ 10 81 ]',
                                                                                    'findEcuFromTaskinfo:has find in task ecu id: 5031, found: 1'],timeout=1500):
            pass
        time.sleep(25) #检测到本次任务中存在SRS升级需等待30S进行重启SRS 启动检索需要约3S
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['SendRawData:raw data: :[ 11 01 ]',
                                                                                    'SendRawData:raw data: :[ 11 01 ]',
                                                                                    'SendRawData:raw data: :[ 11 01 ]',
                                                                                    'ResetSRSExitCb:reset srs result: 0after reset srs  waiting 5s to start version collection',
                                                                                    'CheckCarMode:get car mode ret:0 car mode:0'],timeout=300):
            pass
        sleep(30) #等待标定结束

    @pytest.mark.V_2_2
    @pytest.mark.full     
    @allure.title(" V2.2_含SRS升级_退出流程不重启SRS")
    def test_fota_caseid_1995489(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_TASK)
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="SRS", did="F1AA", data_info_update=[0x88, 0x94, 0x52, 0x10, 0x92, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="SRS", did="F1AE", data_info_update=[0x61, 0x50, 0x31, 0x01, 0x00, 0x20, 0x41, 0x41])
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
        self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
        self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
        self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x00]}})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0301": { 1 : [0x10]}})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"FF00": { 1 : [0x10]}})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0205": { 1 : [0x10, 0x00, 0x00, 0x00, 0x00]}})
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:exit_ota => factory_exit_ota',
                                                                                    'SendRawData:raw data: :[ 10 81 ]',
                                                                                    'waiting 20s to start version collection'],timeout=1000):
            pass
        time.sleep(17) #等待20S 进行版本校验
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='GetVehicleECUVersion:',timeout=60):
            pass
        self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status,target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=300)

if __name__ == "__main__":
    pass