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
from xat_ecu.legacy.common.data_handle import *
from xat_ecu.legacy.protocol.ProtocolServerKeywords import ProtocolServerKeywords

@pytest.mark.ecu_mock
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota_EcuMock_A(TestABCBase):
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
        set_bench_vlan9_ip("172.16.9.21")
        
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
    @pytest.mark.sanity
    @allure.title("非域控刷写_仅升级小件") 
    def test_fota_caseid_1987565(self):
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
        self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 120)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="OnEcuUpgrade: hv---addr:1a12, upgrade ret(1:ok;0:failed): 1", timeout=800): 
            pass


@pytest.mark.ecu_mock
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota_EcuMock_B(TestABCBase):
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
                                    FOTA_Skip_Debug.update_precondition_check
                                    ])
        self.mix.update_version_debug(self.taskid,["CD"]) 
        set_bench_vlan9_ip("172.16.9.21")
        self.server_mock = ProtocolServerKeywords('doip', '172.16.9.21', 13400)
        self.server_mock.init_middleware()
        self.ssh.type_commands(DeviceName.BGM,"cp /data/debug_bak.sh /data/debug.sh;sync")
        self.ssh.type_commands(DeviceName.BGM,"cd /data;chmod 777 debug.sh;sync")
        self.ssh.type_commands(DeviceName.BGM,"cd /data;chmod -R 777 sl;sync")
        self.ssh.type_commands(DeviceName.BGM,"cd /data;/app/bin/swdl -nw 10 1;sync") 
        self.io.bgm_power_off()
        sleep(3)
        self.io.bgm_power_on()
        sleep(20)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.mix.fota_back_to_idle()


    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.server_mock.doip_sock_obj.tcp_server_sock.stop()
        self.ssh.type_commands(DeviceName.BGM,"cd /data;/app/bin/swdl -nw 10 0;sync")
        self.ssh.type_commands(DeviceName.BGM,"cd /data;rm debug_script_executed_count;rm -rf debug.sh;sync")

    @pytest.mark.V3_0_0
    @pytest.mark.smoke
    @allure.title("常规ota_含CD升级成功_正向流程") 
    def test_fota_caseid_1997073(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1281: {
                0x22: {
                    0xf1aa: ['62f1aa8895037286202043'],
                    0xf1ae: ['62f1ae016230310210204142'],
                    0xf186: ['62f18602'],
                    0xd01c: ['7f2222'],
                },
                0x31: {
                    0x010206: ['710102061001'],
                    0x01ff00: ['7101ff0010'],
                    0x010205: ['710102051000000000'],
                    0x01a100: ['7101a1001000'],
                    0x010212: ['710102121000'],
                },
                0x34: {
                    0x00: ['744000000802']
                },
                0x10: {
                    0x02: ['5002001901f4']
                },
                0x11: {
                    0x01: ['5101']
                    },
                0x27:{
                    0x01: ['6701193be6'],
                    0x02: ['6702']
                }
            },
        })
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send raw data rsp addr:1281, data:71 01 02 05 10 00 00 00 00",
                                                                                  "send stack raw data, addr:1281, data::11 01"], timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        reset_time = time.time()
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords="send stack raw data, addr:1281, data::10 02", timeout=60): 
            pass
        enter_boot_time = time.time()
        wait_time = enter_boot_time - reset_time
        logger.info(f"enter_boot_time:{enter_boot_time - reset_time}")
        logger.info(f"wait_time:{wait_time}")
        assert 5.5 < wait_time < 7 

    @pytest.mark.V3_0_0
    @pytest.mark.full
    @allure.title("常规ota_含CD升级成功_重启CD不响应") 
    def test_fota_caseid_1997072(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1281: {
                0x22: {
                    0xf1aa: ['62f1aa8895037286202043'],
                    0xf1ae: ['62f1ae016230310210204142'],
                    0xf186: ['62f18602'],
                    0xd01c: ['7f2222'],
                },
                0x31: {
                    0x010206: ['710102061001'],
                    0x01ff00: ['7101ff0010'],
                    0x010205: ['710102051000000000'],
                    0x01a100: ['7101a1001000'],
                    0x010212: ['710102121000'],
                },
                0x34: {
                    0x00: ['744000000802']
                },
                0x10: {
                    0x02: ['5002001901f4']
                },
                0x11: {
                    0x01: ['7f1122']
                    },
                0x27:{
                    0x01: ['6701193be6'],
                    0x02: ['6702']
                }
            },
        })
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1281, data::11 01",
                                                                                  'send raw data rsp addr:1281, data:7f 11 22'], timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", unexpect_keywords="send stack raw data, addr:1281, data::10 02", timeout=20): 
            pass   

    @pytest.mark.V3_0_0
    @pytest.mark.full
    @allure.title("常规ota_含CD升级失败_无重启流程") 
    def test_fota_caseid_1997071(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1281: {
                0x22: {
                    0xf1aa: ['62f1aa8895037286202043'],
                    0xf1ae: ['62f1ae016230310210204142'],
                    0xf186: ['62f18602'],
                    0xd01c: ['7f2222'],
                },
                0x31: {
                    0x010206: ['710102061001'],
                    0x01ff00: ['7101ff0010'],
                    0x010205: ['710102051000000000'],
                    0x01a100: ['7101a1001000'],
                    0x010212: ['7f3131'],
                },
                0x34: {
                    0x00: ['744000000802']
                },
                0x10: {
                    0x02: ['5002001901f4']
                },
                0x11: {
                    0x01: ['7f1122']
                    }, 
                0x27:{
                    0x01: ['6701193be6'],
                    0x02: ['6702']
                }
            },
        })
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='progress:95', timeout=900):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", unexpect_keywords="EcuResetByAddrCb:ecu addr:1281 ,req 11 01 ret", timeout=20): 
            pass 

if __name__ == "__main__":
    pass