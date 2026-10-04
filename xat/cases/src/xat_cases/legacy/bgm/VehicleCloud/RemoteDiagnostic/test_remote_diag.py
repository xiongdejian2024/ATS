import os
import sys
import pytest
import allure
import re
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@pytest.mark.remotediagfull
@allure.feature("基础架构")
@allure.story("remote_diag")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update(["VehicleModeService_client", "ObtDiagService_client","KeyService_client"])
        self.tsp.get_remote_diag_token()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)
        sleep(5)#等待TSP处理，避免异常
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.ssh.set_airplane_mode(isOn.Off)
        self.io.bgm_diag_line_up()
       
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.sanity
    @allure.title("远程诊断_无云配置参数 _本地触发充电口盖标定远程诊断上报结果")
    def test_remote_diag_caseid_1993178(self):
        self.ssh.set_airplane_mode(isOn.On)
        # self.ssh.type_commands(DeviceName.BGM,"rm -rf /data/persistent/config_*;sync;rm -rf /data/config_service/remoteDiag/;sync")
        # time.sleep(2) #此步骤会删除云配置本地数据库,历史配置数据将无法恢复，需重新下发，慎用
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=True)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(ID=255, status=calibration_status.kIdle)
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['"触发源:Screen',
                                                                                  "功能名称：充电口盖标定",
                                                                                  'http upload success'],timeout=60):    
            pass


    @pytest.mark.smoke
    @allure.title("远程诊断_远程诊断触发充电口盖标定和结果上报")
    def test_remote_diag_caseid_1989452(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):    
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen,session_time_out=600)
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['"触发源:RemoteDiag',
                                                                                  "功能名称：充电口盖标定",
                                                                                  'http upload success'],timeout=60):    
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_cali)

    @pytest.mark.smoke
    @allure.title("开启远程诊断会话_条件检测满足")
    def test_remote_diag_caseid_1980898(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}',
                                                                                  'sig 1 remote session is open:true'],timeout=20):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)    
    
    @pytest.mark.full
    @allure.title("开启远程诊断会话_条件检测诊断仲裁不满足")
    def test_remote_diag_caseid_1980897(self):
        self.io.bgm_diag_line_up()
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords='cmd:1 para:{"code":1, "msg":"Arb Fail"}',timeout=20):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen) 

    @pytest.mark.full
    @allure.title("开启远程诊断会话_条件检测诊断车速不满足")
    def test_remote_diag_caseid_1980896(self):
        self.bus_comm.set_vehspd_gear(vehspd=10000)
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":1,"msg":"Speed Check NG"}',
                                                                                  'sig 1 remote session is open:false'],timeout=20):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)

    @pytest.mark.sanity
    @allure.title("开启远程诊断会话_默认时间300s")
    def test_remote_diag_caseid_1980895(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:2 para:{"code":0, "msg":"Timeout"}',
                                                                                  'sig 1 remote session is open:false'],timeout=305):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)  

    @pytest.mark.sanity
    @allure.title("开启远程诊断会话_会话定时器设定功能")
    def test_remote_diag_caseid_1980894(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:2 para:{"code":0, "msg":"Timeout"}',
                                                                                  'sig 1 remote session is open:false'],timeout=105):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen,session_time_out=100)               

    @pytest.mark.sanity
    @allure.title("开启远程诊断会话_周期检测车速周期设定功能")
    def test_remote_diag_caseid_1980893(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['sig 2 vehicle speed:0.000000'],timeout=30):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen,check_intervel=5)
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['sig 2 vehicle speed:39.099998'],timeout=30):
            self.bus_comm.set_vehspd_gear(vehspd=10000)

    @pytest.mark.full
    @allure.title("本地结束远程会话_定时器超时")
    def test_remote_diag_caseid_1980892(self):
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen,session_time_out=10)
        time.sleep(15) #等待会话超时结束log打印完整
        jet_log = self.ssh.type_commands(DeviceName.BGM,"/app/bin/zstdcat /log/jetlog_messages |grep -E ' RM_DIAG_V2T:| LUA_Uploader:' | tail -n 200")
        opentaskid= re.findall(r'Parse OK, task id:(.*?), version:010101, cmd:1', jet_log, re.S)[-1]
        closdtaskid = re.findall(r'UploadRemoteSessionResult start, task_id:(.\w+) cmd:2 para:{"code":0, "msg":"Timeout"}', jet_log, re.S)[-1]
        assert opentaskid == closdtaskid

    @pytest.mark.full
    @allure.title("本地结束远程会话_本地OBT连接断开_诊断激活线")
    def test_remote_diag_caseid_1980890(self):
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)
        time.sleep(3) #等待会话开启完成
        self.io.bgm_diag_line_up()
        time.sleep(5) #等待log打印完整
        jet_log = self.ssh.type_commands(DeviceName.BGM,"/app/bin/zstdcat /log/jetlog_messages |grep -E ' RM_DIAG_V2T:| LUA_Uploader:' | tail -n 200")
        opentaskid= re.findall(r'Parse OK, task id:(.*?), version:010101, cmd:1', jet_log, re.S)[-1]
        closdtaskid = re.findall(r'UploadRemoteSessionResult start, task_id:(.\w+) cmd:2 para:{"code":0, "msg":"Arb Release"}', jet_log, re.S)[-1]
        assert opentaskid == closdtaskid 
   
    @pytest.mark.full
    @allure.title("本地结束远程会话_车速不满足")
    def test_remote_diag_caseid_1980889(self):
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)
        time.sleep(3) #等待会话开启完成
        self.bus_comm.set_vehspd_gear(vehspd=10000)
        time.sleep(5) #等待log打印完整
        jet_log = self.ssh.type_commands(DeviceName.BGM,"/app/bin/zstdcat /log/jetlog_messages |grep -E ' RM_DIAG_V2T:| LUA_Uploader:' | tail -n 200")
        opentaskid= re.findall(r'Parse OK, task id:(.*?), version:010101, cmd:1', jet_log, re.S)[-1]
        closdtaskid = re.findall(r'UploadRemoteSessionResult start, task_id:(.\w+) cmd:2 para:{"code":1,"msg":"Speed Check NG"}', jet_log, re.S)[-1]
        assert opentaskid == closdtaskid 

    @pytest.mark.full
    @allure.title("本地结束远程会话_本地会话结束_不执行远程诊断序列任务")
    def test_remote_diag_caseid_1980888(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)    
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=[':CloseSession','cmd:2 para:{"code":1,"msg":"Speed Check NG"}'],timeout=30):
            self.bus_comm.set_vehspd_gear(vehspd=10000)
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", unexpect_keywords='version:010101, cmd:3',timeout=30):
           self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_22_P0_DID) 

    @pytest.mark.full
    @allure.title("本地结束远程会话_本地会话结束_中断执行远程诊断序列任务")
    def test_remote_diag_caseid_1980887(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_22_P2_DID)
        time.sleep(5) #等待诊断序列执行以下在打断      
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords='":2}","respCode":',timeout=60):
            self.bus_comm.set_vehspd_gear(vehspd=10000)

    @pytest.mark.sanity
    @allure.title("关闭远程会话_断开OBT释放诊断仲裁")
    def test_remote_diag_caseid_1980886(self):
        with self.log_manage.check_jetlog_by_keywords(log_type="ARB", keywords='Arbitrateing: remote diag',timeout=60):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)
        with self.log_manage.check_jetlog_by_keywords(log_type="ARB", keywords='Release remote diag',timeout=60):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)          

    @pytest.mark.smoke
    @allure.title("关闭远程会话_关闭结果上报")
    def test_remote_diag_caseid_1980885(self):
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['CloseSession','cmd:2 para:{"code":0}'],timeout=60):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)

    @pytest.mark.full
    @allure.title("关闭远程会话_中断执行中的诊断序列任务")
    def test_remote_diag_caseid_1980884(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_22_P0_DID)     
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords='":2}","respCode":',timeout=60):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)

    @pytest.mark.sanity
    @allure.title("执行远程诊断序列_单个诊断序列重置计时器")
    def test_remote_diag_caseid_1980883(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen,session_time_out=30)
        time.sleep(20) #等待20s后下发诊断指令重置计时器
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_22_P1_DID)     
        time.sleep(20) #验证计时器是否被重置
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords='cmd:2 para:{"code":0, "msg":"Timeout"}',timeout=60):
            pass

    @pytest.mark.full
    @allure.title("执行远程诊断序列_多个诊断序列重置计时器")
    def test_remote_diag_caseid_1980882(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen,session_time_out=30)
        time.sleep(20) #等待20s后下发诊断指令重置计时器
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_22_P1_DID)     
        time.sleep(20) #验证计时器是否被重置
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_22_P1_DID)
        time.sleep(20) #验证计时器是否被重置
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords='cmd:2 para:{"code":0, "msg":"Timeout"}',timeout=60):
            pass  

    @pytest.mark.full
    @allure.title("执行远程诊断序列_诊断序列任务上报超时重试")
    def test_remote_diag_caseid_1980881(self):
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_22_P1_DID)
        time.sleep(3)#避免诊断指令下发失败
        self.ssh.set_airplane_mode(isOn.On)   
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['UploadRemoteDiagResult return:false',
                                                                                  'UploadRemoteDiagResult return:false',
                                                                                  'UploadRemoteDiagResult return:false',
                                                                                  'UploadRemoteDiagResult return:false'],timeout=100):
            pass
        self.ssh.set_airplane_mode(isOn.Off)
        time.sleep(30)#等待飞行模式关闭后，重新上报结束会话
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)

    @pytest.mark.smoke
    @allure.title("可执行的UDS诊断服务范围定义_服务支持22_P0 DID")
    def test_remote_diag_caseid_1980880(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):    
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen,session_time_out=600)
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_22_P0_DID)
        self.mix.check_remote_diag_results(CheckRemoteDiagRes.CheckRemoteDiagRes_22_P0_DID)

    @pytest.mark.smoke
    @allure.title("可执行的UDS诊断服务范围定义_服务支持22_P1 DID")
    def test_remote_diag_caseid_1986484(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):    
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen,session_time_out=600)   
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_22_P1_DID)
        self.mix.check_remote_diag_results(CheckRemoteDiagRes.CheckRemoteDiagRes_22_P1_DID)

    @pytest.mark.full
    @allure.title("可执行的UDS诊断服务范围定义_服务支持22_P2 DID")
    def test_remote_diag_caseid_1986485(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):    
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen,session_time_out=600)   
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_22_P2_DID)
        self.mix.check_remote_diag_results(CheckRemoteDiagRes.CheckRemoteDiagRes_22_P2_DID)

    @pytest.mark.smoke
    @allure.title("可执行的UDS诊断服务范围定义_服务支持14")
    def test_remote_diag_caseid_1980876(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):    
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)   
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_14)
        self.mix.check_remote_diag_results(CheckRemoteDiagRes.CheckRemoteDiagRes_14)

    @pytest.mark.smoke
    @allure.title("可执行的UDS诊断服务范围定义_服务支持3E")
    def test_remote_diag_caseid_1980874(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):    
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)    
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_3E)
        self.mix.check_remote_diag_results(CheckRemoteDiagRes.CheckRemoteDiagRes_3E)        

    @pytest.mark.smoke
    @allure.title("可执行的UDS诊断服务范围定义_服务支持19")
    def test_remote_diag_caseid_1987380(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):    
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)    
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_19)
        self.mix.check_remote_diag_results(CheckRemoteDiagRes.CheckRemoteDiagRes_19)

    @pytest.mark.full
    @allure.title("下发不支持的诊断指令_1002、1003、1101")
    def test_remote_diag_caseid_1987381(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):    
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)       
        with self.log_manage.check_jetlog_by_keywords(log_type=" diag_client:", unexpect_keywords=['tx 1001:10 02','tx 1001:10 03','tx 1001:10 01',
                                                                                          'tx 1002:10 02','tx 1002:10 03','tx 1002:10 01',],timeout=60):
           self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_10_11)

    @pytest.mark.full
    @allure.title("远程诊断序列执行中_会话超时关闭")
    def test_remote_diag_caseid_1980870(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):    
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen,session_time_out=10)   
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:2 para:{"code":0, "msg":"Timeout"}',':2}","respCode":'],timeout=100):
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_22_P2_DID)

    # @pytest.mark.sanity
    # @allure.title("休眠场景_远程诊断会话开启")
    # def test_remote_diag_caseid_1985638(self):
    #     self.mix.network_sleep()
    #     self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen)
    #     time.sleep(30) #等待远程诊断任务唤醒整车
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords='sig 1 remote session is open:true',timeout=60):
    #         pass
    #     self.mix.network_wakeup()
              
if __name__ == "__main__":
    pass
