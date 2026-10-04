import pytest
import allure
import pytest
import allure
from xat_cases.legacy.bgm.mcu.case_helper.test_abc_base import TestABCBase 
from xat_ecu.api.common.common import *


@pytest.mark.mcu_test
@allure.feature("BG车控车设/雨刮功能")
@allure.story("雨刮DID")
class Test_Switch(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # 读取ccp  方便后面进行恢复
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x06],recv=[0x62, 0xF1, 0x06])
        self.ccp_original_value = recv_data_list[3:1556 + 3]
        self.mix.write_vehicle_model_ccp(vehicle_model=VehicleType.Venus, vehicle_mca=VehicleMca.Mca_400v)
        self.soa.update(["WiperService_client","WTIService_client","OuterRearViewService_client"])
        sleep(1)
        self.soa.start_get_wiper_switch_sts()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location
        self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )  
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
         #解锁状态
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.io.set_five_door_sts(sts=Door.close)
        sleep(2)
        

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.set_hood_sts(HoodSts.Close)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0xA4,0x07])
        self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0xA4],recv=[0x62, 0x45, 0xA4,0x07])

    def after_class(self, ecu):
        # Code Location
        self.soa.stop_get_wiper_switch_sts()
        self.sd_tester.write_ccp_value(self.ccp_original_value)
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        super().after_class(self, ecu)
    
    def set_pre_condition_for_maintain_service(self, wash_func_sts: isOn, maintain_pos: isOn, wiper_mode: WiperMode,
                                               usage_mode: Union[UsageMode, None] = None,
                                               car_mode: Union[CarMode, None] = None, ccp: dict = {},time_wait = 1):
        self.mix.set_common_precontion(usage_mode=usage_mode, car_mode=car_mode, ccp=ccp)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, wash_func_sts)
        self.soa.hmi_set_wiper_maintaince_pos(maintain_pos)
        self.soa.hmi_set_wiper_mode(WiperPos.Front, wiper_mode)
        sleep(time_wait)

    def set_wiper_mode_and_read_did(self,mode,expect_value):
        self.soa.hmi_set_wiper_mode(WiperPos.Front,mode)
        self.bus_comm.check_wiper_mode_req(mode)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0X18],recv=expect_value)

    @pytest.mark.full
    def test_caseid_1987572(self):
        """
        Internal DID 控制WMM激活前洗涤(DID_420A)
        """
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x0A,0x03,0x00],recv=[0x6F, 0x42, 0X0A])
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0X0A],recv=[0x62, 0x42, 0X0A,0x00])
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",0)

        self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x0A,0x03,0x01],recv=[0x6F, 0x42, 0X0A])
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0X0A],recv=[0x62, 0x42, 0X0A,0x01])
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        
        self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x0A,0x03,0x02],recv=[0x6F, 0x42, 0X0A])
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0X0A],recv=[0x62,0x42, 0X0A,0x02])
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        
        self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x0A,0x03,0x03],recv=[0x6F, 0x42, 0X0A])
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0X0A],recv=[0x62, 0x42,0X0A,0X03])
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",3)
        
        self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x0A,0x00],recv=[0x6F, 0x42, 0X0A])
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0X0A],recv=[0x62, 0x42,0X0A,0X01])
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
    
    @allure.title("雨刷停止位状态")
    @pytest.mark.full
    def test_caseid_1987461(self):
        """
        Internal DID 雨刮停止位状态(DID_418F)
        """
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_singal("cem_lin1","WmmCem_Lin1Fr01", 'WiprInWipgArFromWMM', 0)
        self.bus_comm.set_singal("cem_lin1","WmmCem_Lin1Fr01", 'WiprInPrkgPosnLoFromWMM', 0)
        self.soa.get_and_event_check_wiper_return_pos(WiperPos.Front,isOn.On)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X8F],recv=[0x62, 0x41, 0X8F,0x01])

        self.bus_comm.set_singal("cem_lin1","WmmCem_Lin1Fr01", 'WiprInWipgArFromWMM', 0)
        self.bus_comm.set_singal("cem_lin1","WmmCem_Lin1Fr01", 'WiprInPrkgPosnLoFromWMM', 1)
        self.soa.get_and_event_check_wiper_return_pos(WiperPos.Front,isOn.Off)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X8F],recv=[0x62, 0x41, 0X8F,0x00])

        self.bus_comm.set_singal("cem_lin1","WmmCem_Lin1Fr01", 'WiprInWipgArFromWMM', 1)
        self.bus_comm.set_singal("cem_lin1","WmmCem_Lin1Fr01", 'WiprInPrkgPosnLoFromWMM', 0)
        self.soa.get_and_event_check_wiper_return_pos(WiperPos.Front,isOn.On)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X8F],recv=[0x62, 0x41, 0X8F,0x01])
       
        self.bus_comm.set_singal("cem_lin1","WmmCem_Lin1Fr01", 'WiprInWipgArFromWMM', 1)
        self.bus_comm.set_singal("cem_lin1","WmmCem_Lin1Fr01", 'WiprInPrkgPosnLoFromWMM', 1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X8F],recv=[0x62, 0x41, 0X8F,0x01])
    

    @pytest.mark.full
    def test_caseid_1987435(self):
        """
        Internal DID雨刮单次刮水(DID_4238)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x2F,0x43,0x28,0x03,0x01],recv=[0x6F, 0x43, 0X28])
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0X28],recv=[0x62, 0x43, 0X28,0X01])
        self.sd_tester.send_request_and_recv_response([0x2F,0x43,0x28,0x03,0x00],recv=[0x6F, 0x43, 0X28])
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",0)
        self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0X28],recv=[0x62, 0x43, 0X28,0X00])
        self.sd_tester.send_request_and_recv_response([0x2F,0x43,0x28,0x00],recv=[0x6F, 0x43, 0X28])
        self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0X28],recv=[0x62, 0x43, 0X28,0X00])
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",0)
        

    @pytest.mark.full
    def test_caseid_1987436(self):
        """
        Internal DID 前喷水继电器控制(DID_41E9)
        """
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x2F,0x41,0xE9,0x03,0x01],recv=[0x6F, 0x41, 0XE9])
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0XE9],recv=[0x62, 0x41, 0XE9,0x01])
        self.sd_tester.send_request_and_recv_response([0x2F,0x41,0xE9,0x03,0x00],recv=[0x6F, 0x41, 0XE9])
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0XE9],recv=[0x62, 0x41, 0XE9,0x00])
        self.sd_tester.send_request_and_recv_response([0x2F,0x41,0xE9,0x00],recv=[0x6F, 0x41, 0XE9])
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0XE9],recv=[0x62, 0x41, 0XE9,0x00])

    @allure.title("雨量传感器重新采用")
    @pytest.mark.full
    def test_caseid_1987437(self):
        """
        Internal DID 雨量传感器重新采用(DID_43B8)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x2F,0x43,0xB8,0x03,0x01],recv=[0x6F, 0x43, 0XB8])
        self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0XB8],recv=[0x62, 0x43, 0XB8,0x01])
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr03","ReAdaptReq",1)
        self.sd_tester.send_request_and_recv_response([0x2F,0x43,0xB8,0x03,0x00],recv=[0x6F, 0x43, 0XB8])
        self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0XB8],recv=[0x62, 0x43, 0XB8,0x00])
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr03","ReAdaptReq",0)
        self.sd_tester.send_request_and_recv_response([0x2F,0x43,0xB8,0x00],recv=[0x6F, 0x43, 0XB8])
        self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0XB8],recv=[0x62, 0x43, 0XB8,0x00])
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr03","ReAdaptReq",0)
    
        

    @pytest.mark.full
    def test_caseid_1987455(self):
        """
        Internal DID 雨水传感器高温检测(DID_4282)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03","RainSnsrDiagcRainSnsrHiTDetd",1)
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0X82],recv=[0x62, 0x42, 0X82,0x01])
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03","RainSnsrDiagcRainSnsrHiTDetd",0)
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0X82],recv=[0x62, 0x42, 0X82,0x00])


    @pytest.mark.full
    def test_caseid_1987462(self):
        """
        Internal DID 反向用例-雨水传感器高温检测(DID_4282)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03","RainSnsrDiagcRainSnsrHiTDetd",1)
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0X82],recv=[0x62, 0x42, 0X82,0x00])
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03","RainSnsrDiagcRainSnsrHiTDetd",0)
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0X82],recv=[0x62, 0x42, 0X82,0x00])


    @pytest.mark.full
    def test_caseid_1987456(self):
        """
        Internal DID 雨水传感器高压检测(DID_4283)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03","RainSnsrDiagcRainSnsrHiVoltDetd",1)
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0X83],recv=[0x62, 0x42, 0X83,0x01])
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03","RainSnsrDiagcRainSnsrHiVoltDetd",0)
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0X83],recv=[0x62, 0x42, 0X83,0x00])


    @pytest.mark.full
    def test_caseid_1987463(self):
        """
        Internal DID 反向用例-雨水传感器高压检测(DID_4283)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03","RainSnsrDiagcRainSnsrHiVoltDetd",1)
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0X83],recv=[0x62, 0x42, 0X83,0x00])
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03","RainSnsrDiagcRainSnsrHiVoltDetd",0)
        sleep(2)
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0X83],recv=[0x62, 0x42, 0X83,0x00])


    @pytest.mark.full
    def test_caseid_1987457(self):
        """
        Internal DID 雨刮电机通信错误检测(DID_430B)
        """
        self.sd_tester.write_ccp({503:0x02})
        for i in [UsageMode.DRIVING,UsageMode.ACTIVE]:
            self.mix.set_common_precontion(usage_mode=i, car_mode=CarMode.NORMAL )  
            self.bus_comm.set_vehspd_gear(vehspd=3.0)
            self.bus_comm.stop_send_pdu("cem_lin1","WmmCem_Lin1Fr01")
            sleep(5)
            self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0X0B],recv=[0x62, 0x43,0x0B,0x01])
            self.bus_comm.resume_send_pdu("cem_lin1","WmmCem_Lin1Fr01")
            sleep(5)
            self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0X0B],recv=[0x62, 0x43,0x0B,0x00])

    @pytest.mark.full
    def test_caseid_1987460(self):
        """
        Internal DID 反向用例-雨刮电机通信错误检测(DID_430B)
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL )  
        self.bus_comm.stop_send_pdu("cem_lin1","WmmCem_Lin1Fr01")
        sleep(5)
        self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0X0B],recv=[0x62, 0x43,0x0B,0x00])
        self.bus_comm.resume_send_pdu("cem_lin1","WmmCem_Lin1Fr01")
        sleep(5)
        self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0X0B],recv=[0x62, 0x43,0x0B,0x00])

    @pytest.mark.full
    def test_caseid_1987458(self):
        """
        Internal DID 雨刮电机节点错误检测(DID_430C)
        """
        for i in [UsageMode.DRIVING,UsageMode.ACTIVE]:
            self.mix.set_common_precontion(usage_mode=i, car_mode=CarMode.NORMAL)  
            self.bus_comm.set_vehspd_gear(vehspd=3.0)
            self.bus_comm.stop_send_pdu("cem_lin1","WmmCem_Lin1Fr01")
            sleep(5)
            self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0X0C],recv=[0x62, 0x43,0x0C,0x01])
            self.bus_comm.resume_send_pdu("cem_lin1","WmmCem_Lin1Fr01")
            sleep(5)
            self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0X0C],recv=[0x62, 0x43,0x0C,0x00])


    @pytest.mark.full
    def test_caseid_1987459(self):
        """
        Internal DID 反向用例-雨刮电机节点错误检测(DID_430C)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL )  
        self.bus_comm.stop_send_pdu("cem_lin1","WmmCem_Lin1Fr01")
        sleep(5)
        self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0X0C],recv=[0x62, 0x43,0x0C,0x00])
        self.bus_comm.resume_send_pdu("cem_lin1","WmmCem_Lin1Fr01")
        sleep(5)
        self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0X0C],recv=[0x62, 0x43,0x0C,0x00])

    @pytest.mark.full
    def test_wiper_caseid_1987568(self):
       """
       Internal DID 雨量传感器阈值(DID_45A4)
       """
       self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL )  
       self.bus_comm.set_vehspd_gear(vehspd=3.0)
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0XA4],recv=[0x62, 0x45,0xA4,0x07])
       self.bus_comm.check("cem_lin1","CemCem_Lin1Fr04","RainSnsrLiThd",7)
       self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
       #写入随机值
       write_rain_list = [random.randint(0, 15)]
       self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0xA4], write_rain_list)
       #检查写入的值
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0xA4],recv=[0x62, 0x45, 0xA4] + write_rain_list)
       self.bus_comm.check("cem_lin1","CemCem_Lin1Fr04","RainSnsrLiThd",write_rain_list[0])
       #写入超范围值
       self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0xA4,0x10])
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0xA4],recv=[0x62, 0x45,0xA4,0x00])
       self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0xA4,0x07])
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0xA4],recv=[0x62, 0x45, 0xA4,0x07])


    @pytest.mark.full
    def test_wiper_caseid_1994502(self):
       """
       Internal DID 诊断重启后，检查雨量传感器阈值(DID_45A4)
       """
       self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL )  
       self.bus_comm.set_vehspd_gear(vehspd=3.0)
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0XA4],recv=[0x62, 0x45,0xA4,0x07])
       self.bus_comm.check("cem_lin1","CemCem_Lin1Fr04","RainSnsrLiThd",7)
       self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
       #写入随机值
       write_rain_list = [random.randint(0, 15)]
       self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0xA4], write_rain_list)
       self.sd_tester.reset_bgm()
       #检查写入的值
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0xA4],recv=[0x62, 0x45, 0xA4] + write_rain_list)
       self.bus_comm.check("cem_lin1","CemCem_Lin1Fr04","RainSnsrLiThd",write_rain_list[0])
       #写入超范围值
       self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
       self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0xA4,0x10])
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0xA4],recv=[0x62, 0x45,0xA4,0x00])
       self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0xA4,0x07])
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0xA4],recv=[0x62, 0x45, 0xA4,0x07])


    @pytest.mark.full
    @pytest.mark.nvm
    def test_wiper_caseid_1994504(self):
       """
       Internal DID 断电上电后，检查雨量传感器阈值(DID_45A4)
       """
       self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL )  
       self.bus_comm.set_vehspd_gear(vehspd=3.0)
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0XA4],recv=[0x62, 0x45,0xA4,0x07])
       self.bus_comm.check("cem_lin1","CemCem_Lin1Fr04","RainSnsrLiThd",7)
       self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
       #写入随机值
       write_rain_list = [random.randint(0, 15)]
       self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0xA4], write_rain_list)
       self.io.bgm_power_off()
       self.io.bgm_power_on()
       sleep(15)
       #检查写入的值
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0xA4],recv=[0x62, 0x45, 0xA4] + write_rain_list)
       self.bus_comm.check("cem_lin1","CemCem_Lin1Fr04","RainSnsrLiThd",write_rain_list[0])
       #写入超范围值
       self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
       self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0xA4,0x10])
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0xA4],recv=[0x62, 0x45,0xA4,0x00])
       self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0xA4,0x07])
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0xA4],recv=[0x62, 0x45, 0xA4,0x07])
    
    @pytest.mark.full
    def test_caseid_1987569(self):
        """
        Internal DID 车窗短降(DID_45BF)
        """
        self.sd_tester.write_ccp({561:0x02})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0XBF],recv=[0x62, 0x45,0xBF,0x01])


    @pytest.mark.full
    def test_caseid_1987451(self):
        """
        Internal DID 从CDC来的雨刮挡位信息(DID_4218)
        """
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.On,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.set_wiper_mode_and_read_did(WiperMode.Off,[0x62, 0x42, 0X18,0x00])
        self.set_wiper_mode_and_read_did(WiperMode.IntLow,[0x62, 0x42, 0X18,0x02])
        self.set_wiper_mode_and_read_did(WiperMode.IntHigh,[0x62, 0x42, 0X18,0x03])
        self.set_wiper_mode_and_read_did(WiperMode.Low,[0x62, 0x42, 0X18,0x04])
        self.set_wiper_mode_and_read_did(WiperMode.High,[0x62, 0x42, 0X18,0x05])
        self.set_wiper_mode_and_read_did(WiperMode.Auto,[0x62, 0x42, 0X18,0x06])
        self.set_wiper_mode_and_read_did(WiperMode.Error,[0x62, 0x42, 0X18,0x07])

    @pytest.mark.full
    @pytest.mark.nvm
    def test_wiper_caseid_1994503(self):
       """
       Internal DID 休眠唤醒后，检查雨量传感器阈值(DID_45A4)
       """
       self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL )  
       self.bus_comm.set_vehspd_gear(vehspd=3.0)
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0XA4],recv=[0x62, 0x45,0xA4,0x07])
       self.bus_comm.check("cem_lin1","CemCem_Lin1Fr04","RainSnsrLiThd",7)
       self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
       #写入随机值
       write_rain_list = [random.randint(0, 15)]
       self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0xA4], write_rain_list)
       self.bus_comm.set_vehspd_gear(vehspd=0.0)
       sleep(1.5)
       self.mix.network_sleep()
       self.io.set_door(Drvr=Door.open)
       self.sd_tester.sd_tester.tester_present()
       self.bus_comm.resume_all_bus_send()
       self.bus_comm.set_vehspd_gear(vehspd=3.0)
       #检查写入的值
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0xA4],recv=[0x62, 0x45, 0xA4] + write_rain_list)
       self.bus_comm.check("cem_lin1","CemCem_Lin1Fr04","RainSnsrLiThd",write_rain_list[0])
       #写入超范围值
       self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
       self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0xA4,0x10])
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0xA4],recv=[0x62, 0x45,0xA4,0x00])
       self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0xA4,0x07])
       self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0xA4],recv=[0x62, 0x45, 0xA4,0x07])
       self.io.bgm_diag_line_up()
       logger.info(f'诊断激活线连接')
       self.io.tcam_kl15_up()
       sleep(5)  # 诊断激活线5s钟变为连接状态

