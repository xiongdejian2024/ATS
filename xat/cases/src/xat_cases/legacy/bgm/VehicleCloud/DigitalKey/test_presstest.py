# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
# """
# @File         :test_charge_pile_open_charge_lid.py
# @Time         :2023/1/31 17:54:31
# @Author       :jiabin.zhu@jiduauto.com
# @Description  :
# """
# import os
# import sys
# import hashlib

# sys.path.append(os.getcwd())
# sys.path.append(os.path.join(os.getcwd(), ""))
# sys.path.append(os.path.join(os.getcwd(), ".."))
# sys.path.append(os.path.join(os.getcwd(), "../.."))
# PRECHECKTI = 1

# from test_case.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *
# from sdk_interface.abc_interface import *

# @allure.feature("互联服务")
# @allure.story("数字钥匙和账号/其他/SE")
# class TestDigitalKeyDID(TestDigitalKeyBase):

#     def before_class(self,ecu):
#         super().before_class(self, ecu)
#         pass

#     def after_class(self, ecu):
#         super().after_class(self, ecu)

#     def before_each_func(self, ecu):
#         pass
    
#     def after_each_func(self, ecu):
#         pass
    
    
    
#     #压力测试NFC和蓝牙解闭锁
#     def test_caseid_1987505(self):
#         self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
#         sleep(3)
#         self.bus_comm.dk.set_cenlock_sts(1) #NFC解锁
#         sleep(5)
#         self.bus_comm.dk.set_cenlock_sts(3) #NFC闭锁
#         sleep(5)
#         self.bus_comm.dk.send_rke_unlock()  #RKE解锁
#         self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
#         self.bus_comm.dk.ck_four_door_lock_cmd(1)
#         self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
#         self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,exp_trigsrc=LockTrigerSource.KeyRem)
#         sleep(1)
#         self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)
#         sleep(5)
#         self.bus_comm.dk.send_rke_lock()   #RKE闭锁
#         self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
#         self.bus_comm.dk.ck_four_door_lock_cmd(2)
#         self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
#         self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,exp_trigsrc=LockTrigerSource.KeyRem)
#         self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)
#         sleep(5)

        
      