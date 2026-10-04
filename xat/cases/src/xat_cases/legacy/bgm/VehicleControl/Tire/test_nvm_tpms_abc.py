import pytest
import random
from xat_cases.legacy.bgm.mcu.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.common.logger import logger

@pytest.mark.mcu_test
class TestNvmStoraAbc(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update(["VehicleModeService_client","LightService_client"])   

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        time.sleep(1)
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)


    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    def reset_bgm(self):
        sleep(10)
        self.io.io_reset_bgm()
        sleep(15)
    
    def reset_bgm_1181(self):
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(25)
        self.sd_tester.update_serverdoipid(0x1002)
    


    @pytest.mark.sanity
    def test_caseid_1993269(self):
        '''写TPMS 281F存储恢复'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        logger.info("读取TPMS ID")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x28, 0x1F]
        )
        sleep(.1)
        write_tpmsid_list = [random.randint(0, 255) for _ in range(16)]
        logger.info("随机写入TPMS ID")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x28, 0x1F], write_tpmsid_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("再次读取tpms id")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x28, 0x1F],
            recv=[0x62, 0x28, 0x1F] + write_tpmsid_list,
            do_assert=True,
        )
        sleep(.1)
        read_tpmsid_lsit = read_date[3:]
        logger.info("恢复tpmsid")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x28, 0x1F] + local_date[3:]
        )
        if read_tpmsid_lsit != write_tpmsid_list:
            log_string = f"写入tpms id失败,读取结果本应为{bytes(write_tpmsid_list).hex()}实际为{bytes(read_tpmsid_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string
    
    @pytest.mark.sanity
    def test_caseid_1984371(self):
        '''写TPMS 281F存储恢复'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        logger.info("读取TPMS ID")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x28, 0x1F]
        )
        sleep(.1)
        write_tpmsid_list = [random.randint(0, 255) for _ in range(16)]
        logger.info("随机写入TPMS ID")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x28, 0x1F], write_tpmsid_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm_1181()
        logger.info("再次读取tpms id")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x28, 0x1F],
            recv=[0x62, 0x28, 0x1F] + write_tpmsid_list,
            do_assert=True,
        )
        sleep(.1)
        read_tpmsid_lsit = read_date[3:]
        logger.info("恢复tpmsid")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x28, 0x1F] + local_date[3:]
        )
        if read_tpmsid_lsit != write_tpmsid_list:
            log_string = f"写入tpms id失败,读取结果本应为{bytes(write_tpmsid_list).hex()}实际为{bytes(read_tpmsid_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    