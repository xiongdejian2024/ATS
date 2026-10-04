import pytest
import random
from xat_cases.legacy.bgm.mcu.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.common.logger import logger

@pytest.mark.mcu_test
class TestNvmStoraAbc(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update(["VehicleModeService_client"])
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.bus_comm.set_dtc_pre()
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)


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
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(25)

    @pytest.mark.sanity
    def test_caseid_1986936(self):
        '''41DE认证密钥_800v'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        logger.info("读取认证密钥")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xDE]
        )
        sleep(.1)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(16)]
        logger.info("读取认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0xDE], write_immokey_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("写入随机密钥后，读取认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xDE],
            recv=[0x62, 0x41, 0xDE] + write_immokey_list,
            do_assert=True,
        )
        sleep(.1)
        read_immokey_lsit = read_date[3:]
        logger.info("恢复认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0xDE,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55] 
        )
        if read_immokey_lsit != write_immokey_list:
            log_string = f"认证密钥写入失败,读取结果本应为{bytes(write_immokey_list).hex()}实际为{bytes(read_immokey_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.sanity
    def test_caseid_1986937(self):
        '''41DF认证密钥_800v'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        logger.info("读取认证密钥")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xDF]
        )
        sleep(.1)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(16)]
        logger.info("读取认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0xDF], write_immokey_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("写入随机密钥后，读取认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xDF],
            recv=[0x62, 0x41, 0xDF] + write_immokey_list,
            do_assert=True,
        )
        sleep(.1)
        read_immokey_lsit = read_date[3:]
        logger.info("恢复认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0xDF,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]
        )
        if read_immokey_lsit != write_immokey_list:
            log_string = f"认证密钥写入失败,读取结果本应为{bytes(write_immokey_list).hex()}实际为{bytes(read_immokey_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string
    
    @pytest.mark.sanity
    def test_caseid_1986938(self):
        '''41E0认证密钥_800v'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        logger.info("读取认证密钥")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xE0]
        )
        sleep(.1)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(16)]
        logger.info("写入认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0xE0], write_immokey_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("写入随机密钥后，读取认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xE0],
            recv=[0x62, 0x41, 0xE0]+ write_immokey_list,
            do_assert=True,
        )
        read_immokey_lsit = read_date[3:]
        logger.info("恢复认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0xE0,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55],
            do_assert=True,
        )
        if read_immokey_lsit != write_immokey_list:
            log_string = f"认证密钥写入失败,读取结果本应为{bytes(write_immokey_list).hex()}实际为{bytes(read_immokey_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.sanity
    def test_caseid_1986939(self):
        '''41E1 SK IV 800V'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        logger.info("读取认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xE1]
        )
        sleep(.1)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(16)]
        logger.info("写入认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0xE1], write_immokey_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("重启后，读取认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0xE1],
            recv=[0x62, 0x41, 0xE1] + write_immokey_list,
            do_assert=True,
        )
        sleep(.1)
        read_immokey_lsit = read_date[3:]
        logger.info("恢复默认值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0xE1,0x69,0x6D,0x6D,0x6F,0x6B,0x65,0x79,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30],
            do_assert=True
        )
        if read_immokey_lsit != write_immokey_list:
            log_string = f"认证密钥写入失败,读取结果本应为{bytes(write_immokey_list).hex()}实际为{bytes(read_immokey_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984495(self):
        '''40A2电量平衡记录'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED)
        logger.info("读取电量平衡记录")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xA2],
            recv=[0x62, 0x40, 0xA2],
            do_assert=True,
        )
        logger.info(f'重启前获取到的{local_date[10]}')
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xA2],
            recv=[0x62, 0x40, 0xA2],
            do_assert=True,
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("读取读取电量平衡记录")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xA2],
            recv=[0x62, 0x40, 0xA2],
            do_assert=True,
        )
        logger.info(f'重启后获取到的{read_date[10]}')
        if read_date[10] != local_date[10]+1:
            assert 0, '电量平衡未记录'

    @pytest.mark.sanity
    def test_caseid_1984376(self):
        '''Factorypaused存储与恢复'''
        self.soa.send_method_request('VehicleModeService_client','SetCarMode',{"mode": 2})
        self.bus_comm.check(
            'backbonefr','CemBackBoneFr02' ,'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02',2)
        #双击危险报警灯开关
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        time.sleep(1)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_car_mode_status(CarMode.NORMAL,car_mode_sub=1)
        time.sleep(1)
        self.reset_bgm()
        self.bus_comm.check_car_mode_status(CarMode.FACTORY,car_mode_sub=0)

    @pytest.mark.full
    def test_caseid_1984462(self):
        '''40E4BMS硬件故障计数'''
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xE4]
        )
        # LIN6信号 设置为11.8 BattURaw
        self.bus_comm.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0xC8, 0xff, 0xff, 0xff, 0xff])
        #仿真DcDcactvd 为1 避免低压报06
        self.bus_comm.set('backbonefr','VddmBackBoneFr08','DcDcActvd',1)
        self.bus_comm.set('cem_lin6','BmsCem_Lin6Fr03', 'BattSnsrHwFltRaw', 1)
        # sleep(20)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        sleep(20)
        self.bus_comm.check('backbonefr','CemBackBoneFr06', 'LVPwrSplyErrSts', 5)
        self.bus_comm.set('cem_lin6','BmsCem_Lin6Fr03', 'BattSnsrHwFltRaw', 0)  
        sleep(1)
        self.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xE4]
        )
        if read_date[7] != local_date[7]+1:
            assert 0, '硬件故障未记录'