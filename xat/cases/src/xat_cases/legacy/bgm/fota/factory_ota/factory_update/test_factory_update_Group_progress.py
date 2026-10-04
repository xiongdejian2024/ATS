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
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.cdc_acu_doip_check])
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
        self.mix.set_car_mode(car_mode=CarMode.FACTORY)
        self.ssh.copy_factory_packages()  
        self.ssh.clear_fota_cache()
        self.sd_tester.reset_bgm()
        self.mix.set_factory_ota_condition(display_hv_soc=250,low_volt_power=11.5,local_diag_sts=DiagActLineSts.DisActive)

                    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.mix.fota_back_to_idle()
        
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.server_mock.doip_sock_obj.tcp_server_sock.stop()
        self.ssh.type_commands(DeviceName.BGM,"cd /data;/app/bin/swdl -nw 10 0;sync")
        self.ssh.type_commands(DeviceName.BGM,"cd /data;rm debug_script_executed_count;rm -rf debug.sh;sync")

    @pytest.mark.V2_2_0
    @pytest.mark.full
    @allure.title("V2.2_intelligent_ECU_update && Tag:LV_ECU _检查Doip ACU CDC 连接失败") 
    def test_fota_caseid_1995490(self):
        try:
            self.ssh.type_commands(DeviceName.BGM,"rm -rf /update/skip_debug;sync")
            self.sd_tester.reset_bgm()
            self.server_mock.clear_mock_data_0x8001()
            self.server_mock.doip_update_service_data_0x8001({
                    0x1444: {
                        0x22: {
                            0xf1aa: ['62f1aa8895036232202043'],
                            0xf1ae: ['62f1ae016120410110204142']
                        }
                    },
                    0x1281: {
                        0x22: {
                            0xf1aa: ['62f1aa8895037286202043'],
                            0xf1ae: ['62f1ae016230310110204142']
                        }
                    },
                })
            with self.log_manage.check_jetlog_by_keywords(log_type=' fota:', keywords='ColEcuVersion:ObtAdaptor, ready call ColVersionInfo', timeout=300):
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            sleep(300) #等待版本收集结束
            with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='" fota:"', keywords=['CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                            'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                            'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                            'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                            'CheckAllDomainsDoIpConnectionCb:result:0, retry count:0'
                                                                                                            ], timeout=130):
                pass       
            with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='" fota:"', keywords=['upgrade_manage => domain_ecu_upgrade',
                                                                                                            'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                            'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                            'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                            'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                            'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                            'CheckAllDomainsDoIpConnectionCb:result:0, retry count:0'
                                                                                                            ], timeout=180):
                pass  
            self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=1500)
        finally:
            self.ssh.update_skip_debug([FOTA_Skip_Debug.cdc_acu_doip_check])

    @pytest.mark.V3_0_0
    @pytest.mark.smoke
    @allure.title("厂内ota_含CD升级成功_正向流程") 
    def test_fota_caseid_1997076(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1281: {
                0x22: {
                    0xf1aa: ['62f1aa8895037286202043'],
                    0xf1ae: ['62f1ae016230310110204141'],
                    0xf186: ['62f18602'],
                    0xd01c: ['7f2222'],
                },
                0x31: {
                    0x01ff00: ['7101ff0010'],
                    0x010205: ['710102051000000000'],
                    0x01a100: ['7101a1001000'],
                    0x010212: ['710102121000'],
                },
                0x34: {
                    0x00: ['744000000400']
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
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords="send stack raw data, addr:1281, data::11 01", timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        reset_time = time.time()    
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords="send stack raw data, addr:1281, data::10 02", timeout=60): 
            pass
        enter_boot_time = time.time()
        wait_time = enter_boot_time - reset_time
        assert 5 < wait_time < 7 

    @pytest.mark.V3_0_0
    @pytest.mark.full
    @allure.title("厂内ota_含CD升级成功_重启CD不响应") 
    def test_fota_caseid_1997075(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1281: {
                0x22: {
                    0xf1aa: ['62f1aa8895037286202043'],
                    0xf1ae: ['62f1ae016230310110204141'],
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
                    0x00: ['744000000400']
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
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1281, data::11 01",
                                                                                  'send raw data rsp addr:1281, data:7f 11 22'], timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", unexpect_keywords="send stack raw data, addr:1281, data::10 02", timeout=20): 
            pass   

    @pytest.mark.V3_0_0
    @pytest.mark.full
    @allure.title("厂内ota_含CD升级失败_无重启流程") 
    def test_fota_caseid_1997074(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1281: {
                0x22: {
                    0xf1aa: ['62f1aa8895037286202043'],
                    0xf1ae: ['62f1ae016230310110204141'],
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
                    0x00: ['744000000400']
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
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='progress:95', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", unexpect_keywords="EcuResetByAddrCb:ecu addr:1281 ,req 11 01 ret", timeout=20): 
            pass 
if __name__ == "__main__":
    pass





