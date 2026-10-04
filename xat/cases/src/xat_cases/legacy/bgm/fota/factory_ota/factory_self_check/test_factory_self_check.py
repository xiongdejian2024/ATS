import os
import sys
import pytest
import allure
import yaml
import json
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common.common import set_bench_vlan9_ip

@pytest.mark.ecu_mock
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service")])
        self.ssh.update_skip_debug([
                                    FOTA_Skip_Debug.cdc_acu_doip_check
                                    ]) 
        self.sd_tester.write_ccp({950: 0x01, 962: 0x00,971: 0x00})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x00,971: 0x00})

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.fota_back_to_idle()
        self.io.bgm_diag_line_down()
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_TASK)
        self.mix.set_factory_ota_condition(display_hv_soc=250,low_volt_power=11.5,local_diag_sts=DiagActLineSts.DisActive)
                    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.sd_tester.diag_cancel()
        self.mix.fota_back_to_idle()
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.sd_tester.write_ccp({950: 0x01, 962: 0x00,971: 0x00})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({950: 0x01, 962: 0x00,971: 0x00})

    @pytest.mark.sanity
    @allure.title("自检任务_mapping解析")
    def test_fota_caseid_1983313(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=["ChangeState:factory_check_condition => factory_build_task",
                                                                                   'loadFactoryTaskFromConfig:PATH:/update/factory/mapping.json',
                                                                                   'parseFactoryTaskInfo:------ factory task mapping info ------',
                                                                                   'AwmOnlineStsResult:wait 20s to collect version, wait NKR ready'], timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @pytest.mark.full
    @allure.title("自检任务_软件匹配_域控软件版本不匹配")
    def test_fota_caseid_1983301(self):
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="NotifyFactoryFOTATaskCheckErrorInfo:ecu name:BGM, ecu_id:6011,error:2", timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert "'ecuName': 'BGM'" not in str(self.soa.get_fota_UpdateErrorInfo())  

    @pytest.mark.sanity
    @allure.title("自检任务_版本收集PN list")
    def test_fota_caseid_1983312(self):
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=["ecu name:DDM ,hwpn:8892362682  A ,hwpn ncr : :[ ]",
                                                                                  "swpn:6150910055 AA",
                                                                                  "swpn:1250910055 AA"], timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)     

    @pytest.mark.sanity
    @allure.title("自检任务_未检测到ECU PN list")
    def test_fota_caseid_1983311(self):
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update={"NRC": 0x22})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:1 ,", timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
    
    @pytest.mark.full
    @allure.title("自检任务_软件匹配_格式解析错误")
    def test_fota_caseid_1983302(self):
        with open('config/ota_mapping.yaml', 'r') as f:
            mapping = yaml.safe_load(f)
        mapping["ecu"][1]["ecuGroup"] = None
        mapping = json.dumps(mapping).replace('{', '{ ').replace('}', ' }').replace('"', '\\"')
        self.ssh.type_commands(DeviceName.BGM, f'echo -n "{mapping}" > /update/factory/mapping.json')
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_SUCCESSFUL.value, timeout=1200)
        assert "'ecuName': 'DDM', 'errorCode': 6" in str(self.soa.get_fota_UpdateErrorInfo())

    @pytest.mark.smoke
    @allure.title("自检任务_软件匹配_NeedProgramming File List")
    def test_fota_caseid_1983303(self):
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=["filterNeedProgramECUPkgInfo:swpn:6150910055 AA",
                                                                                   "filterNeedProgramECUPkgInfo:app pkg size:1, other pkg size:1, ess pkg size:0"], timeout=600):
            pass

    @pytest.mark.full
    @allure.title("自检任务_软件匹配_软件依赖错误_仅SBL文件")
    def test_fota_caseid_1983304(self):
        with open('config/ota_mapping.yaml', 'r') as f:
            mapping = yaml.safe_load(f)
        mapping = json.dumps(mapping).replace('{', '{ ').replace('}', ' }').replace('"', '\\"')
        self.ssh.type_commands(DeviceName.BGM, f'echo -n "{mapping}" > /update/factory/mapping.json')
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F1AA", data_info_update=[0x88, 0x93, 0x01, 0x37, 0x14, 0x20, 0x20, 0x42])
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x02, 0x00, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x02, 0x00, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=["EcuSelfSWCheck: ecu name: ECM3 ecu id: 5091 hasEcuSelfSWCheck: 1",
                                                                                   "reloadTaskInfoFromPers:name:ECM3 has sbl"], timeout=600):
            pass
      
    @pytest.mark.full
    @allure.title("自检任务_软件匹配_软件依赖错误_单APP文件")
    def test_fota_caseid_1983305(self):
        with open('config/ota_mapping.yaml', 'r') as f:
            mapping = yaml.safe_load(f)
        mapping = json.dumps(mapping).replace('{', '{ ').replace('}', ' }').replace('"', '\\"')
        self.ssh.type_commands(DeviceName.BGM, f'echo -n "{mapping}" > /update/factory/mapping.json')
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F1AA", data_info_update=[0x88, 0x93, 0x01, 0x37, 0x14, 0x20, 0x20, 0x42])
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x01, 0x00, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x02, 0x00, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="EcuSelfSWCheck: ecuSelfSWCheck failed , so not program ecu: ECM3", timeout=600):
            pass
        assert "'ecuName': 'ECM3', 'errorCode': 7" in str(self.soa.get_fota_UpdateErrorInfo())

    @pytest.mark.full
    @allure.title("自检任务_软件匹配_软件依赖错误_多data文件")
    def test_fota_caseid_1983306(self):
        with open('config/ota_mapping.yaml', 'r') as f:
            mapping = yaml.safe_load(f)
        mapping = json.dumps(mapping).replace('{', '{ ').replace('}', ' }').replace('"', '\\"')
        self.ssh.type_commands(DeviceName.BGM, f'echo -n "{mapping}" > /update/factory/mapping.json')
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F1AA", data_info_update=[0x88, 0x93, 0x01, 0x37, 0x14, 0x20, 0x20, 0x42])
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x02, 0x00, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x01, 0x00, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="EcuSelfSWCheck: ecuSelfSWCheck failed , so not program ecu: ECM3", timeout=600):
            pass
        assert "'ecuName': 'ECM3', 'errorCode': 7" in str(self.soa.get_fota_UpdateErrorInfo())

    @pytest.mark.full
    @allure.title("自检任务_软件匹配_硬件号错误_模糊索引_硬件号匹配")
    def test_fota_caseid_1983307(self):
        with open('config/ota_mapping.yaml', 'r') as f:
            mapping = yaml.safe_load(f)
        mapping["ecu"][1]["ecuId"] = "6029"
        mapping = json.dumps(mapping).replace('{', '{ ').replace('}', ' }').replace('"', '\\"')
        self.ssh.type_commands(DeviceName.BGM, f'echo -n "{mapping}" > /update/factory/mapping.json')
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="findECUHwVersionInTask:ECU HWPN matched:8892362682  A, so change collected ecu id to6029", timeout=600):
        #     pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="findECUHwVersionInTask:ECU ecuId fuzzy matched and HWPN matched, ecuId: 6029, HWPN: 8892362682  A", timeout=600):
            pass

    @pytest.mark.full
    @allure.title("自检任务_软件匹配_硬件号错误_模糊索引_ECUID&硬件号不匹配")
    def test_fota_caseid_1983308(self):
        with open('config/ota_mapping.yaml', 'r') as f:
            mapping = yaml.safe_load(f)
        mapping["ecu"][1]["ecuId"] = "6029"
        mapping = json.dumps(mapping).replace('{', '{ ').replace('}', ' }').replace('"', '\\"')
        self.ssh.type_commands(DeviceName.BGM, f'echo -n "{mapping}" > /update/factory/mapping.json')
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x98, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="ChangeState:factory_build_task => ", timeout=600):
            pass
        assert "'ecuName': 'DDM', 'errorCode': 3" in str(self.soa.get_fota_UpdateErrorInfo())

    @pytest.mark.full
    @allure.title("自检任务_软件匹配_硬件号错误_模糊索引_硬件号不匹配")
    def test_fota_caseid_1983309(self):
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x98, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="ChangeState:factory_build_task => ", timeout=600):
            pass
        assert "'ecuName': 'DDM', 'errorCode': 3" in str(self.soa.get_fota_UpdateErrorInfo())

    @pytest.mark.V_2_0
    @pytest.mark.smoke
    @allure.title("自检任务_软件匹配_BGM_CCPID1,CCPValuea3,mapping文件ECU CCPID为1，CCPValue为a1")
    def test_fota_caseid_1986940(self):
        self.sd_tester.write_ccp({1: 0xa3})
        self.sd_tester.reset_bgm() #写入CCP ID 1 = A3
        with open('config/ota_mapping.yaml', 'r') as f:
            mapping = yaml.safe_load(f)
        mapping["ecu"][1]["packages"][0]["ccpId"] = 1
        mapping["ecu"][1]["packages"][1]["ccpId"] = 1
        mapping["ecu"][1]["packages"][0]["ccpCode"] = 'a1'
        mapping["ecu"][1]["packages"][1]["ccpCode"] = 'a1'
        mapping = json.dumps(mapping).replace('{', '{ ').replace('}', ' }').replace('"', '\\"')
        self.ssh.type_commands(DeviceName.BGM, f'echo -n "{mapping}" > /update/factory/mapping.json') #将修改mapping ccpid和value导入
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="compareCCPCode:compare ccp_code, expexted ccp_id: a1, real ccp_code: a3", timeout=600):
            pass
        assert "'ecuName': 'DDM', 'errorCode': 3" in str(self.soa.get_fota_UpdateErrorInfo())

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("自检任务_软件匹配_BGM_CCPID962,CCPValue00,mapping文件ECU CCPID为953，CCPValue为空")
    def test_fota_caseid_1986941(self):
        self.sd_tester.write_ccp({962: 0x00})
        self.sd_tester.reset_bgm() #写入CCP 
        with open('config/ota_mapping.yaml', 'r') as f:
            mapping = yaml.safe_load(f)
        mapping["ecu"][1]["packages"][0]["ccpId"] = 953
        mapping["ecu"][1]["packages"][1]["ccpId"] = 953
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=["filterNeedProgramECUPkgInfo:swpn:6150910055 AA",
                                                                                   "reloadTaskInfoFromPers:name:DDM, ecu app pKg size: 1"], timeout=600):
            pass

    @pytest.mark.V_2_0
    @pytest.mark.full
    @allure.title("自检任务_软件匹配_BGM_CCPID962,CCPValue00,mapping文件ECU CCPID为-100默认值，CCPValue为2")
    def test_fota_caseid_1986942(self):
        self.sd_tester.write_ccp({962: 0x00})
        self.sd_tester.reset_bgm() #写入CCP 
        with open('config/ota_mapping.yaml', 'r') as f:
            mapping = yaml.safe_load(f)
        mapping["ecu"][1]["packages"][0]["ccpCode"] = '02'
        mapping["ecu"][1]["packages"][1]["ccpCode"] = '02'
        mapping = json.dumps(mapping).replace('{', '{ ').replace('}', ' }').replace('"', '\\"')
        self.ssh.type_commands(DeviceName.BGM, f'echo -n "{mapping}" > /update/factory/mapping.json') #将修改mapping ccpid和value导入
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=["filterNeedProgramECUPkgInfo:swpn:6150910055 AA",
                                                                                   "reloadTaskInfoFromPers:name:DDM, ecu app pKg size: 1"], timeout=600):
            pass

    @pytest.mark.V_2_0
    @pytest.mark.smoke
    @allure.title("自检任务_软件匹配_BGM_CCPID962,CCPValue00,mapping文件ECU CCPID为-100默认值，CCPValue为空")
    def test_fota_caseid_1986943(self):
        self.sd_tester.write_ccp({962: 0x00})
        self.sd_tester.reset_bgm() #写入CCP 
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=["filterNeedProgramECUPkgInfo:swpn:6150910055 AA",
                                                                                   "reloadTaskInfoFromPers:name:DDM, ecu app pKg size: 1"], timeout=600):
            pass

    @pytest.mark.V_2_0
    @pytest.mark.smoke
    @allure.title("自检任务_软件匹配_BGM_CCPID1556,CCPValue01,mapping文件ECU CCPID为1556，CCPValue为01")
    def test_fota_caseid_1986944(self):
        self.sd_tester.write_ccp({1556: 0x01})
        self.sd_tester.reset_bgm() #写入CCP 
        with open('config/ota_mapping.yaml', 'r') as f:
            mapping = yaml.safe_load(f)
        mapping["ecu"][1]["packages"][0]["ccpId"] = 1556
        mapping["ecu"][1]["packages"][1]["ccpId"] = 1556
        mapping["ecu"][1]["packages"][0]["ccpCode"] = '01'
        mapping["ecu"][1]["packages"][1]["ccpCode"] = '01'
        mapping = json.dumps(mapping).replace('{', '{ ').replace('}', ' }').replace('"', '\\"')
        self.ssh.type_commands(DeviceName.BGM, f'echo -n "{mapping}" > /update/factory/mapping.json') #将修改mapping ccpid和value导入
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=["filterNeedProgramECUPkgInfo:swpn:6150910055 AA",
                                                                                   "reloadTaskInfoFromPers:name:DDM, ecu app pKg size: 1"], timeout=600):
            pass

    @pytest.mark.V_2_0	
    @pytest.mark.smoke
    @allure.title("自检任务_软件匹配_BGM_CCP:950==02,962==00 ,VDDM刷写400V软件，BBM刷写400V软件，BNCM 天幕类型971 = 00")
    def test_fota_caseid_1991567(self):
        self.ssh.download_factory_package_to_bgm(package_url='https://minio.jidupmastaging.com/rsms/rsms/staging/67342184e4b00026e2712b10_6200000300ADY.zip')
        self.ssh.type_commands(DeviceName.BGM,'rm -rf /update/factory/*;sync;cp /data/factory_package/* /update/factory;sync')
        self.sd_tester.write_ccp({950: 0x02,962: 0x00,971: 0x00})
        self.sd_tester.reset_bgm() #写入CCP 
        self.diag_mock.update_0x22_data(ecu_name="BNCM", did="F1AA", data_info_update=[0x25, 0x00, 0x00, 0x00, 0x96, 0x20, 0x20, 0x43]) #2500000096 C
        self.diag_mock.update_0x22_data(ecu_name="BNCM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="VDDM", did="F1AA", data_info_update=[0x88, 0x91, 0x98, 0x35, 0x75, 0x20, 0x20, 0x41]) #8891983575 A
        self.diag_mock.update_0x22_data(ecu_name="VDDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="BBM", did="F1AA", data_info_update=[0x88, 0x91, 0x38, 0x06, 0x80, 0x20, 0x20, 0x42]) #8891380680 B
        self.diag_mock.update_0x22_data(ecu_name="BBM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['compareCCPCode:compare ccp_code, expexted ccp_id: 00, real ccp_code: 0',
                                                                                'findECUHwVersionInTask:ECU ecuId and HWPN matched, ecuId: 1022, HWPN: 2500000096  C',
                                                                                "compareCCPCode:compare ccp_code, expexted ccp_id: 00, real ccp_code: 0",
                                                                                "findECUHwVersionInTask:ECU ecuId and HWPN matched, ecuId: 5011, HWPN: 8891983575  A",
                                                                                'compareCCPCode:compare ccp_code, expexted ccp_id: 00, real ccp_code: 0',
                                                                                'findECUHwVersionInTask:ECU ecuId and HWPN matched, ecuId: 5021, HWPN: 8891380680  B'], timeout=600):
            pass  

    @pytest.mark.V_2_0	
    @pytest.mark.smoke
    @allure.title("自检任务_软件匹配_BGM_CCP:950==02,962==02 ,VDDM刷写VDDM_800V软件，BBM刷写BBM_800V软件，BNCM 天幕类型 971 = 01")
    def test_fota_caseid_1991566(self):
        self.ssh.download_factory_package_to_bgm(package_url='https://minio.jidupmastaging.com/rsms/rsms/staging/67342184e4b00026e2712b10_6200000300ADY.zip')
        self.ssh.type_commands(DeviceName.BGM,'rm -rf /update/factory/*;sync;cp /data/factory_package/* /update/factory;sync')
        self.sd_tester.write_ccp({950: 0x02,962: 0x02,971: 0x01})
        self.sd_tester.reset_bgm() #写入CCP 
        self.diag_mock.update_0x22_data(ecu_name="BNCM", did="F1AA", data_info_update=[0x25, 0x00, 0x00, 0x00, 0x96, 0x20, 0x20, 0x43]) #2500000096 C
        self.diag_mock.update_0x22_data(ecu_name="BNCM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="VDDM", did="F1AA", data_info_update=[0x88, 0x91, 0x98, 0x35, 0x75, 0x20, 0x20, 0x41]) #8891983575 A
        self.diag_mock.update_0x22_data(ecu_name="VDDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="BBM", did="F1AA", data_info_update=[0x88, 0x91, 0x38, 0x06, 0x80, 0x20, 0x20, 0x42]) #8891380680 B
        self.diag_mock.update_0x22_data(ecu_name="BBM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['compareCCPCode:compare ccp_code, expexted ccp_id: 01, real ccp_code: 1',
                                                                                'findECUHwVersionInTask:ECU ecuId and HWPN matched, ecuId: 1022, HWPN: 2500000096  C',
                                                                                "compareCCPCode:compare ccp_code, expexted ccp_id: 02, real ccp_code: 2",
                                                                                "findECUHwVersionInTask:ECU ecuId fuzzy matched and HWPN matched, ecuId: 5012, HWPN: 8891983575  A",
                                                                                'compareCCPCode:compare ccp_code, expexted ccp_id: 02, real ccp_code: 2',
                                                                                'findECUHwVersionInTask:ECU ecuId and HWPN matched, ecuId: 5021, HWPN: 8891380680  B'], timeout=600):
            pass 

    @pytest.mark.V_2_0	
    @pytest.mark.smoke
    @allure.title("自检任务_软件匹配_BGM_CCP:950==01,962==02 ,VDDM刷写VDDM_MCA软件，BBM刷写BBM_MCA软件")
    def test_fota_caseid_1991563(self):
        self.ssh.download_factory_package_to_bgm(package_url='https://minio.jidupmastaging.com/rsms/rsms/staging/67340292e4b00026e2712ae9_6100000300ABY.zip')
        self.ssh.type_commands(DeviceName.BGM,'rm -rf /update/factory/*;sync;cp /data/factory_package/* /update/factory;sync')
        self.sd_tester.write_ccp({950: 0x01,962: 0x02})
        self.sd_tester.reset_bgm() #写入CCP 
        self.diag_mock.update_0x22_data(ecu_name="VDDM", did="F1AA", data_info_update=[0x88, 0x91, 0x98, 0x35, 0x75, 0x20, 0x20, 0x41]) #8891983575 A
        self.diag_mock.update_0x22_data(ecu_name="VDDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="BBM", did="F1AA", data_info_update=[0x88, 0x91, 0x38, 0x06, 0x80, 0x20, 0x20, 0x42]) #8891380680 B
        self.diag_mock.update_0x22_data(ecu_name="BBM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=["compareCCPCode:compare ccp_code, expexted ccp_id: 02, real ccp_code: 2",
                                                                                "findECUHwVersionInTask:ECU ecuId fuzzy matched and HWPN matched, ecuId: 5012, HWPN: 8891983575  A",
                                                                                'compareCCPCode:compare ccp_code, expexted ccp_id: 02, real ccp_code: 2',
                                                                                'findECUHwVersionInTask:ECU ecuId fuzzy matched and HWPN matched, ecuId: 5022, HWPN: 8891380680  B',
                                                                                'reloadTaskInfoFromPers:name:VDDM_MCA has sbl',
                                                                                'reloadTaskInfoFromPers:name:BBM_MCA has sbl'], timeout=600):
            pass 

    @pytest.mark.V_2_0	
    @pytest.mark.smoke
    @allure.title("自检任务_软件匹配_BGM_CCP:950==01,962==00 ,VDDM刷写400V软件，BBM刷写400V软件")
    def test_fota_caseid_1991562(self):
        self.ssh.download_factory_package_to_bgm(package_url='https://minio.jidupmastaging.com/rsms/rsms/staging/67340292e4b00026e2712ae9_6100000300ABY.zip')
        self.ssh.type_commands(DeviceName.BGM,'rm -rf /update/factory/*;sync;cp /data/factory_package/* /update/factory;sync')
        self.sd_tester.write_ccp({950: 0x01,962: 0x00})
        self.sd_tester.reset_bgm() #写入CCP 
        self.diag_mock.update_0x22_data(ecu_name="VDDM", did="F1AA", data_info_update=[0x88, 0x91, 0x98, 0x35, 0x75, 0x20, 0x20, 0x41]) #8891983575 A
        self.diag_mock.update_0x22_data(ecu_name="VDDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="BBM", did="F1AA", data_info_update=[0x88, 0x91, 0x38, 0x06, 0x80, 0x20, 0x20, 0x42]) #8891380680 B
        self.diag_mock.update_0x22_data(ecu_name="BBM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=["compareCCPCode:compare ccp_code, expexted ccp_id: 00, real ccp_code: 0",
                                                                                "findECUHwVersionInTask:ECU ecuId and HWPN matched, ecuId: 5011, HWPN: 8891983575  A",
                                                                                'compareCCPCode:compare ccp_code, expexted ccp_id: 00, real ccp_code: 0',
                                                                                'findECUHwVersionInTask:ECU ecuId and HWPN matched, ecuId: 5021, HWPN: 8891380680  B',
                                                                                'reloadTaskInfoFromPers:name:VDDM has sbl',
                                                                                'reloadTaskInfoFromPers:name:BBM has sbl'], timeout=600):
            pass 
if __name__ == "__main__":
    pass