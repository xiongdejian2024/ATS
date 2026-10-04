import os
import sys
import time
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_cases.legacy.basetech.case_helper.diag_case_helper.DiagTestBase import *
from xat_ecu.api.abc_interface import *


@allure.feature("性能稳定性/四域重启")
class TestDomainReSet(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.bus_comm.wakeup_tcam_by_can()

    def after_each_func(self, ecu):
        self.bus_comm.stop_wakeup_tcam_by_can()
        sleep(10)
        super().after_each_func(ecu)

    @pytest.mark.smoke
    def test_caseid_1986549(self):
        with allure.step("TCAM通过can信号重启_02超时"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,5)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)     
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3

    @pytest.mark.Sanity
    def test_caseid_1986566(self):
        with allure.step("TCAM通过can信号重启_信号不完整"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)        
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3

    @pytest.mark.Sanity
    def test_caseid_1986563(self):
        with allure.step("TCAM通过can信号重启顺序错误_132"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3

    @pytest.mark.Sanity
    def test_caseid_1986558(self):
        with allure.step("TCAM通过can信号重启_信号不完整_11"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)         
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3


    @pytest.mark.Full
    def test_caseid_1986565(self):
        with allure.step("TCAM通过can信号重启_信号不完整02"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)            
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01) 
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3

    @pytest.mark.Full
    def test_caseid_1986564(self):
        with allure.step("TCAM通过can信号重启_信号不完整03"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)  
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3

    @pytest.mark.Full
    def test_caseid_1986562(self):
        with allure.step("TCAM通过can信号重启顺序错误_213"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01) 
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3  

    @pytest.mark.Full
    def test_caseid_1986561(self):
        with allure.step("TCAM通过can信号重启顺序错误_231"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3   

    @pytest.mark.Full
    def test_caseid_1986560(self):
        with allure.step("TCAM通过can信号重启顺序错误_312"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3 

    @pytest.mark.Full
    def test_caseid_1986559(self):
        with allure.step("TCAM通过can信号重启顺序错误_321"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3

    @pytest.mark.Full
    def test_caseid_1986557(self):
        with allure.step("TCAM通过can信号重启_信号不完整_12"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)   
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3

    @pytest.mark.Full
    def test_caseid_1986556(self):
        with allure.step("TCAM通过can信号重启_信号不完整_13"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)  
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3 

    @pytest.mark.Full
    def test_caseid_1986555(self):
        with allure.step("TCAM通过can信号重启_信号不完整_21"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)  
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3

    @pytest.mark.Full
    def test_caseid_1986554(self):
        with allure.step("TCAM通过can信号重启_信号不完整_22"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01) 
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3

    @pytest.mark.Full
    def test_caseid_1986553(self):
        with allure.step("TCAM通过can信号重启_信号不完整_23"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)   
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3                       
                                   
    @pytest.mark.Full
    def test_caseid_1986552(self):
        with allure.step("TCAM通过can信号重启_信号不完整_31"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)   
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3  

    @pytest.mark.Full
    def test_caseid_1986551(self):
        with allure.step("TCAM通过can信号重启_信号不完整_32"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)   
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3                                            

    @pytest.mark.Full
    def test_caseid_1986550(self):
        with allure.step("TCAM通过can信号重启_信号不完整_33"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)    
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3

    @pytest.mark.Full
    def test_caseid_1986548(self):
        with allure.step("TCAM通过can信号重启_03超时"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,5)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)    
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() > 3

    @pytest.mark.smoke
    def test_caseid_1986567(self):
        with allure.step("发送can信号重启TCAM"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() <= 3


    @pytest.mark.smoke
    def test_caseid_1986545(self):
        with allure.step("TCAM通过can信号重启_多帧信号01_01"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() <= 3

    @pytest.mark.Sanity
    def test_caseid_1986547(self):
        with allure.step("TCAM通过can信号重启_02超时重新计时"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,5)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)          
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() <= 3

    @pytest.mark.Sanity
    def test_caseid_1986544(self):
        with allure.step("TCAM通过can信号重启_多帧信号01-02"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)   
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() <= 3

    @pytest.mark.Full
    def test_caseid_1986546(self):
        with allure.step("TCAM通过can信号重启_03超时重新计时"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,5)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)    
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() <= 3

    @pytest.mark.Full
    def test_caseid_1986543(self):
        with allure.step("TCAM通过can信号重启_多帧信号01-03"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)    
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() <= 3

    @pytest.mark.Full
    def test_caseid_1986542(self):
        with allure.step("TCAM通过can信号重启_多帧信号02-01"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)     
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() <= 3

    @pytest.mark.Full
    def test_caseid_1986541(self):
        with allure.step("TCAM通过can信号重启_多帧信号02-02"):
            self.bus_comm.preheat_msg("connectivitycanfd", "BgmConnectivityFr22")
            sleep(2)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAM_UB',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte0',82,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',1,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',2,0.01)
            self.bus_comm.four_domain_restart_send_signal('BGMMPUCtrlTCAMByte1',3,0.01)
            time.sleep(180)
            assert self.ssh.get_tcam_uptime() <= 3