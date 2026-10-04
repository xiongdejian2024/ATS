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

    @pytest.mark.sanity
    def test_caseid_1993316(self):
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
    def test_caseid_1993317(self):
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
    def test_caseid_1993318(self):
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
    def test_caseid_1993319(self):
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

    # @pytest.mark.full
    # def test_caseid_1984495(self):
    #     '''40A2电量平衡记录'''
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED)
    #     logger.info("读取电量平衡记录")
    #     ret_code, local_date = self.sd_tester.send_request_and_recv_response(
    #         [0x22, 0x40, 0xA2],
    #         recv=[0x62, 0x40, 0xA2],
    #         do_assert=True,
    #     )
    #     logger.info(f'重启前获取到的{local_date[10]}')
    #     self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
    #     sleep(1)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response(
    #         [0x22, 0x40, 0xA2],
    #         recv=[0x62, 0x40, 0xA2],
    #         do_assert=True,
    #     )
    #     sleep(1)
    #     logger.info("重启bgm")
    #     self.reset_bgm()
    #     logger.info("读取读取电量平衡记录")
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED)
    #     ret_code, read_date = self.sd_tester.send_request_and_recv_response(
    #         [0x22, 0x40, 0xA2],
    #         recv=[0x62, 0x40, 0xA2],
    #         do_assert=True,
    #     )
    #     logger.info(f'重启后获取到的{read_date[10]}')
    #     if read_date[10] != local_date[10]+1:
    #         assert 0, '电量平衡未记录'

    @pytest.mark.sanity
    def test_caseid_1993274(self):
        '''Factorypaused存储与恢复'''
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.mix.s2s_change_car_mode_and_check_result(CarMode.FACTORY,car_mode_sub=0)
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

    @pytest.mark.smoke
    def test_caseid_1993272(self):
        '''Usagemode_本地存储和恢复_Driving_No_Run'''
        self.mix.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.bus_comm.check_usage_mode_status(UsageMode.ACTIVE)
        self.bus_comm.set(
            'backbonefr','VddmBackBoneFr00', 'EngSt1WdStsEngSt1WdSts', 5
        )
        time.sleep(10)
        self.reset_bgm()
        self.bus_comm.set(
            'backbonefr','VddmBackBoneFr00', 'EngSt1WdStsEngSt1WdSts', 0
        )
        self.bus_comm.check_usage_mode_status(UsageMode.ACTIVE)

    @pytest.mark.smoke
    def test_caseid_1993275(self):
        '''车辆模式的本地存储和恢复_CarModFactory'''
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.mix.s2s_change_car_mode_and_check_result(CarMode.FACTORY,car_mode_sub=0)
        time.sleep(10)
        self.reset_bgm()
        self.bus_comm.check_car_mode_status(CarMode.FACTORY,car_mode_sub=0)

    @pytest.mark.smoke
    def test_caseid_1993284(self):
        '''展车模式存储与恢复'''
        self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00', 'EpbStsEpbSts', 3)
        self.soa.send_method_request(
            'VehicleModeService_client',
            'SetExhibitionMode',
            {"isOpen": True},
        )
        self.soa.send_request_and_ck_resp(
            'VehicleModeService_client',
            "GetExhibitionModeSts",
            {},
            {"out": {"isOpen": True, "isValid": True}},
        )
        self.bus_comm.check(
            'propulsioncan','BgmPropulsionFr01',
            'ExhibitionModeStsExhibitionModeSts_1_BgmPropSignalIPdu01',
            'OnOff1_On'
        )
        time.sleep(1)
        self.reset_bgm()
        self.bus_comm.check(
            'propulsioncan','BgmPropulsionFr01',
            'ExhibitionModeStsExhibitionModeSts_1_BgmPropSignalIPdu01',
            'OnOff1_On',
        )

    @pytest.mark.sanity
    def test_caseid_1993274(self):
        '''Carmode_车辆模式的本地存储和恢复_FactoryPaused'''
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.mix.s2s_change_car_mode_and_check_result(CarMode.FACTORY,car_mode_sub=0)
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
    @pytest.mark.smoke
    def test_caseid_1993276(self):
        '''门状态存储'''
        self.io.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
        self.io.set_door(Drvr=Door.open, Pass=Door.close, RiRe=Door.close, LeRe=Door.open, Trunk=Door.close)
        self.bus_comm.check(
            'bodycan','CemBodyFr02', 'DoorDrvrSts_2_CemBodySignalIPdu02', 1
        )
        self.bus_comm.check(
            'bodycan','CemBodyFr02', 'DoorLeReSts_1_CemBodySignalIPdu02', 1
        )
        self.reset_bgm()
        self.bus_comm.check(
            'bodycan','CemBodyFr02', 'DoorDrvrSts_2_CemBodySignalIPdu02', 1
        )
        self.bus_comm.check(
            'bodycan','CemBodyFr02', 'DoorLeReSts_1_CemBodySignalIPdu02', 1
        )

    @pytest.mark.smoke
    def test_caseid_1993280(self):
        '''读FOTA状态F153存储'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        logger.info("读FOTA状态值")
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0xF1, 0x53]
        )
        sleep(.1)
        write_f153_list = [random.randint(0, 4)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0xF1, 0x53], write_f153_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("读FOTA状态值")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0xF1, 0x53],
            recv=[0x62, 0xF1, 0x53] + write_f153_list,
            do_assert=True,
        )
        sleep(1)
        read_f153_lsit = read_date[3:]
        logger.info("恢复读FOTA状态值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0xF1, 0x53, 0x00]
        )
        if read_f153_lsit != write_f153_list:
            log_string = f"写入读FOTA状态值失败,读取结果本应为{bytes(write_f153_list).hex()}实际为{bytes(read_f153_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.smoke
    def test_caseid_1993283(self):
        '''雨量传感器阈值DID 45A4'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        logger.info("读取雨量传感器阈值")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0xA4]
        )
        sleep(.1)
        write_rain_list = [random.randint(0, 15)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0xA4], write_rain_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("读取雨量传感器阈值")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0xA4],
            recv=[0x62, 0x45, 0xA4] + write_rain_list
        )
        sleep(.1)
        read_rain_lsit = read_date[3:]
        logger.info("恢复雨量传感器阈值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0xA4] + local_date[3:]
        )
        if read_rain_lsit != write_rain_list:
            log_string = f"写入雨量传感器阈值失败,读取结果本应为{bytes(write_rain_list).hex()}实际为{bytes(read_rain_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.smoke
    def test_caseid_1993268(self):
        '''认证密钥40DE存储'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        logger.info("读取认证密钥")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xDE]
        )
        sleep(.1)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(32)]
        logger.info("读取认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0xDE], write_immokey_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("写入随机密钥后，读取认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xDE],
            recv=[0x62, 0x40, 0xDE] + write_immokey_list,
            do_assert=True,
        )
        sleep(.1)
        read_immokey_lsit = read_date[3:]
        logger.info("恢复认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0xDE] + local_date[3:]
        )
        if read_immokey_lsit != write_immokey_list:
            log_string = f"认证密钥写入失败,读取结果本应为{bytes(write_immokey_list).hex()}实际为{bytes(read_immokey_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.smoke
    def test_caseid_1993267(self):
        '''认证密钥40DF存储'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        logger.info("读取认证密钥")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xDF]
        )
        sleep(.1)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(32)]
        logger.info("读取认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0xDF], write_immokey_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("写入随机密钥后，读取认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xDF],
            recv=[0x62, 0x40, 0xDF] + write_immokey_list,
            do_assert=True,
        )
        sleep(.1)
        read_immokey_lsit = read_date[3:]
        logger.info("恢复认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0xDF] + local_date[3:]
        )
        if read_immokey_lsit != write_immokey_list:
            log_string = f"认证密钥写入失败,读取结果本应为{bytes(write_immokey_list).hex()}实际为{bytes(read_immokey_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.smoke
    def test_caseid_1993266(self):
        '''认证密钥40E0存储'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        logger.info("读取认证密钥")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xE0]
        )
        sleep(.1)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(32)]
        logger.info("读取认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0xE0], write_immokey_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("写入随机密钥后，读取认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xE0],
            recv=[0x62, 0x40, 0xE0] + write_immokey_list,
            do_assert=True,
        )
        sleep(.1)
        read_immokey_lsit = read_date[3:]
        logger.info("恢复认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0xE0] + local_date[3:]
        )
        if read_immokey_lsit != write_immokey_list:
            log_string = f"认证密钥写入失败,读取结果本应为{bytes(write_immokey_list).hex()}实际为{bytes(read_immokey_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    # @pytest.mark.sanity
    # def test_caseid_1984457(self):
    #     '''40EF闭锁命令记录'''
    #     self.sd_tester.send_data([0x22, 0x40, 0xEF])
    #     result1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
    #     sleep(1)
    #     self.io.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
    #     self.bus_comm.dk.set_cenlock_sts(0x3)
    #     sleep(5)
    #     self.reset_bgm()
    #     self.sd_tester.send_data([0x22, 0x40, 0xEF])
    #     result2 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
    #     if result1 == result2:
    #         str1 = f'此次闭锁命令未记录'
    #         logger.info(str1)
    #         assert 0, str1

    # @pytest.mark.sanity
    # def test_caseid_1984458(self):
    #     '''40F0解锁命令记录'''
    #     self.sd_tester.send_data([0x22, 0x40, 0xF0])
    #     result1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
    #     self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
    #     self.bus_comm.dk.set_cenlock_sts(0x1)
    #     sleep(5)
    #     # self.reset_bgm()
    #     self.sd_tester.update_serverdoipid(0x1FFF)
    #     self.sd_tester.send_data([0x11, 0x81])
    #     sleep(25)
    #     self.sd_tester.send_data([0x22, 0x40, 0xF0])
    #     result2 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
    #     if result1 == result2:
    #         str1 = f'此次解锁命令未记录'
    #         logger.info(str1)
    #         assert 0, str1

    @pytest.mark.smoke
    def test_caseid_1993273(self):
        '''Usagemode_本地存储和恢复_Active_No_Run'''
        self.mix.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.bus_comm.check_usage_mode_status(UsageMode.ACTIVE)
        self.reset_bgm()
        self.bus_comm.check_usage_mode_status(UsageMode.ACTIVE)

    @pytest.mark.smoke
    def test_caseid_1993271(self):
        '''写CCP车辆配置字F106存储恢复'''
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0xF1, 0x06]
        )
        sleep(.1)
        logger.info("写入ccp")
        self.sd_tester.write_single_ccp(1556, 4)  # 总共1558个byte,后两位是校验位
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("再次读取ccp")
        self.sd_tester.send_data([0x22, 0xF1, 0x06])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        logger.info("恢复ccp")
        localdate = local_date[-3]
        self.sd_tester.write_single_ccp(1556, localdate)
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        assert result[-3] == 4

    @pytest.mark.smoke
    def test_caseid_1993270(self):
        '''写vin码F190存储恢复'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0xF1, 0x90]
        )
        sleep(.1)
        write_vin_list = [random.randint(0, 255) for _ in range(17)]
        logger.info("随机写入vin码")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0xF1, 0x90], write_vin_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("再次读取vin码")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0xF1, 0x90],
            recv=[0x62, 0xF1, 0x90] + write_vin_list,
            do_assert=True,
        )
        sleep(.1)
        read_vin_lsit = read_date[3:]
        logger.info("恢复vin码")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0xF1, 0x90] + local_date[3:]
        )
        if read_vin_lsit != write_vin_list:
            log_string = f"写入vin码失败,读取结果本应为{bytes(write_vin_list).hex()}实际为{bytes(read_vin_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

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

    @pytest.mark.smoke
    def test_caseid_1993286(self):
        '''电源管理DIDF0F5存储'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        logger.info("读取电源管理值")
        self.sd_tester.send_request_and_recv_response([0x22, 0xF0, 0xF5])
        sleep(.1)
        logger.info("写入电源管理值")
        self.sd_tester.send_request_and_recv_response([0x2E, 0xF0, 0xF5, 0x27, 0x0A, 0X03, 0X05, 0X03, 0x02],do_assert=True)
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("读取电源管理值")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code,read_date=self.sd_tester.send_request_and_recv_response([0x22, 0xF0, 0xF5],do_assert=True)
        sleep(.1)
        logger.info("恢复电源管理值")
        self.sd_tester.send_request_and_recv_response([0x2E, 0xF0, 0xF5, 0x28, 0x0A, 0X03, 0X05, 0X03, 0x02],do_assert=True)
        if read_date[-6] != 39:
            assert 0,"F0F5电源管理值未存储"

    @pytest.mark.sanity
    def test_caseid_1993290(self):
        '''4600内灯亮度值调节'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        logger.info("读取内灯亮度值")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x46, 0x00]
        )
        sleep(.1)
        logger.info("写入内灯亮度值")
        write_power_list = [random.randint(0, 100) for _ in range(5)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x46, 0x00], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("读取内灯亮度值")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x46, 0x00],
            recv=[0x62, 0x46, 0x00] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复内灯亮度值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x46, 0x00] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入内灯亮度值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.smoke
    def test_caseid_1993282_1993281(self):
        '''nfc解闭锁状态存储'''
        self.io.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        self.bus_comm.check(
            'connectivitycanfd','VgmConnFr12',
            'LockgCenStsLockSt_2_VgmConnSignalIPdu12',
            3,
        )
        logger.info("nfc解锁")
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        self.bus_comm.check(
            'connectivitycanfd','VgmConnFr12',
            'LockgCenStsLockSt_2_VgmConnSignalIPdu12',
            1,
        )

    @pytest.mark.full
    def test_caseid_1984455(self):
        '''使用模式时间统计convenience存储区间为72-96bit'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data([0x22, 0x43, 0x0F])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        date1 = result[12]
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.soa.send_method_request('VehicleModeService_client', "SetUsageModeUp", {"mode": 2})
        sleep(6)
        self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)
        time.sleep(63)  # 需求中需要等待1min才能存储
        self.sd_tester.send_data([0x22, 0x43, 0x0F])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        self.reset_bgm()
        self.sd_tester.send_data([0x22, 0x43, 0x0F])
        result1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        date2 = result1[12]
        if date2 != date1 + 1:
            assert 0, "usagemode未存储此次时间统计"

    @pytest.mark.smoke
    def test_caseid_1984381(self):
        '''统计usagemode使用次数存储convenience存储区间为144-160bit'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data([0x22, 0x43, 0x0E])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        date1 = result[21]
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.soa.send_method_request('VehicleModeService_client', "SetUsageModeUp", {"mode": 2})
        sleep(6)
        self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)
        sleep(11)  # 需求中需要等待10s才能计数
        self.reset_bgm()
        self.sd_tester.send_data([0x22, 0x43, 0x0E])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        if result[21] != date1 + 2:  # 因为重启的时候超过了10s所以应+2
            assert 0, "usagemode未存储此次切换"

    @pytest.mark.full
    def test_caseid_1984472(self):
        '''4297解锁持续时间'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        logger.info("读取nfc解锁持续时间的值")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x42, 0x97]
        )
        sleep(.1)
        logger.info("写入nfc解锁持续时间的值")
        write_power_list = [random.randint(0, 255)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x42, 0x97], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("读取nfc解锁持续时间的值")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x42, 0x97],
            recv=[0x62, 0x42, 0x97] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复nfc解锁持续时间的值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x42, 0x97, 0xFF], do_assert=True
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入nfc解锁持续时间的值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984473(self):
        '''4532休眠超时充电使能'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data([0x22, 0x45, 0x32])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        self.sd_tester.send_data([0x2E, 0x45, 0x32, 0x01])
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.sd_tester.send_data([0x22, 0x45, 0x32])
        date1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data([0x2E, 0x45, 0x32, 0x00])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        if date1[-1] != 1:
            assert 0, "本次写入的值未存储"

    @pytest.mark.full
    def test_caseid_1984474(self):
        '''DID4534休眠异常充电电压阈值,
        诊断调查表中DID读出的值应除以10范围在8-16'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x34]
        )
        sleep(.1)
        logger.info("随机写入值")
        write_power_list = [random.randint(80, 160)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x34], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x34],
            recv=[0x62, 0x45, 0x34] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x34] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984475(self):
        '''DID4530休眠低压唤醒充电使能,取值0=Enable 1=Disable'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data([0x22, 0x45, 0x30])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        self.sd_tester.send_data([0x2E, 0x45, 0x30, 0x01])
        logger.info("bgm重启")
        sleep(1)
        self.reset_bgm()
        self.sd_tester.send_data([0x22, 0x45, 0x30])
        date1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data([0x2E, 0x45, 0x30, 0x00])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        if date1[-1] != 1:
            assert 0, "本次写入的值未存储"

    @pytest.mark.full
    def test_caseid_1984476(self):
        '''
        DID4531休眠低压唤醒充电电压阈值
        取值范围8-16
        '''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x31]
        )
        sleep(.1)
        write_power_list = [random.randint(80, 160)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x31], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x31],
            recv=[0x62, 0x45, 0x31] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x31] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984477(self):
        '''DID4533能补电退出SOC阈值'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x33]
        )
        sleep(.1)
        write_power_list = [random.randint(0, 127)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x33], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x33],
            recv=[0x62, 0x45, 0x33] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x33] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.smoke
    def test_caseid_1984367(self):
        '''408F远程车辆IMMO密钥的读写状态16个byte'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0x8F]
        )
        sleep(.1)
        write_power_list = [random.randint(0, 255) for _ in range(16)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0x8F], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.sd_tester.stop_tester_present()
        self.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0x8F],
            recv=[0x62, 0x40, 0x8F] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0x8F] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.sanity
    def test_caseid_1984478(self):
        '''诊断写carmode'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY)
        sleep(1)
        self.reset_bgm()
        self.sd_tester.send_data([0x22, 0xD1, 0x34])
        date1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        if date1[-1] != 2:
            assert 0, "此次切换未存储"

    @pytest.mark.smoke
    def test_caseid_1984479(self):
        '''防盗状态'''
        self.io.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        time.sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check(
            'bodycan','CemBodyFr02', 'DoorDrvrSts_2_CemBodySignalIPdu02', 1
        )
        self.bus_comm.check('backbonefr','CemBackBoneFr18', 'AlrmStsAlrmSt', 2)
        self.reset_bgm()
        self.bus_comm.check('backbonefr','CemBackBoneFr18', 'AlrmStsAlrmSt', 2)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)

    @pytest.mark.full
    def test_caseid_1984480(self):
        '''4535充电开启SOC阈值'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x35]
        )
        sleep(.1)
        write_power_list = [random.randint(0, 127)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x35], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x35],
            recv=[0x62, 0x45, 0x35] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x35] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984481(self):
        '''42E9中控锁防玩保护'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        self.sd_tester.send_data([0x22, 0x42, 0xE9])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        self.sd_tester.send_data([0x2E, 0x42, 0xE9, 0x01])
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        self.sd_tester.send_data([0x22, 0x42, 0xE9])
        date1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        self.sd_tester.send_data([0x2E, 0x42, 0xE9, 0x00])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        if date1[-1] != 1:
            assert 0, "本次写入的值未存储"

    @pytest.mark.full
    def test_caseid_1984486(self):
        '''4109方向盘加热温度补偿'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0x09]
        )
        sleep(1)
        write_power_list = [random.randint(1, 15)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0x09], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0x09],
            recv=[0x62, 0x41, 0x09] + write_power_list,
            do_assert=True,
        )
        sleep(1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0x09] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984485(self):
        '''4313驱动数量,只有1和2两驱和四驱'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0x13])
        sleep(.1)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x43, 0x13, 0x02])
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        self.sd_tester.send_data([0x22, 0x43, 0x13])
        date1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x43, 0x13, 0x01])
        if date1[-1] != 2:
            assert 0, "本次写入的值未存储"

    @pytest.mark.full
    def test_caseid_1984482(self):
        '''7023方向盘加热控制'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x70, 0x23]
        )
        sleep(.1)
        write_power_list = [
            random.randint(0, 2),
            random.randint(0, 88),
            random.randint(0, 2),
            random.randint(0, 88),
            random.randint(0, 100),
            random.randint(0, 100),
            random.randint(0, 120),
            random.randint(0, 120),
            random.randint(0, 120),
        ]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x70, 0x23], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x70, 0x23],
            recv=[0x62, 0x70, 0x23] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x70, 0x23] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.sanity
    def test_caseid_1984483(self):
        '''内灯模式存储'''
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.soa.send_method_request(
            "LightService_client",
            "LightControl",
            {
                "lights": [
                    {
                        "light": {"type": 26, "zoneId": 0},
                        "mode": 2,
                        "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0},
                    }
                ]
            },
        )
        sleep(1)
        self.soa.send_request_and_ck_resp(
            "LightService_client", "GetInternalLightMode", {}, {"out": 2}
        )
        self.reset_bgm()
        self.soa.send_request_and_ck_resp(
            "LightService_client", "GetInternalLightMode", {}, {"out": 2}
        )

    @pytest.mark.full
    def test_caseid_1984484(self):
        '''EE99喇叭开关触发喇叭的次数和时间'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        self.sd_tester.send_data([0x22, 0xEE, 0x99])
        result1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        self.io.set_horn_switch_sts(isOn.Off)#打开
        sleep(3)
        self.io.set_horn_switch_sts(isOn.On)#关闭
        self.sd_tester.send_request_and_recv_response([0x22, 0xEE, 0x99])
        sleep(1)
        self.reset_bgm()
        self.sd_tester.send_data([0x22, 0xEE, 0x99])
        result2 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        if result2[3] != result1[3] + 1:
            assert 0, "本次开关未存储"

    # @pytest.mark.full
    # def test_caseid_1984490(self):
    #     '''4200电动尾翼'''
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
    #     ret_code, local_date = self.sd_tester.send_request_and_recv_response(
    #         [0x22, 0x42, 0x00]
    #     )
    #     sleep(.1)
    #     write_power_list = [
    #         random.randint(0, 1),
    #         random.randint(0, 244),
    #         random.randint(0, 1),
    #         random.randint(0, 244),
    #     ]
    #     self.sd_tester.send_request_and_recv_response(
    #         [0x2E, 0x42, 0x00], write_power_list, do_assert=True
    #     )
    #     sleep(1)
    #     logger.info("bgm重启")
    #     self.reset_bgm()
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
    #     ret_code, read_date = self.sd_tester.send_request_and_recv_response(
    #         [0x22, 0x42, 0x00],
    #         recv=[0x62, 0x42, 0x00] + write_power_list,
    #         do_assert=True,
    #     )
    #     sleep(.1)
    #     read_power_lsit = read_date[3:]
    #     logger.info("恢复值")
    #     self.sd_tester.send_request_and_recv_response(
    #         [0x2E, 0x42, 0x00] + local_date[3:]
    #     )
    #     if read_power_lsit != write_power_list:
    #         log_string = f"写入电动尾翼值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
    #         logger.info(log_string)
    #         assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984493(self):
        '''416D室内灯光白天至黑夜计时器存储'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0x6D]
        )
        sleep(.1)
        num = random.randint(0, 10000)
        num_hex = hex(num)[2:].zfill(4)
        write_list = [int(num_hex[i : i + 2], 16) for i in range(0, len(num_hex), 2)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0x6D], write_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0x6D], recv=[0x62, 0x41, 0x6D] + write_list, do_assert=True
        )
        sleep(.1)
        read_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0x6D, 0x07, 0xD0])
        if read_lsit != write_list:
            log_string = (
                f"写入41F8值失败,读取结果本应为{bytes(write_list).hex()}实际为{bytes(read_lsit).hex()}"
            )
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984494(self):
        '''416E室内灯光黑夜至白天计时器存储'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0x6E])
        sleep(.1)
        num = random.randint(0, 10000)
        num_hex = hex(num)[2:].zfill(4)
        write_list = [int(num_hex[i : i + 2], 16) for i in range(0, len(num_hex), 2)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0x6E], write_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0x6E], recv=[0x62, 0x41, 0x6E] + write_list, do_assert=True
        )
        sleep(.1)
        read_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0x6E, 0x07, 0xD0])
        if read_lsit != write_list:
            log_string = (
                f"写入416E值失败,读取结果本应为{bytes(write_list).hex()}实际为{bytes(read_lsit).hex()}"
            )
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984491(self):
        '''416F内灯白天至黑夜值'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0x6F])
        sleep(.1)
        num = random.randint(400, 700)
        num_hex = hex(num)[2:].zfill(4)
        write_list = [int(num_hex[i : i + 2], 16) for i in range(0, len(num_hex), 2)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0x6F], write_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0x6F], recv=[0x62, 0x41, 0x6F] + write_list, do_assert=True
        )
        sleep(.1)
        read_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0x6F, 0x07, 0xD0])
        if read_lsit != write_list:
            log_string = (
                f"写入值失败,读取结果本应为{bytes(write_list).hex()}实际为{bytes(read_lsit).hex()}"
            )
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984492(self):
        '''4170内灯黑夜至白天值'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0x70])
        sleep(.1)
        num = random.randint(800, 1300)
        num_hex = hex(num)[2:].zfill(4)
        write_list = [int(num_hex[i : i + 2], 16) for i in range(0, len(num_hex), 2)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0x70], write_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0x70], recv=[0x62, 0x41, 0x70] + write_list, do_assert=True
        )
        sleep(.1)
        read_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0x70, 0x07, 0xD0])
        if read_lsit != write_list:
            log_string = (
                f"写入值失败,读取结果本应为{bytes(write_list).hex()}实际为{bytes(read_lsit).hex()}"
            )
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1993291(self):
        '''40E4BMS硬件故障计数'''
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xE4]
        )
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        # LIN6信号 设置为11.8 BattURaw
        self.bus_comm.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0xC8, 0xff, 0xff, 0xff, 0xff])
        #仿真DcDcactvd 为1 避免低压报06
        self.bus_comm.set('backbonefr','VddmBackBoneFr08','DcDcActvd',1)
        sleep(1) 
        self.bus_comm.set('cem_lin6','BmsCem_Lin6Fr03', 'BattSnsrHwFltRaw', 1)
        sleep(20)
        # UsageMode 设置为13 Driving
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        sleep(5)
        self.bus_comm.check('backbonefr','CemBackBoneFr06', 'LVPwrSplyErrSts', 5)
        self.bus_comm.set('cem_lin6','BmsCem_Lin6Fr03', 'BattSnsrHwFltRaw', 0)  
        sleep(1)
        self.reset_bgm()
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xE4]
        )
        if read_date[7] != local_date[7]+1:
            assert 0, '硬件故障未记录'