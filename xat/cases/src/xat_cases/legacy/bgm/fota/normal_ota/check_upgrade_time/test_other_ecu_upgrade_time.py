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

@pytest.mark.ecu_mock
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service")])
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
        self.mix.update_version_debug(self.taskid,["DDM"])
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("FOTA_业务性能稳定性-非域控ECU刷写时长小于等于10min") 
    def test_fota_caseid_1991580(self):
        # 更新DDM的SID：10且session_mode：02的回复数据为[0x00, 0x32, 0x01, 0xf4]。此例子的实际回复的数据为：10 02回复50 01 00 32 01 f4
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})

        # 更新DDM的SID：22且DID：F186的回复数据为[0x02]。此例子的实际回复的数据为：22 f1 86回复62 f1 86 02
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])

        # 更新DDM的SID：22且DID：D01C的回复数据为{"NRC": 0x22}即负响应。此例子的实际回复的数据为：22 d0 1c回复7f 22 22
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})

        # 更新DDM的SID：27且为请求安全解锁种子01的回复数据为[0xa9, 0x19, 0xce],发送安全解锁key 02的回复数据为空。此例子的实际回复的数据为：27 01回复67 01 a9 19 ce，27 02回复67 02
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})

        # 更新DDM的SID：34的回复数据为[0x20, 0x0f, 0xa2]。此例子的实际回复的数据为：34 ...回复74 20 0f a2
        self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])

        # 更新DDM的SID：36的block_sequence_counter_nrc_config为空代表所有36服务均回复正相应。如果需要回复负响应，例如：block_sequence_counter_nrc_config={2: 0x78, 18: 0x11} 表示
        # DDM收到第二个counter回复否定响应0x78，第18个counter回复0x11否定响应
        self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})

        # 更新DDM的SID：37的回复数据为空。此例子的实际回复的数据为：67
        self.diag_mock.update_0x37_data(ecu_name="DDM", data={})

        # 更新DDM的SID：31且DID：0212的回复数据为{ 1 : [0x10, 0x00]}。此例子的实际回复的数据为：31 01 02 12回复71 01 02 12 10 00
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x00]}})

        # 更新DDM的SID：31且DID：0301的回复数据为{ 1 : [0x10]}。此例子的实际回复的数据为：31 01 03 01回复71 01 03 01 10
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0301": { 1 : [0x10]}})

        # 更新DDM的SID：31且DID：FF00的回复数据为{ 1 : [0x10]}。此例子的实际回复的数据为：31 01 ff 00回复71 01 ff 00 10
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"FF00": { 1 : [0x10]}})

        # 更新DDM的SID：31且DID：0205的回复数据为{ 1 : [0x10, 0x00, 0x00, 0x00, 0x00]}。此例子的实际回复的数据为：31 01 02 05回复71 01 02 05 10 00 00 00 00
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0205": { 1 : [0x10, 0x00, 0x00, 0x00, 0x00]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="StartUpgrade:hv---addr: 1a12", timeout=600):

            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        start_time = time.time()    
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="OnEcuUpgrade: hv---addr:1a12, upgrade ret(1:ok;0:failed): 1", timeout=800): 
            pass
        end_time = time.time()
        update_time = end_time - start_time
        logger.info(f"DDM升级耗时{update_time}秒")
        assert update_time < 600 
         
if __name__ == "__main__":
    pass