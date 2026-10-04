import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.constants.common import *


@allure.feature("车身网关测试/基础架构")
@allure.story("整车模式/车辆模式")
class TestChangeCarModeNot(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update(["VehicleModeService_client","CentralLockService_client"])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.bus_comm.set_vehspd(0.0)
        self.bus_comm.set_vehmtn()
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.mix.set_car_mode(CarMode.NORMAL)
        sleep(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
        super().after_class(self, ecu)

    @pytest.fixture(scope="function")
    def set_lock(self):
        self.bus_comm.check_car_mode_status(CarMode.NORMAL,car_mode_sub=0)     
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC) 
        yield
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC) 

    @pytest.fixture(scope="function")
    def set_lock_TrigSrc(self):     
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC) 
        yield
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.mix.set_car_mode(CarMode.NORMAL)       
        sleep(15)  
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC) 
    
    @pytest.fixture(scope="function")
    def set_unlock_TrigSrc(self):     
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC) 
        yield
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.mix.set_car_mode(CarMode.NORMAL)       
        sleep(15)  

    @pytest.fixture(scope="function")
    def set_driving_lock(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC) 
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        yield
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC) 

    @pytest.fixture(scope="function")
    def set_driving_unlock(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC) 
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        
    @pytest.mark.usefixtures("set_lock")
    @pytest.mark.full
    def test_car_mode_caseid_110084(self):
        '''
        normal to dyno
           1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt != 0 AlrmSt_Disarmd
        '''
        self.bus_comm.check_alrm_sts_req(alrm_sts=AlrmSts.Armd)
        self.sd_tester.change_car_mode(CarMode.DYNO)
        
    @pytest.mark.usefixtures("set_driving_lock")
    @pytest.mark.full
    def test_car_mode_caseid_110053(self):
        '''
        normal to factory
           1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  == 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt != 0 AlrmSt_Disarmd
        '''
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.Ukwn)
        self.mix.diag_not_change_car_mode(2)
    
    @pytest.mark.usefixtures("set_driving_lock")
    @pytest.mark.full
    def test_car_mode_caseid_110013(self):
        '''
        normal not to factory
           1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  == 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt != 0 AlrmSt_Disarmd
        '''   
        self.mix.diag_not_change_car_mode(2)

    @pytest.mark.usefixtures("set_lock")
    @pytest.mark.full
    def test_car_mode_caseid_109970(self):
        '''
        normal not to transport
           1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt != 0 AlrmSt_Disarmd
        '''
        self.mix.diag_not_change_car_mode(1)

    @pytest.mark.usefixtures("set_driving_lock")
    @pytest.mark.full
    def test_car_mode_caseid_109938(self):
        '''
        normal to transport
           1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  == 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1 == 0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt != 0 AlrmSt_Disarmd
        '''
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.Ukwn)
        self.mix.diag_not_change_car_mode(1)

    @pytest.mark.usefixtures("set_lock_TrigSrc")
    @pytest.mark.full
    @pytest.mark.carmode
    def test_car_mode_caseid_109924(self):
        '''
        normal to crash
          1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt != 0 AlrmSt_Disarmd
        '''
        self.bus_comm.check_alrm_sts_req(alrm_sts=AlrmSts.Armd)
        self.sd_tester.change_car_mode(CarMode.CRASH)
    
    @pytest.mark.usefixtures("set_driving_unlock")
    @pytest.mark.full
    def test_car_mode_caseid_110010(self):
        '''
        normal not to transport
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  == 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        ''' 
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.Ukwn)
        time.sleep(.3)
        self.mix.diag_not_change_car_mode(1)

    @pytest.mark.usefixtures("set_driving_unlock")
    @pytest.mark.full
    def test_car_mode_caseid_110142(self):
        '''
        normal not to factory
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  == 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.Ukwn)
        time.sleep(.3)
        self.mix.diag_not_change_car_mode(2)

    @pytest.mark.usefixtures("set_driving_unlock")
    @pytest.mark.full
    def test_car_mode_caseid_109969(self):
        '''
        normal not to dyno
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  == 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.mix.diag_not_change_car_mode(5)
    
    @pytest.mark.usefixtures("set_driving_unlock")
    @pytest.mark.full
    def test_car_mode_caseid_109961(self):
        '''
        normal not to factory
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  == 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.mix.diag_not_change_car_mode(2)
    
    @pytest.mark.usefixtures("set_driving_unlock")
    @pytest.mark.full
    def test_car_mode_caseid_109948(self):
        '''
        normal to crash
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  == 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.Ukwn)
        self.mix.diag_not_change_car_mode(3)
    
    @pytest.mark.usefixtures("set_driving_unlock")
    @pytest.mark.full
    def test_car_mode_caseid_110080(self):
        '''
        normal to dyno
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  == 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.Ukwn)
        self.mix.diag_not_change_car_mode(5)
    
    @pytest.mark.usefixtures("set_driving_unlock")
    @pytest.mark.full
    def test_car_mode_caseid_109945(self):
        '''
        normal to transport
            1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  == 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt == 0 AlrmSt_Disarmd
        '''
        self.mix.diag_not_change_car_mode(1)


    @pytest.mark.usefixtures("set_lock")
    @pytest.mark.full
    def test_car_mode_caseid_110147(self):
        '''
        normal to crash
           1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt != 0 AlrmSt_Disarmd
        '''        
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.Ukwn)
        self.bus_comm.check_alrm_sts_req(alrm_sts=AlrmSts.Armd)
        self.mix.diag_not_change_car_mode(3)

    @pytest.mark.usefixtures("set_lock")
    @pytest.mark.full
    @pytest.mark.carmode
    def test_car_mode_caseid_109918(self):
        '''
        normal to dyno
        
          1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts  != 13 UsgModSts1_UsgModDriving
            2.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1==0 CarModSts1_CarModNormal
            3.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 0 VehMtnSt2_Ukwn
            4.BackboneFR:38-8-64:AlrmStsAlrmSt_AlrmSt != 0 AlrmSt_Disarmd
        '''
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.Ukwn)
        self.bus_comm.check_alrm_sts_req(alrm_sts=AlrmSts.Armd)
        self.mix.diag_not_change_car_mode(5)