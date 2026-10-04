# 多进程 test
# from ecu_simulator.sdk.driver.tosun.libTSCANAPI import *
# from ecu_simulator.sdk.driver.tosun import libTSCANAPI
from multiprocessing import Process
from threading import Thread
from time import sleep


def test_func1():
    from xat_ecu.legacy.sdk.driver.tosun.libTSCANAPI.TSCommon import (
        initialize_lib_tscan,
        tsapp_connect,
        size_t,
        finalize_lib_tscan,
        tsapp_disconnect_by_handle,
    )

    ADeviceHandle1 = size_t(0)
    can = b"604B84C2E4BAF6CF"
    initialize_lib_tscan(True, True, False)  # 函数初始化
    print("11111111111111111111111111111111111")
    tsapp_connect(can, ADeviceHandle1)
    print("222222222222222222222222222222222222222")
    sleep(5)
    tsapp_disconnect_by_handle(ADeviceHandle1)


def test_func2():
    from xat_ecu.legacy.sdk.driver.tosun.libTSCANAPI.TSCommon import (
        initialize_lib_tscan,
        tsapp_connect,
        size_t,
        finalize_lib_tscan,
    )

    ADeviceHandle2 = size_t(0)
    fr = b"615784C2E4BAF7DB"
    initialize_lib_tscan(True, True, False)  # 函数初始化
    print("33333333333333333333333333333333333333333")
    tsapp_connect(fr, ADeviceHandle2)
    print("444444444444444444444444444444444444444444")
    sleep(10)

    print("5555555555555555555555555555555555")
    finalize_lib_tscan()
    print("666666666666666666666666666666666666666666666")

    # stop()


def stop():
    from xat_ecu.legacy.sdk.driver.tosun.libTSCANAPI.TSCommon import (
        initialize_lib_tscan,
        tsapp_connect,
        size_t,
        finalize_lib_tscan,
    )

    print("5555555555555555555555555555555555")
    finalize_lib_tscan()
    print("666666666666666666666666666666666666666666666")


if __name__ == "__main__":
    # worke dir: ecu_simulator/

    # ADeviceHandle1 = size_t(0)
    # initialize_lib_tscan(True, True, False)  # 函数初始化
    # print("3333333333333333333333333333333333")
    # tsapp_connect(can, ADeviceHandle1)
    # print("4444444444444444444444444444444444444")

    # process1 = Process(target=test_func1, name="fr", daemon=True)
    # process2 = Process(target=test_func2, name="fr", daemon=True)
    # process1.start()
    # process2.start()

    thread1 = Thread(target=test_func1, name="can", daemon=True)
    process2 = Process(target=test_func2, name="fr", daemon=True)

    process2.start()  # 必需先起进程
    thread1.start()  # 目前把这注解了，才可以run起来

    sleep(20)

    # thread1.join(10)
    # process2.join(10)  # 回收，释放资源
    print("888888888888888888888888888888888888888888888888888888")
    process3 = Process(target=test_func2, name="fr3", daemon=True)
    process3.start()
    print("999999999999999999999999999999999999999999999999999999")

    sleep(20)

    # print("5555555555555555555555555555555555")
    # finalize_lib_tscan()
    # print("666666666666666666666666666666666666666666666")

    print("7777777777777777777777777777777777777777777777777")
