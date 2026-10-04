"""
@filename     : test_UdsServer.py
@time         : 2024/10/14 14:19
@author       : lei.tao@jiduauto.com
@description  : 
"""


import os
import sys
import ctypes
import multiprocessing
import traceback
import allure
import pytest
cur_path = os.path.join(os.getcwd().split('sat')[0], 'sat')
sys.path.append(cur_path)
from xat_cases.legacy.jetsoa.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.nuc_app import *
from xat_cases.legacy.jetsoa.case_helper.json_modification import *



def run_with_assert(queue, func, *args, **kwargs):
    """
    使用断言执行函数，并将结果或异常发送到队列。
    Args:
        queue (Queue): 用于存储结果的队列。
        func (Callable[..., Any]): 要执行的函数。
        *args: 传递给func的位置参数。
        **kwargs: 传递给func的关键字参数。

    Returns:
        无返回值。结果或异常将被发送到队列中。
    """
    try:
        func(*args, **kwargs)
        queue.put(None)  # 表示没有异常
    except AssertionError as e:
        queue.put((e, traceback.format_exc()))  # 发送异常和堆栈跟踪到队列
    except Exception as e:
        queue.put((e, traceback.format_exc()))  # 捕获其他可能的异常



@allure.feature("Demon")
@allure.story("UdsServer")
class TestExampleAbstract(TestABCBase):
    def before_class(self, ecu):
        logger.info("before_class")
        process_check("CarinaX86_64/bin")
        self.diagd = None
        self.jetlog = None
        super().before_class(self, ecu)
        # 启动jetlog
        self.jetlog = start_process(os.path.join(cur_path, "sotest/juds_demo/start_jetlog.sh"))
        # 启动diag
        self.diagd = start_process(os.path.join(cur_path, "sotest/juds_demo/start_diagd.sh"))
        
    def before_each_func(self, ecu):
        logger.info("before_each_func")
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        logger.info("after_class")
        if self.diagd:
            stop_process(self.diagd)
        if self.jetlog:
            stop_process(self.jetlog)
        sleep(3)#等待日志落盘
        process_check("CarinaX86_64/bin")
        jetsoa_env_check()
        super().after_class(self, ecu)

    def read_did_f186(self):
        #  load c++ library
        self.cpp_case_lib = ctypes.cdll.LoadLibrary("../../sotest/juds_demo/build/libtest_uds_app.so")
        self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        # call c++ function
        result = self.cpp_case_lib.start_uds_server()
        # check result
        assert 0 == result
        data_ret = b"\x03"
        self.cpp_case_lib.setup_read_did_cb1(0x1001, 0x0E80, 0xF186, data_ret, len(data_ret), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0xF1, 0x86])
        sleep(0.2)
        assert 0 == self.cpp_case_lib.check_read_did_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x62, 0xF1, 0x86, 0x03]
        self.cpp_case_lib.stop_uds_server() 

    def read_did_f190(self):
        #  load c++ library
        self.cpp_case_lib_f190 = ctypes.cdll.LoadLibrary("../../sotest/juds_demo/build/libtest_uds_app.so")
        self.cpp_case_lib_f190.startUdsServer_ReadDid.restype = ctypes.c_int
        # call c++ function
        result = self.cpp_case_lib_f190.startUdsServer_ReadDid()
        # check result
        assert 0 == result
        data_ret = b"\x03"
        self.cpp_case_lib_f190.setup_read_did_cb1(0x1001, 0x0E80, 0xF190, data_ret, len(data_ret), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x22, 0xF1, 0x90])
        sleep(0.2)
        assert 0 == self.cpp_case_lib_f190.check_read_did_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x62, 0xF1, 0x90, 0x03]
        self.cpp_case_lib_f190.stop_uds_server()

    @allure.title("多进程读DID服务")
    @pytest.mark.smoke
    def test_caseid_1989260(self):
        queue = multiprocessing.Queue()
        # 创建并启动进程
        for i in [self.read_did_f186, self.read_did_f190]:
            p = multiprocessing.Process(target=run_with_assert, args=(queue, i))
            p.start()
            p.join()
            result = queue.get()

        if result is None:
            print("Function executed successfully")
        else:
            exception, traceback_str = result
            print(f"An assert error occurred in the function:{exception}")
            print(traceback_str)
            assert False # 这里可以进一步处理异常，比如记录日志、重新抛出等

#########################################################################################################################
    def write_did_d904(self):
        #  load c++ library
        self.cpp_case_lib = ctypes.cdll.LoadLibrary("../../sotest/juds_demo/build/libtest_uds_app.so")
        self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        # call c++ function
        result = self.cpp_case_lib.start_uds_server()
        # check result
        assert 0 == result
        data_exp = b"\x02\x02\x02"
        self.cpp_case_lib.setup_write_did_cb1(0x1001, 0x0E80, 0xD904, data_exp, len(data_exp), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x2E, 0xd9, 0x04, 0x02, 0x02, 0x02])
        sleep(0.2)
        assert 0 == self.cpp_case_lib.check_write_did_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x6E, 0xd9, 0x04]
        self.cpp_case_lib.stop_uds_server() 

    #### 写DID服务_d9ba
    def write_did_d9ba(self):#  load c++ library
        self.cpp_case_lib_d9ba = ctypes.cdll.LoadLibrary("../../sotest/juds_demo/build/libtest_uds_app.so")
        self.cpp_case_lib_d9ba.startUdsServer_WriteDid.restype = ctypes.c_int
        # call c++ function
        result = self.cpp_case_lib_d9ba.startUdsServer_WriteDid()
        # check result
        assert 0 == result
        data_exp = b"\x02\x02\x02"
        self.cpp_case_lib_d9ba.setup_write_did_cb1(0x1001, 0x0E80, 0xD9BA, data_exp, len(data_exp), 0)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x2E, 0xd9, 0xba, 0x02, 0x02, 0x02])
        sleep(0.2)
        assert 0 == self.cpp_case_lib_d9ba.check_write_did_cb_result()
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x6E, 0xd9, 0xba]
        self.cpp_case_lib_d9ba.stop_uds_server()

    @allure.title("多进程写DID服务")
    @pytest.mark.smoke
    def test_caseid_1989261(self):
        queue = multiprocessing.Queue()
        # 创建并启动进程
        for i in [self.write_did_d904, self.write_did_d9ba]:
            p = multiprocessing.Process(target=run_with_assert, args=(queue, i))
            p.start()
            p.join()
            result = queue.get()

        if result is None:
            print("Function executed successfully")
        else:
            exception, traceback_str = result
            print(f"An assert error occurred in the function:{exception}")
            print(traceback_str)
            assert False

    @allure.title("多进程读写DID服务")
    @pytest.mark.smoke
    def test_caseid_1989262(self):
        queue = multiprocessing.Queue()
        # 创建并启动进程
        for i in [self.read_did_f186, self.write_did_d9ba]:
            p = multiprocessing.Process(target=run_with_assert, args=(queue, i))
            p.start()
            p.join()
            result = queue.get()

        if result is None:
            print("Function executed successfully")
        else:
            exception, traceback_str = result
            print(f"An assert error occurred in the function:{exception}")
            print(traceback_str)
            assert False

#########################################################################################################################
    def routine_control_ea29(self):
        #  load c++ library
        self.cpp_case_lib = ctypes.cdll.LoadLibrary("../../sotest/juds_demo/build/libtest_uds_app.so")
        self.cpp_case_lib.start_uds_server.restype = ctypes.c_int
        # call c++ function
        result = self.cpp_case_lib.start_uds_server()
        # check result
        assert 0 == result
        option_record_exp = b"\x01\x02"
        status_record_return = b"\x02\x03"
        self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x01,0xea29,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)  #31服务
        sleep(0.2)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x31, 0x01, 0xea, 0x29, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x71, 0x01, 0xea, 0x29, 0x02, 0x03]
        assert 0 == self.cpp_case_lib.check_routine_ctrl_cb_result(1)
        self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x03,0xea29,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)  #31服务
        self.sd_tester.send_data([0x31, 0x03, 0xea, 0x29])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x71, 0x03, 0xea, 0x29, 0x02, 0x03]
        assert 0 == self.cpp_case_lib.check_routine_ctrl_cb_result(3)
        self.cpp_case_lib.setup_routine_ctrl_cb1(0x1001,0x0E80,0x02,0xea29,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)  #31服务
        self.sd_tester.send_data([0x31, 0x02, 0xea, 0x29])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x71, 0x02, 0xea, 0x29, 0x02, 0x03]
        assert 0 == self.cpp_case_lib.check_routine_ctrl_cb_result(2)
        self.cpp_case_lib.stop_uds_server() 

    #### 例程控制routeine_control_a100
    def routine_control_a100(self):
        self.cpp_case_lib_a100 = ctypes.cdll.LoadLibrary("../../sotest/juds_demo/build/libtest_uds_app.so")
        self.cpp_case_lib_a100.startUdsServer_routine_id.restype = ctypes.c_int
        # call c++ function
        result = self.cpp_case_lib_a100.startUdsServer_routine_id()
        # check result
        assert 0 == result
        option_record_exp = b"\x01\x02"
        status_record_return = b"\x02\x03"
        self.cpp_case_lib_a100.setup_routine_ctrl_cb1(0x1001,0x0E80,0x01,0xa100,
            option_record_exp,len(option_record_exp),status_record_return,len(status_record_return),0)  #31服务
        sleep(0.2)
        self.sd_tester.update_serverdoipid(0x1001, ecu="BGM")  # server_addr
        self.sd_tester.send_data([0x31, 0x01, 0xa1, 0x00, 0x01, 0x02])
        sleep(0.2)
        result = (self.sd_tester.return_udsdata_and_check_and_print_response_result())
        assert result == [0x71, 0x01, 0xa1, 0x00, 0x02, 0x03]
        assert 0 == self.cpp_case_lib_a100.check_routine_ctrl_cb_result(1)
        self.cpp_case_lib_a100.stop_uds_server()
    
    @allure.title("多进程例程控制服务")
    @pytest.mark.smoke
    def test_caseid_1989263(self):
        queue = multiprocessing.Queue()
        # 创建并启动进程
        for i in [self.routine_control_ea29, self.routine_control_a100]:
            p = multiprocessing.Process(target=run_with_assert, args=(queue, i))
            p.start()
            p.join()
            result = queue.get()

        if result is None:
            print("Function executed successfully")
        else:
            exception, traceback_str = result
            print(f"An assert error occurred in the function:{exception}")
            print(traceback_str)
            assert False

    @allure.title("多进程读did和例程控制服务")
    @pytest.mark.smoke
    def test_caseid_1989264(self):
        queue = multiprocessing.Queue()
        # 创建并启动进程
        for i in [self.read_did_f186, self.routine_control_a100]:
            p = multiprocessing.Process(target=run_with_assert, args=(queue, i))
            p.start()
            p.join()
            result = queue.get()

        if result is None:
            print("Function executed successfully")
        else:
            exception, traceback_str = result
            print(f"An assert error occurred in the function:{exception}")
            print(traceback_str)
            assert False

    @allure.title("多进程写did和例程控制服务")
    @pytest.mark.smoke
    def test_caseid_1989265(self):
        queue = multiprocessing.Queue()
        # 创建并启动进程
        for i in [self.write_did_d904, self.routine_control_a100]:
            p = multiprocessing.Process(target=run_with_assert, args=(queue, i))
            p.start()
            p.join()
            result = queue.get()

        if result is None:
            print("Function executed successfully")
        else:
            exception, traceback_str = result
            print(f"An assert error occurred in the function:{exception}")
            print(traceback_str)
            assert False

    @allure.title("多进程读写did和例程控制服务")
    @pytest.mark.smoke
    def test_caseid_1989266(self):
        queue = multiprocessing.Queue()
        # 创建并启动进程
        for i in [self.read_did_f186, self.read_did_f190, self.write_did_d904, self.write_did_d9ba, self.routine_control_a100, self.routine_control_ea29]:
            p = multiprocessing.Process(target=run_with_assert, args=(queue, i))
            p.start()
            p.join()
            result = queue.get()

        if result is None:
            print("Function executed successfully")
        else:
            exception, traceback_str = result
            print(f"An assert error occurred in the function:{exception}")
            print(traceback_str)
            assert False