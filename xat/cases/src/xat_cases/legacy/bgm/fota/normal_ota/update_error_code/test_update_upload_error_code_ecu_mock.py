import os
import sys
import pytest
import allure
import yaml

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
                    FOTA_Skip_Debug.car_mode_normal,
                    FOTA_Skip_Debug.baseline,
                    FOTA_Skip_Debug.before_group_1081,
                    FOTA_Skip_Debug.before_group_hv_ctl,
                    FOTA_Skip_Debug.ecm3_down_hv,
                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                    FOTA_Skip_Debug.upload_version_from_debug_file,
                    FOTA_Skip_Debug.CDC_UA,
                    FOTA_Skip_Debug.ACU_UA,
                    FOTA_Skip_Debug.version_collect,
                    FOTA_Skip_Debug.cdc_acu_doip_check,
                    FOTA_Skip_Debug.update_precondition_check
                    ]) 
        self.mix.update_version_debug(self.taskid,["DDM"])
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.mix.back_fota_to(FOTAMasteSts.IDLE,taskid=self.taskid) 
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @allure.title("上传云端_Retry_Programming_Faile(0328)") 
    def test_fota_caseid_1983096(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0328"'], timeout=300):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            
    # @allure.title("上传云端_Retry_Programming_Success(03FA)") 
    # def test_fota_caseid_1983095(self):
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
    #     self.diag_mock.update_0x34_data(ecu_name="DDM", data={"NRC": 0x22})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords="send stack raw data, addr:1a12, data::34", timeout=300):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
    #     time.sleep(1) # 等待第一轮刷写 34重试结束
    #     self.diag_mock.update_0x11_data(ecu_name="DDM", reset_type=0x01)
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
    #     self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
    #     self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
    #     self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x00]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0301": { 1 : [0x10]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"FF00": { 1 : [0x10]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0205": { 1 : [0x10, 0x00, 0x00, 0x00, 0x00]}})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"03FA"'], timeout=1200):
    #         pass

    @allure.title("上传云端_ECU_CANNOT_EnterProgrammingSession(030A)_1002负响应") 
    def test_fota_caseid_1987439(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: {"NRC": 0x22}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"030A"'], timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @allure.title("上传云端_ECU_CANNOT_EnterProgrammingSession(030A)_不回复1002") 
    def test_fota_caseid_1987442(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: {"NRC": "no_reply"}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"030A"'], timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @allure.title("上传云端_ECU_CANNOT_EnterProgrammingSession(030A)_22f186负响应") 
    def test_fota_caseid_1987440(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update={"NRC": 0x22})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"030A"'], timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @allure.title("上传云端_ECU_CANNOT_EnterProgrammingSession(030A)_不回复22f186") 
    def test_fota_caseid_1987441(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update={"NRC": "no_reply"})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"030A"'], timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

# SOA-24098 现阶段暂不做要求，偏差接受
    # @allure.title("上传云端_ECU_ECU_Unlock_Failed(0320)_2701负响应") 
    # def test_fota_caseid_1987443(self):
    #     self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: {"NRC": 0x22}})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0320"'], timeout=600):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

# SOA-24098 现阶段暂不做要求，偏差接受
    # @allure.title("上传云端_ECU_Update_Failed(031D)_不回复2701") 
    # def test_fota_caseid_1987429(self):
    #     self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: {"NRC": "no_reply"}})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"031D"'], timeout=600):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
    
# SOA-24098 现阶段暂不做要求，偏差接受
    # @allure.title("上传云端_ECU_Unlock_Failed(0320)_2702负响应") 
    # def test_fota_caseid_1987444(self):
    #     self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: {"NRC": 0x22}})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0320"'], timeout=600):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

# SOA-24098 现阶段暂不做要求，偏差接受
    # @allure.title("上传云端_ECU_Unlock_Failed(031D)_不回复2702") 
    # def test_fota_caseid_1987427(self):
    #     self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: {"NRC": "no_reply"}})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"031D"'], timeout=600):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

# SOA-24098 现阶段暂不做要求，偏差接受
    # @allure.title("上传云端_ECU_CheckSignature_Failed(0321)_负响应") 
    # def test_fota_caseid_1987445(self):
    #     self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
    #     self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
    #     self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
    #     self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : {"NRC": 0x22}}})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0321"'], timeout=600):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

# SOA-24098 现阶段暂不做要求，偏差接受
    # @allure.title("上传云端_ECU_CheckSignature_Failed(0321)_不回复") 
    # def test_fota_caseid_1983118(self):
    #     self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
    #     self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
    #     self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
    #     self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : {"NRC": "no_reply"}}})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0321"'], timeout=600):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

# SOA-24098 现阶段暂不做要求，偏差接受
    # @allure.title("上传云端_ECU_SBLActive_Failed(0322)_负响应") 
    # def test_fota_caseid_1995908(self):
    #     self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
    #     self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
    #     self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
    #     self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x00]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0301": { 1 : {"NRC": 0x22}}})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0322"'], timeout=600):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

# SOA-24098 现阶段暂不做要求，偏差接受
    # @allure.title("上传云端_ECU_SBLActive_Failed(0322)_不回复") 
    # def test_fota_caseid_1995809(self):
    #     self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
    #     self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
    #     self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
    #     self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x00]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0301": { 1 : {"NRC": "no_reply"}}})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0322"'], timeout=600):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

# SOA-24098 现阶段暂不做要求，偏差接受
    # @allure.title("上传云端_ECU_EraseError_Failed(0323)_负响应") 
    # def test_fota_caseid_1995910(self):
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
    #     self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
    #     self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
    #     self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x00]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0301": { 1 : [0x10]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"FF00": { 1 : {"NRC": 0x22}}})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0323"'], timeout=600):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

# SOA-24098 现阶段暂不做要求，偏差接受
    # @allure.title("上传云端_ECU_EraseError_Failed(0323)_不回复") 
    # def test_fota_caseid_1983116(self):
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
    #     self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
    #     self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
    #     self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x00]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0301": { 1 : [0x10]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"FF00": { 1 : {"NRC": "no_reply"}}})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0323"'], timeout=600):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

# SOA-24098 现阶段暂不做要求，偏差接受
    # @allure.title("上传云端_ECU_CompleteCompatible_Failed(0324)_负响应") 
    # def test_fota_caseid_1987448(self):
    #     assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
    #     self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
    #     self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
    #     self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x00]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0301": { 1 : [0x10]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"FF00": { 1 : [0x10]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0205": { 1 : {"NRC": 0x22}}})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0324"'], timeout=600):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

# SOA-24098 现阶段暂不做要求，偏差接受
    # @allure.title("上传云端_ECU_CompleteCompatible_Failed(0324)_不回复") 
    # def test_fota_caseid_1983115(self):
    #     assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
    #     self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
    #     self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
    #     self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x00]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0301": { 1 : [0x10]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"FF00": { 1 : [0x10]}})
    #     self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0205": { 1 : {"NRC": "no_reply"}}})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0324"'], timeout=600):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

if __name__ == "__main__":
    pass

    




