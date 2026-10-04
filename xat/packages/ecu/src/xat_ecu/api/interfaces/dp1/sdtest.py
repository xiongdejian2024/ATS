#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :sdtest.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :诊断仪能力模拟 实现接口
"""
from xat_ecu.api import CommonSdTest
from xat_ecu.api.common.common import *
from xat_ecu import reporting as allure
import socket
from xat_ecu.legacy.sdk.diagnosis.uds_securitycal import SecurityAlgorithm
from xat_ecu.legacy.sdk.diagnosis.aes_128_cbc import Aes128
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.sdk.bgm_crc import calc_crc_f106
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.sdk.sdk_tools import *
flash_count=0


class SdTest(CommonSdTest):
    def change_usage_mode(self, usage_mode: UsageMode, do_assert: bool = True):
        self.sd_tester.update_serverdoipid(0x1002)
        return self.sd_tester.change_usage_mode(mode_type=usage_mode.value, do_assert=do_assert)

    def change_car_mode(self, car_mode: CarMode, do_assert: bool = True):
        self.sd_tester.update_serverdoipid(0x1002)
        return self.sd_tester.change_car_mode(mode_type=car_mode.value, do_assert=do_assert)
    
    def write_ccp(self, ccp: dict):
        self.sd_tester.update_serverdoipid(0x1002)
        result,ccp_value=self.sd_tester.write_multi_ccp(ccp)
        return result,ccp_value

    def read_bgm_mcu_version(self):
        self.sd_tester.update_serverdoipid(0x1002)
        return self.sd_tester.read_mcu_version_or_check()

    def read_bgm_boot_version(self):
        self.sd_tester.update_serverdoipid(0x1002)
        return self.sd_tester.read_boot_version_or_check()

    def read_bgm_switch_version(self):
        self.sd_tester.update_serverdoipid(0x1001)
        return self.sd_tester.read_switch_version_or_check()
    
    def diag_cancel(self):
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.send_data([0x31,0x01,0xA1,0x02])
        logger.info("send FOTA diag cancel")
        time.sleep(0.5)
        
    def enter_bgm_default_session(self):
        self.send_data_and_check(0x1001, [0x10, 0x01], '5001', diagnostic_action="enter_bgm_default_session")

    def enter_bgm_programming_session(self):
        self.send_data_and_check(0x1001, [0x10, 0x02],'5002', diagnostic_action="enter_bgm_programming_session")
    
    def enter_bgm_extended_session(self):
        self.send_data_and_check(0x1001, [0x10, 0x03], '5003', diagnostic_action="enter_bgm_extended_session")
    
    def manage_send_data(self,data):
        if isinstance(data,int):
            data_str = hex(data)[2:].replace(' ', "")
            send_data = [int(data_str[i:i + 2], 16) for i in range(0, len(data_str), 2)]
        elif isinstance(data,list):
            send_data = data
        elif isinstance(data,str):
            send_data = [int(data[i:i + 2], 16) for i in range(0, len(data), 2)]
        else:
            assert False,"请填写正确的发送数据格式"
        return send_data
    
    def mangage_check_data(self, ta, send_data, check_data):
        if isinstance(ta,int):
            if isinstance(check_data,list) and isinstance(check_data[0],int):#如果发送逻辑地址只有一个 检查返回值是列表，列表内元素是int
                for i in range(len(check_data)):
                    check_data[i] = hex(check_data[i])[2:] if len(hex(check_data[i])[2:]) % 2 == 0 else '0' + hex(check_data[i])[2:]
                check_data = "".join(check_data)
            elif isinstance(check_data,str):
                pass
            elif isinstance(check_data,dict):
                pass
            else:
                assert False,'请填写正确的预期结果数据格式'
        elif isinstance(ta,list):
            if isinstance(check_data,list) and isinstance(check_data[0],list):
                for i in range(len(check_data)):
                    for j in range(len(check_data[i])):
                        if isinstance(check_data[i][j], int):
                            check_data[i][j] = hex(check_data[i][j])[2:] if len(hex(check_data[i][j])[2:]) % 2 == 0 else '0' + hex(check_data[i][j])[2:]
                    check_data[i] = "".join(check_data[i])
            #如果发送逻辑地址超过1个 检查返回值是列表，列表内元素是str
            elif isinstance(check_data,list) and isinstance(check_data[0], str):
                pass
            else:
                assert False,f'请填写正确的预期结果数据格式 发送数据{send_data} 发送数据格式{type(send_data)}'
        return check_data
    
    def send_diag_data(self, ta, send_data, diagnostic_action):
        send_data_str = "".join([hex(i)[2:] if len(hex(i)[2:])%2==0 else '0' + hex(i)[2:] for i in send_data])
        if isinstance(ta,int):
            with allure.step(f"{hex(ta)}:发送数据:{send_data_str}"):
                self.sd_tester.update_serverdoipid(ta)
                # 功能寻址发送
                if ta==TA.FUNCTION:
                    self.sd_tester.send_data_to_functional_addressing(send_data)
                    return_result = self.sd_tester.client_sim.return_function_userdata_and_check_response()
                    retunr_result_dict={}
                    for key,value in return_result.items():
                        retunr_result_dict[key] = [v.replace(' ','').lower() for v in value]
                    payload = retunr_result_dict
                else:  
                    self.sd_tester.send_data(send_data)
                    return_result_list=self.sd_tester.return_udsdata_and_check_and_print_response_result(diagnostic_action)
                    return_result_str="".join(['0'+ hex(elemnt)[2:]  if len(hex(elemnt)[2:]) == 1 else hex(elemnt)[2:] for elemnt in return_result_list])
                    payload = return_result_str
        elif isinstance(ta,list):
            return_result_list=[]
            for t in ta:
                with allure.step(f"{hex(t)}:发送数据:{send_data_str}"):
                    self.sd_tester.update_serverdoipid(t)
                    self.sd_tester.send_data(send_data)
                    return_result=self.sd_tester.return_udsdata_and_check_and_print_response_result(diagnostic_action)
                    return_result_list.append(return_result)
            
            return_result_str_list=[]
            for retunr_result in return_result_list:
                return_result_str = "".join(['0' + hex(elemnt)[2:] if len(hex(elemnt)[2:]) == 1 else hex(elemnt)[2:] for elemnt in retunr_result])
                return_result_str_list.append(return_result_str)
            payload = return_result_str_list
        return payload
    
    def send_data_and_check(self,ta:int, data:str,check_data='',check_length=0,check_range=[],check_in=[],diagnostic_action: str="Diagnostic Action"):
        # 统一传入的data的类型
        send_data = self.manage_send_data(data)   
        # 统一传入check_data的类型   
        check_data = self.mangage_check_data(ta, send_data, check_data)
        # 发送数据并获取响应结果
        payload = self.send_diag_data(ta, send_data, diagnostic_action)
        # 将发送得到的返回值与期望值对比     
        if isinstance(ta,int) and isinstance(check_data,str):
            with allure.step(f"检查返回值与预期值是否符合要求"):
                if check_data:
                    with allure.step(f"{hex(ta)}:返回值{payload} 预期值{check_data} 检查返回值与预期值是否一致或预期值在返回值内"):
                        if len(check_data) <= len(payload):
                            assert check_data == payload[:len(check_data)], f"返回数据为{payload},而期望数据为{check_data},返回值与预期不一致"
                        else:
                            assert False, f"返回数据为{payload},而期望数据为{check_data},返回值与预期不一致"
                if check_length:
                    with allure.step(f"{hex(ta)}:检查返回值长度与预期长度是否一致"):
                        if len(payload) != check_length:
                            assert False, f"返回数据长度为{len(payload)},而期望数据长度为{check_length},返回值数据长度与预期数据长度不一致"
                
                if check_range:
                    with allure.step(f"{hex(ta)}:检查返回值范围是否与预期范围是否一致"):
                        if int(payload[6:],16) > check_range[0] and int(payload[6:],16) < check_range[1]:
                            assert True, f"返回数据为{int(payload[6:],16)},而期望数据范围是({check_range[0]},{check_range[1]}),返回值与预期范围不一致"
        elif ta == 0x1FFF and isinstance(check_data,dict):
            if check_data:
                with allure.step(f"{hex(ta)}:返回值{payload} 预期值{check_data} 检查返回值与预期值是否一致或预期值在返回值内"):
                    for key,value in check_data.items():
                        flag = False
                        for pay in payload[key]:
                            if value in pay:
                                if len(value) <= len(pay):
                                    flag = True
                        assert flag,f'预期值不在返回值内或者长度不符合预期'    
            if check_length:
                with allure.step(f"{hex(ta)}:检查返回值长度与预期长度是否一致"):               
                    for key,value in check_length.items():
                        flag = False
                        for pay in payload[key]:
                            if len(pay) == value:  
                                flag = True
                        assert flag,f'返回值{payload[key]}长度不符合预期'  
            if check_range:
                pass
                # todo：范围型返回值检查待做
                # with allure.step(f"{hex(ta)}:检查返回值范围是否与预期范围是否一致"):
                #     for key,value in check_data.items():
                #         flag = False
                #         for pay in payload[key]:
                #             if payload[6:] > check_range[0] and payload[6:] < check_range[1]:
                #                     flag = True
                #         assert flag, f"返回数据为{payload[6:]},而期望数据范围是({check_range[0]},{check_range[1]}),返回值与预期范围不一致" 
        elif isinstance(ta,list) and isinstance(check_data,list):
            if len(ta) != len(check_data):
                assert False,f'发送逻辑地址数量和预期数据数量不一致 TA:{len(ta)}个 check_data:{len(check_data)}个,请检查'
                
            if not isinstance(check_length,list):
                check_length=[]
                for i in range(0,len(check_data)):
                    check_length.append(0)
                    
            with allure.step(f"检查返回值与预期值是否符合要求"):
                for t,checkdata,returndata,datalength,checkrange,checkin in zip(ta,check_data,payload,check_length,check_range,check_in):
                    if checkdata:
                        with allure.step(f"{hex(t)}:返回值{returndata} 预期值{checkdata} 检查返回值与预期值是否一致或预期值在返回值内"):
                            if len(checkdata) <= len(returndata):
                                 assert checkdata == returndata[:len(checkdata)], f"返回数据为{returndata},而预期数据为{checkdata},返回值与预期不一致"
                            else:
                                assert False, f"返回数据为{returndata},而预期数据为{checkdata},返回值与预期不一致"
                    if datalength:
                        with allure.step(f"{hex(t)}:返回值长度{len(returndata)} 预期值长度{datalength} 检查返回值数据长度与预期数据长度是否一致"):
                            if len(returndata) != datalength:
                                assert False, f"返回数据{returndata} 长度为{len(returndata)},而预期数据长度为{datalength},返回值数据长度与预期数据长度不一致"

                    if checkrange:
                        with allure.step(f"{hex(ta)}:检查返回值范围是否与预期范围是否一致"):
                            if check_range[0] < int(self.payload[6:],16) < check_range[1]:
                                assert False, f"返回数据为{self.payload},而预期数据范围是({check_range[0]},{check_range[1]}),返回值与预期范围不一致"

                    if checkin:
                        with allure.step(f"{hex(ta)}:检查返回值是否在预期值范围内"):
                            if self.payload[6:] not in checkin:
                                assert False, f"返回数据为{self.payload} 返回值为{self.payload[6:]},而预期值范围是{checkin},返回值不在预期值范围内"            
        else:
            assert False,f"check_data:{check_data} unexpected type：{(type(check_data))}"        
        return payload

    def update_serverdoipid(self, doipid, ecu="BGM"):
        '''
        更新 逻辑地址
        @param doipid: 0x1001  0x1002
        @param ecu:
        @return:
        '''
        self.sd_tester.update_serverdoipid(doipid, ecu=ecu)

    def send_request_and_recv_response(self, msg, msg1=None, recv=True, do_assert=True, ):
        '''
        发送数据可以传递一个字符串，一个是列表，随机组合
        发送数据，是否接收返回值，根据recv 决定，是否直接报错 根据do_assert 决定
        @param msg: 发送的数据，可以是列表[0x10,0x01]，可以是16进制字符串1001/10 01，
         @param msg1: 发送的数据，可以是列表[0x10,0x01]，可以是16进制字符串1001/10 01，
        @param recv: 格式为字符串，列表 布尔 ；对接收的数据是否校验，True 只校验是否为正响应，传入具体的值，则会比较值是否相等
        @param do_assert:
        @param kwargs:
        @return: True/False ，[]
        '''
        return self.sd_tester.send_request_and_recv_response(msg=msg, msg1=msg1, recv=recv, do_assert=do_assert)

    def send_data(self, data, timeout=0.2):
        '''
           发送数据  列表里面需要是整型 或者发送数据内容，可以为列表（[0x10,0x01]），或者16进制字符传（1003）
           @param data: such as [0x10, 0x03] 或者  1003
           @return:
        '''
        if isinstance(data, list):
            send_data = data
        else:
            data = str(data).replace(" ", '').strip()
            send_data = [int(data[i:i + 2], 16) for i in range(0, len(data), 2)]
        self.sd_tester.send_data(send_data)
        time.sleep(timeout)

    def quit_boot(self, time_delay=20):
        '''
        退出boot
        @param time_delay: 重启后延时时间，单位为秒
        @return:
        '''
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86])
        if recv_data_list[:4] == [0x62, 0xf1, 0x86, 0x01]:
            return
        self.sd_tester.send_request_and_recv_response([0x10, 0x01])
        time.sleep(time_delay)
        # 校验
        self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86], recv=[0x62, 0xf1, 0x86, 0x01])

    def enter_boot(self, time_delay=10):
        '''
        退出 进入boot
        @param time_delay: 重启后延时时间，单位为秒
        @return:
        '''

        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86])
        if recv_data_list[:4] == [0x62, 0xf1, 0x86, 0x02]:
            return

        self.sd_tester.enter_program_session_functional_addressing()
        time.sleep(time_delay)
        # 校验
        self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86], recv=[0x62, 0xf1, 0x86, 0x02])

    def return_udsdata_and_check_and_print_response_result(self):
        '''
        发送诊断请求后，用来接收响应的
        返回一个列表 如 [0x71,0x01,0x02, 0x05,0x10,0x00,0x00,0x00,0x00,]
        @return:
        '''
        return self.sd_tester.return_udsdata_and_check_and_print_response_result()
    def session_ctrl_and_check(self, ta: int, session=SESSION.EMPTY, check_data='', check_length=0,
                                check_method=Check_Method.read):

        if session == SESSION.EMPTY:
            return
        if isinstance(ta, int):
            ta_list = [ta]
            check_data_list1 = [check_data]
        else:
            ta_list = ta
            check_data_list1 = check_data

        for index, ad_ress in enumerate(ta_list):
            self.update_serverdoipid(ad_ress)
            err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86])
            if recv_data_list[3] != session:
                self.sd_tester.send_request_and_recv_response([0x10, session], recv=[0x50, session])
                if (ad_ress==TA.BGM_MCU)and (session == SESSION.PROGRAMMING or recv_data_list[3] == SESSION.PROGRAMMING):
                    time.sleep(20)
            if check_method == Check_Method.read:
                if ad_ress==TA.TCAM:
                    sleep(0.04)
                self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86],recv=check_data_list1[index])
         
    def unlock_and_check(self,ta:int,session=SESSION.EMPTY,level=UnLock.L0,unlock_step=UnlockStep.key,constant=None,check_data='',check_length=0,check_range=[],check_in=[]):
        if level == UnLock.L0:
            if session:
                session_checkdata = f'62f1860{session}' if isinstance(ta,int) else [f'62f1860{session}']*len(ta)
                self.session_ctrl_and_check(ta,session,session_checkdata)
            return
        
        if isinstance(ta,list):
            if session==SESSION.EMPTY:
                session = SESSION.PROGRAMMING if level == UnLock.L1 else SESSION.EXTENDED
                session_checkdata = [f'62f18602']*len(ta) if level == UnLock.L1 else [f'62f18603']*len(ta)
            else:
                session_checkdata = [f'62f1860{session}']*len(ta)
        else:
            if session==SESSION.EMPTY:
                session = SESSION.PROGRAMMING if level == UnLock.L1 else SESSION.EXTENDED
                session_checkdata = f'62f18602' if level == UnLock.L1 else f'62f18603'
            else:
                session_checkdata = f'62f1860{session}'
                
        self.session_ctrl_and_check(ta,session,session_checkdata)
                        
        with allure.step(f"解锁安全等级{level}"):
            try:
                level_str='%02d' % level
                if unlock_step == UnlockStep.seed:
                    return_result=self.send_data_and_check(ta,f'27{level_str}',check_data)
                elif unlock_step == UnlockStep.key:
                    if isinstance(ta,list):
                        seed_list=self.send_data_and_check(ta,f'27{level_str}',[f'67{level_str}']*len(ta))
                        logger.info(f"************seed_list={seed_list}")
                        if seed_list.startswith("000000"):
                            return []
                        calculatedKey_list=[]
                        for t,seed in zip(ta,seed_list):
                            calculatedKey_list.append(self.caculate_key(t,level,seed[4:],constant))                            
                        return_result=[]
                        level_str='%02d' % (level+1)
                        for t,calculatedkey,checkdata,in zip(ta,calculatedKey_list,check_data):
                            return_result.append(self.send_data_and_check(t,[0x27,int('%02d' % (level+1),16)]+calculatedkey,checkdata))
                    else:
                        seed=self.send_data_and_check(ta,f'27{level_str}',f'67{level_str}')[4:]
                        logger.info(f"************seed={seed}")
                        if seed.startswith("000000"):
                            return []
                        calculatedKey=self.caculate_key(ta,level,seed,constant)
                        level_str='%02d' % (level+1)
                        return_result=self.send_data_and_check(ta,[0x27,int('%02d' % (level+1),16)]+calculatedKey,f'67{level_str}')
                else:
                    assert False,'请填入正确的解锁步骤'
            except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
                    assert False,f'安全等级{level}解锁失败 ERROR:{e}'
        return return_result
                       
    def read_did_and_check(self,ta:int,did:int,session=SESSION.EMPTY,check_data='',check_length=0,check_range=[],check_in=[]):
        session_checkdata = f'62f1860{session}' if isinstance(ta,int) else [f'62f1860{session}']*len(ta)
        self.session_ctrl_and_check(ta,session,session_checkdata)
        data = f'22{hex(did)[2:].zfill(4)}'
        with allure.step(f"读取DID:{hex(did)}"):
            return_result=self.send_data_and_check(ta,data,check_data,check_length,check_range,check_in)
        return return_result
    
    def write_did_and_check(self,ta:int,did:int,session=SESSION.EMPTY,unlock_level=UnLock.L0,write_data='',check_data='',check_length=0,check_range=[],check_in=[],check_method=Check_Method.reset,recover=True):   
        pass_status = True
        try:
            result_data = None
            did_str = hex(did)[2:].zfill(4)
            raw_data=self.read_did_and_check(ta,did,session)
            unlock_check_data =  '67' if isinstance(ta,int) else  ['67']*len(ta)
            self.unlock_and_check(ta,session,unlock_level,UnlockStep.key,constant=None,check_data=unlock_check_data)
            write_data = f'2E{did_str}{write_data}'
            
            with allure.step(f"写入DID:{did_str} 写入值:{write_data}"):
                if check_method == Check_Method.read:
                    wirte_checkdata= f'6e{did_str}' if isinstance(ta,int) else [f'6e{did_str}'] * len(ta)
                    self.send_data_and_check(ta,write_data,wirte_checkdata)
                    time.sleep(0.5)  #写入值后加等待0.5s时间再读 保证值已经被存储
                    result_data=self.read_did_and_check(ta,did,SESSION.EMPTY,check_data,check_length,check_range,check_in)    
                elif check_method == Check_Method.reset:
                    wirte_checkdata= f'6e{did_str}' if isinstance(ta,int) else [f'6e{did_str}'] * len(ta)
                    self.send_data_and_check(ta,write_data,wirte_checkdata)
                    self.reset_0x1181()
                    self.unlock_and_check(ta,session,unlock_level,UnlockStep.key,constant=None,check_data='67')
                    result_data=self.read_did_and_check(ta,did,SESSION.EMPTY,check_data,check_length,check_range,check_in)
                elif check_method ==Check_Method.response:
                    result_data=self.send_data_and_check(ta,write_data,check_data)
                else:
                    assert False,'请填入正确的检查方式'
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
            logger.error(f'ERROR:{e}')
            pass_status = False
        finally:            
            if recover:
                with allure.step(f"将DID:{did_str}值恢复为写入前的值"):
                    write_data = f'2E{did_str}{raw_data[6:]}'
                    self.send_data_and_check(ta,write_data,f'6e{did_str}')
                    time.sleep(0.5)  #写入值后加等待0.5s时间再读 保证值已经被存储
                    recover_data=self.read_did_and_check(ta,did,SESSION.EMPTY,raw_data)
                    if recover_data != raw_data:
                        logger.error(f'恢复值失败，返回数据为{recover_data},而期望数据为{raw_data},返回值与预期不一致')
            assert pass_status

        return result_data
                
    def io_ctrl_and_check(self, ta, did: int, io_type: int, session=SESSION.EMPTY, unlock_level=UnLock.L0,
                          write_data='', check_data='', check_length=0, check_range=[], check_in=[],
                          check_method=Check_Method.read, recover=True):
        try:
            did_str = hex(did)[2:].zfill(4)
            data = f'2F{did_str}{hex(io_type)[2:].zfill(2)}{write_data}'
            if session==SESSION.EMPTY:
                session = SESSION.PROGRAMMING if unlock_level == UnLock.L1 else SESSION.EXTENDED
            self.sd_tester.update_serverdoipid(ta)
            
            ret_code, ret_msg = self.sd_tester.send_request_and_recv_response(msg=[0x22, 0xf1, 0x86],
                                                                              recv=[0x62, 0xf1, 0x86])
            if ret_msg[3] != session:
                self.sd_tester.send_request_and_recv_response(msg=[0x10, session],
                                                              recv=[0x50, session])
                if (ta==TA.BGM_MCU)and (session == SESSION.PROGRAMMING or ret_msg[3] == SESSION.PROGRAMMING):
                    time.sleep(20)

            if unlock_level != UnLock.L0:
                with allure.step(f"进行27 解锁 "):
                    self.security_access(session, unlock_level, ta)
            with allure.step(f"写入IO Control DID:{did_str} 写入值:{write_data}"):
                if check_method == Check_Method.read:
                    write_checkdata = f'6f{did_str}' if isinstance(ta, int) else [f'6f{did_str}'] * len(ta)
                    self.send_request_and_recv_response(data, recv=write_checkdata)
                    time.sleep(0.5)
                    self.send_request_and_recv_response([0x22], msg1=did_str, recv=check_data)

                elif check_method == Check_Method.response:
                    self.update_serverdoipid(ta)
                    self.send_request_and_recv_response(data, recv=check_data)
                else:
                    logger.info(f"unexpected check_method")
                    assert False

        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
            logger.info(f"ERROR:{e}")
            assert False, f"{str(e)}"
        # finally:
        #     if recover:
        #         self.unlock_and_check(ta, session, unlock_level, UnlockStep.key, constant=None, check_data='67')
        #         with allure.step(f"将IO Control:{hex(did)[2:]}退出诊断控制"):
        #             data = f'2F{did_str}00'
        #             write_checkdata = f'6f{did_str}' if isinstance(ta, int) else [f'6f{did_str}'] * len(ta)
        #             self.send_data_and_check(ta, data, write_checkdata)
        #             time.sleep(1)
        #     return result_data
                 
    def routine_ctrl_and_check(self, ta, did: int, routine_type: int, session=SESSION.EMPTY, unlock_level=UnLock.L0,
                                write_data='', check_data='', check_length=0, check_range=[], check_in=[]):
        data = f'31{hex(routine_type)[2:].zfill(2)}{hex(did)[2:].zfill(4)}{write_data}'
        unlock_check_data = '67' if isinstance(ta, int) else ['67'] * len(ta)
        self.unlock_and_check(ta, session, unlock_level, UnlockStep.key, constant=None, check_data=unlock_check_data)
        with allure.step(f"写入Routine Control:{hex(did)[2:].zfill(4)} 写入值:{write_data}"):
            result_data = self.send_data_and_check(ta, data, check_data, check_length, check_range, check_in)

        return result_data


    def control_dtc_setting_and_check(self,ta,setting_type:int,session=SESSION.EMPTY,unlock_level=UnLock.L0,check_data='',check_length=0,check_range=[],check_in=[]):  
        data = f'85{hex(setting_type)[2:].zfill(2)}'
        unlock_check_data =  '67' if isinstance(ta,int) else  ['67']*len(ta)
        self.unlock_and_check(ta,session,unlock_level,UnlockStep.key,constant=None,check_data=unlock_check_data)
        with allure.step(f"写入Control DTC Setting:85 {hex(setting_type)[2:]}"):
            result_data=self.send_data_and_check(ta,data,check_data,check_length,check_range,check_in)
        return result_data
    
    def clear_all_dtc_and_check(self, ta, session=SESSION.EMPTY, unlock_level=UnLock.L0, check_data='', check_length=0, check_range=[], check_in=[]):
        self.session_ctrl_and_check(ta,session)
        self.unlock_and_check(ta,session,unlock_level,UnlockStep.key,constant=None,check_data='67')
        with allure.step(f"Clear DTC：14FFFFFF"):
            result_data=self.send_data_and_check(ta,'14ffffff',check_data,check_length,check_range,check_in)
        return result_data
    
    def communication_control_and_check(self,ta,control_did:int,control_type=None,session=SESSION.EMPTY,unlock_level=UnLock.L0,check_data='',check_length=0,check_range=[],check_in=[]): 
        # self.session_ctrl_and_check(ta,session)
        data = f'28{hex(control_did)[2:].zfill(2)}{hex(control_type)[2:].zfill(2)}'
        unlock_check_data =  '67' if isinstance(ta,int) else  ['67']*len(ta)
        self.unlock_and_check(ta,session,unlock_level,UnlockStep.key,constant=None,check_data=unlock_check_data)
        with allure.step(f"Communication Control：28 {control_did} {control_type}"):
            result_data=self.send_data_and_check(ta,data,check_data,check_length,check_range,check_in)
        return result_data
    
    def read_dtc_and_check(self,ta,sub_did=int,dtc_did:int=None,dtc_type=int,session=SESSION.EMPTY,check_data='',check_length=0,check_range=[],check_in=[]): 
        self.session_ctrl_and_check(ta,session)
        dtc_did = '' if not dtc_did else  hex(dtc_did)[2:] if len(hex(dtc_did)[2:])%2==0 else '0' +hex(dtc_did)[2:]
        sub_did = hex(sub_did)[2:] if len(hex(sub_did)[2:])%2==0 else '0' +hex(sub_did)[2:]
        dtc_type= hex(dtc_type)[2:] if len(hex(dtc_type)[2:])%2==0 else '0' +hex(dtc_type)[2:]
        data = '19' + sub_did+ dtc_did + dtc_type
        with allure.step(f"DTC：19 {sub_did} {dtc_did} {dtc_type}"):
            result_data=self.send_data_and_check(ta,data,check_data,check_length,check_range,check_in)
        return result_data
    
    def close_fireware(self):
        try:
            return_result=self.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.DEFAULT,'62b165')
            if return_result[6:] == '02':
                logger.info("防火墙已关闭")
            else:
                logger.info("防火墙打开状态，关闭防火墙")
                self.routine_ctrl_and_check(TA.BGM_SOC,0xA040,0x01,SESSION.EXTENDED,UnLock.L7,'02ff','7101a040')
                return_result=self.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.DEFAULT,'62b165')
                if return_result[6:] == '02':
                    logger.info("防火墙关闭成功")
                else:
                    assert False,'关闭防火墙失败'
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
            logger.info(f"关闭防火墙失败 ERROR:{e}")
            assert False
            
    def get_mcu_cpuload(self):
        '''
        返回 cpu load
        @return:
        '''
        try:
            self.update_serverdoipid(0x1002)
            self.send_data([0x22, 0xdb, 0x02])
            return_result_list = self.return_udsdata_and_check_and_print_response_result()
            cpuload_list = return_result_list[3:]
            cpuload1 = cpuload_list[0]
            cpuload2 = cpuload_list[1]
            cpuload3 = cpuload_list[2]
            cpuload4 = cpuload_list[3]
            string = f'核0:50ms内mcu当前负载:{cpuload1}%  50ms内mcu峰值负载:{cpuload2}% 500ms内mcu当前负载:{cpuload3}% 500ms内mcu峰值负载:{cpuload4}%'
            with allure.step(string):
                logger.info(string)

            cpuload1 = cpuload_list[4]
            cpuload2 = cpuload_list[5]
            cpuload3 = cpuload_list[6]
            cpuload4 = cpuload_list[7]
            string = f'核1:50ms内mcu当前负载:{cpuload1}%  50ms内mcu峰值负载:{cpuload2}% 500ms内mcu当前负载:{cpuload3}% 500ms内mcu峰值负载:{cpuload4}%'
            with allure.step(string):
                logger.info(string)
            return cpuload_list
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
            logger.error(f"读取cpu load 失败 ERROR：{e}")
            return []

    def get_ecu_core_assembly_part_number(self):
        return_result=self.read_did_and_check(TA.BGM_MCU,0xF1AA,SESSION.DEFAULT,'62f1aa')
        return return_result[6:]
    
    def get_ecu_delivery_assembly_part_number(self):
        return_result=self.read_did_and_check(TA.BGM_MCU,0xF1AB,SESSION.DEFAULT,'62f1ab')
        return return_result[6:]
    
    def get_ecu_serial_number(self):
        return_result=self.read_did_and_check(TA.BGM_MCU,0xF18C,SESSION.DEFAULT,'62f18c')
        return return_result[6:]

    def get_vehicle_identification_number(self):
        return_result=self.read_did_and_check(TA.BGM_MCU,0xF190,SESSION.DEFAULT,'62f190')
        return return_result[6:]
    
    def get_mcu_software_part_number(self):
        return_result=self.read_did_and_check(TA.BGM_MCU,0xF1F0,SESSION.DEFAULT,'62f1f0')
        return return_result[6:]
    
    def get_primary_bootloader_software_part_number(self):
        return_result=self.read_did_and_check(TA.BGM_MCU,0xF1A5,SESSION.PROGRAMMING,'62f1a5')
        self.exit_muc_boot()
        return return_result[6:]
        
    def enter_mcu_boot(self,reconnect=True):
        with allure.step(f"进入BGM_MCU boot"):
            return_result=self.read_did_and_check(TA.BGM_MCU,0xf186,SESSION.EMPTY,'62f186')
            if return_result[6:] in ['01','03']:
                logger.info("BGM不在boot下 发送1002进入boot")
                self.sd_tester.stop_tester_present()
                payload=self.send_data_and_check(TA.BGM_MCU,'1002','5002')
                before= time.time()
                self.wait_vehicle_announcement(before_time=before,reset_type=0x1002)
                if reconnect:
                    self.sd_tester.tester_present()
                    return_result=self.read_did_and_check(TA.BGM_MCU,0xf186,SESSION.EMPTY,'62f186')
                    if return_result[6:] !='02':
                        assert False,'BGM进入boot失败'
            else:
                logger.info("BGM已经在boot下了")
            
            return payload
    
    def exit_muc_boot(self,reconnect=True):
        with allure.step(f"退出BGM_MCU boot"):
            return_result=self.read_did_and_check(TA.BGM_MCU,0xf186,SESSION.EMPTY,'62f186')
            if return_result[6:] == '02':
                logger.info("BGM在boot下 发送1181退出boot")
                self.sd_tester.stop_tester_present()
                self.send_data_and_check(TA.FUNCTION,'1181')
                before = time.time()
                self.wait_vehicle_announcement(before_time=before,reset_type=0x1181)
                if reconnect:
                    self.sd_tester.tester_present()
                    return_result=self.read_did_and_check(TA.BGM_MCU,0xf186,SESSION.EMPTY,'62f186')
                    if return_result[6:] !='01':
                        assert False,'BGM退出boot失败'
            else:
                logger.info("BGM不在boot下")
                
    def reset_0x1082(self,reconnect=True):
        with allure.step(f"发送1082重启BGM"):
            self.sd_tester.stop_tester_present()
            self.send_data_and_check(TA.FUNCTION,'1082')
            before = time.time()
            self.wait_vehicle_announcement(before_time=before,reset_type=0x1082)
            if reconnect:
                self.sd_tester.tester_present()
                return_result=self.read_did_and_check(TA.BGM_MCU,0xf186,SESSION.EMPTY,'62f186')
                if return_result[6:] !='02':
                    assert False,'BGM重启进入boot失败'
    
    def reset_0x1181(self,reconnect=True, reboot_TA=TA.FUNCTION):
        with allure.step(f"向{reboot_TA}发送1181重启指令"):
            self.sd_tester.stop_tester_present()
            self.sd_tester.update_serverdoipid(reboot_TA)
            self.sd_tester.send_data([0x11,0x81])
            before = time.time()
            self.wait_vehicle_announcement(before_time=before,reset_type=0x1181)
            if reconnect:
                self.sd_tester.tester_present()
                return_result=self.read_did_and_check(TA.BGM_MCU,0xf186,SESSION.EMPTY,'62f186')
                if return_result[6:] !='01':
                    assert False,'BGM重启后进入app失败'
                
    def change_usagemode_a_to_b(self, usage_mode_a:UsageMode, usage_mode_b:UsageMode, wait_time:Union[int,float]=1):
        promt_info = f"---------------->将UsageMode从{usage_mode_a.name}切到{usage_mode_b.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.sd_tester.change_usage_mode(usage_mode_a.value)
            time.sleep(wait_time)
            self.sd_tester.change_usage_mode(usage_mode_b.value)

    def write_sensor_id(self, tpms_id:list, do_assert:bool=True, **kwargs):
        promt_info = f"---------------->写4轮传感器ID，胎压ID为{tpms_id}"
        with allure.step(promt_info):
            logger.info(promt_info)
            time.sleep(0.3)
            self.sd_tester.diagnostic_session_check()
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
                "Send f186 to get result"
            )[3:]
            curr_status = result[-1]
            if curr_status != 0x03:
                # 进入扩展会话
                self.sd_tester.enter_extended_session()
                result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
                    "Send 1003 to get result"
                )
                if do_assert and result[0] != 0x50:
                    assert 0, f'enter_extended_session 失败'
                self.sd_tester.security_access_level_l3()
            else:
                # 判断是否需要解锁
                self.sd_tester.client_sim.send_data([0x27, 0x05])
                result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
                    "Send 0x27, 0x09 to get result"
                )
                curr_le = result[2:]
                if curr_le != [0x00, 0x00, 0x00]:
                    # 五级 27 解锁
                    self.sd_tester.security_access_level_l3()
            # 写入DID
            self.sd_tester.send_data([0x2E, 0x28, 0x1F] + tpms_id)
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
                "Write all zero clear sensor"
            )
            curr_status = result[0]
            if do_assert and curr_status != 0x6E:
                assert 0, f'写入did失败'

    def check_tpms_id(self,response: list, tpms_id: list, is_null: bool):
        """
        检查自定位后胎压ID是否和预期一致
        :param response: 诊断22 28 1f的响应
        :param tpms_id: 预期的胎压ID
        :param is_null:是否判断为全0
        :return:
        """
        l = len(response)
        is_ture = 1
        k = 0
        j = 0
        cnt1 = 0
        cnt2 = 0
        if l == 16:
            if is_null == True:
                while k < l - 1:
                    if response[k] != 0:
                        is_ture = 0
                    k = k + 1
            else:
                for j in range(4):
                    while k < l - 1:
                        for i in range(4):
                            if response[k + i] == tpms_id[i + 4 * j]:
                                cnt1 += 1
                        if cnt1 == 4:
                            cnt2 += 1
                            cnt1 = 0
                        else:
                            cnt1 = 0
                        k = k + 4
                    k = 0
                if cnt2 == 4:
                    is_ture = 1
                else:
                    is_ture = 0
        else:
            is_ture = 0
        if is_ture == 1:
            assert 1, "tpms_id与预期一致"
        else:
            assert 0, "tpms_id与预期不一致"

    def check_dtc(self,response: list, DTC: list, status: hex):
        l = len(response)
        k = 0
        dtc_cnt = 0
        dtc_flag = 0
        dtc_zt = 0
        while k < l - 1:
            for i in range(3):
                if response[k + i] == DTC[i]:
                    dtc_cnt += 1
            if dtc_cnt == 3:
                dtc_flag = 1
                dtc_zt = response[k + 3]
            dtc_cnt = 0
            k = k + 4
        if dtc_flag == 1:
            assert dtc_zt & 9 == status, "DTC状态与预期不一致"
        else:
            if status == 0:
                logger.info("与预期一致DTC不存在")
            else:
                assert 0, "DTC不存在"

    def check_dtc_num(self,response: list):
        l = len(response)
        num = l / 4
        if num > 20:
            status1 = 1
            status2 = 0
        else:
            status1 = 9
            status2 = 8
        return status1, status2
    
    def send_dtc_request_and_return_check_status(self):
        promt_info = f"---------------->发送读DTC请求并返回需要校验的DTC状态"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.sd_tester.send_data([0x19, 0x02, 0x09])
            logger.info("向1002发送  0x19, 0x02, 0x09")
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result()[3:]
            status1, status2 = self.check_dtc_num(result)
            logger.info(f'result为{result}，status1为{status1}，status2为{status2}')
            return result, status1, status2

    def send_dtc_request_and_check_dtc_status(self, DTC: list, status:hex):
        promt_info = f"---------------->发送读DTC请求并校验DTC状态"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.sd_tester.send_data([0x19, 0x02, 0x09])
            logger.info("向1002发送  0x19, 0x02, 0x09")
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result()[3:]
            self.check_dtc(result, DTC, status)

    def wait_vehicle_announcement(self,before_time=0,reset_type=None,timeout=60):
        bufsize = 1024
        addr = ('', 13400)
        udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpServer.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        udpServer.settimeout(timeout)
        udpServer.bind(addr)
        before = time.time()
        with allure.step(f"等待第一帧车辆公告发出"):
            logger.info("Waiting for Vehicle Announcement....")
            while (time.time() - before < timeout):
                try:
                    data,client_info = udpServer.recvfrom(bufsize)
                    if b'\x02\xfd\x00\x04' and b'\x10\x01'  in data:
                        strhex = ''
                        hexlist = []
                        for i in list(data):
                            if len(hex(i)) % 2 == 0:
                                hexlist.append(hex(i))
                            else:
                                hexlist.append('0x0' + hex(i)[2:])
                        for i in hexlist:
                            strhex += i[2:]
                        catch_time = time.time()
                        ip=client_info[0]
                        logger.info(f"获取到车辆公告 BGM:{ip}")
                        break
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
                    assert False,f"超时{timeout}s未收到车辆公告 ERROR:{e}"
            
            if time.time() - before > 60:
                assert False,f"超时{timeout}s未收到车辆公告 ERROR:{e}"
                
            #如果传入重启前的时间 表示要获取第一帧车辆公告发出时间与重启指令的间隔
            if before_time:
                interval = catch_time -before_time
                if reset_type==0x1181 :
                    logger.info(f'{hex(reset_type)[2:]}重启到第一条车辆公告发出时间间隔:{interval} 需求在20s内')
                elif reset_type==0x1082 or reset_type==0x1002:
                    logger.info(f'{hex(reset_type)[2:]}重启到第一条车辆公告发出时间间隔:{interval} 需求在16s内')
                else:
                    logger.info(f'{hex(reset_type)[2:]}重启到第一条车辆公告发出时间间隔:{interval}')
                return interval
            else:
                return catch_time        
        
    def hard_reset(self,ta,reconnect=True):
        with allure.step(f"Hard Reset: 1101"):
            self.sd_tester.stop_tester_present()
            result_data=self.send_data_and_check(ta,'1101','5101')
            before= time.time()
            self.wait_vehicle_announcement(before_time=before,reset_type=0x1101)
            if reconnect:
                self.sd_tester.tester_present()
        return result_data
    
    def soft_reset(self,ta,reconnect=True):
        with allure.step(f"Soft Reset: 1103"):
            self.sd_tester.stop_tester_present()
            result_data=self.send_data_and_check(ta,'1103','5103')
            before= time.time()
            self.wait_vehicle_announcement(before_time=before,reset_type=0x1103)
            if reconnect:
                self.sd_tester.tester_present()
        return result_data
            
    def caculate_key(self,ta,level,seed,constant=None):
        if level==UnLock.L1:
            real_leve=1
        elif level==UnLock.L3:
            real_leve=2
        elif level==UnLock.L5:
            real_leve=3
        elif level==UnLock.L7:
            real_leve=4
        elif level==UnLock.L11:
            real_leve=6
        
        if isinstance(seed,list):
            pass
        elif isinstance(seed,str):
            seed=[int(seed[i:i + 2], 16) for i in range(0, len(seed), 2)]
        else:
            assert False,"请填入正确格式seed值"
        
        if ta==TA.BGM_MCU or ta==TA.BGM_SOC:
            uds_security_cal = SecurityAlgorithm('BGM')
        elif ta==TA.TCAM:
            uds_security_cal = SecurityAlgorithm('TCAM')
        else:
            assert False,'接口只支持BGM/TCAM安全等级解锁'  #后期可扩展 目前只用到BGM和TCAM解锁
    
        if not constant:
            calculatedKey=list(uds_security_cal.get_calculated_key(real_leve,seed))
            logger.info(f'calculatedKey={calculatedKey}')
        else:
            if real_leve==4:
                cryptor_aes128 = Aes128(key=constant, iv="00000000000000000000000000000000")
                cryptor_aes128.update_key_hexstr(constant)
                calculatedKey = list(cryptor_aes128.encrypt(bytes(seed)))
            else:
                seed_bytes = int.from_bytes(seed, byteorder='little',signed=False)
                calculatedKey = list(uds_security_cal.cal_seed(seed_bytes,constant).to_bytes(3, 'little'))
            
        return calculatedKey

    def write_bncm_key(self,ta=TA.BGM_MCU,session=SESSION.EXTENDED,unlock_level=UnLock.L5,bncm_key=None):
        bncm_status=self.read_did_and_check(TA.BGM_MCU,0xd904,SESSION.DEFAULT,'62d904') #62d90400 未写入 or 62d90401 已写入
        if bncm_status == '62d90401':
            logger.info("值已经被写入先擦除BNCM值 再写入BNCM值")
            with allure.step(f"擦除BNCM值"):
                self.write_did_and_check(ta,0xd905,session,unlock_level,bncm_key,'6ed905',check_method=Check_Method.response,recover=False)
            with allure.step(f"读取D904状态确认是否已经被擦除 00是已经被擦除 01未被擦除"):
                self.read_did_and_check(ta,0xd904,SESSION.EMPTY,'62d90400')
            with allure.step(f"写入BNCM值"):
                self.write_did_and_check(ta,0xd903,session,unlock_level,bncm_key,'6ed903',check_method=Check_Method.response,recover=False)
            with allure.step(f"读取D904状态确认是否已经被写入 00是已经被擦除 01未被擦除"):
                self.read_did_and_check(ta,0xd904,SESSION.EMPTY,'62d90401')
            with allure.step(f"重启后再读取D904状态确认是否已经被写入"):
                self.reset_0x1181()
                self.read_did_and_check(ta,0xd904,session,'62d90401')
        elif bncm_status == '62d90400':
            logger.info("值未被写入 直接写入BNCM值")
            with allure.step(f"写入BNCM值"):
                self.write_did_and_check(TA.BGM_MCU,0xd903,session,unlock_level,bncm_key,'6ed903',check_method=Check_Method.response,recover=False)
            with allure.step(f"读取D904状态确认是否已经被写入 00是已经被擦除 01未被擦除"):
                self.read_did_and_check(TA.BGM_MCU,0xd904,SESSION.EMPTY,'62d90401')
            with allure.step(f"重启后再读取D904状态确认是否已经被写入"):
                self.reset_0x1181()
                self.read_did_and_check(TA.BGM_MCU,0xd904,SESSION.DEFAULT,'62d90401')
            
    def get_and_check_tpms_id(self,tpms_id: list, is_null: bool):
        self.sd_tester.send_data([0x22, 0x28, 0x1f])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result()[3:]
        #检查胎压IDpyt
        self.check_tpms_id(result, tpms_id, is_null)
        
    def get_bgm_app_soft_version(self):
        f1ae_info = self.read_did_and_check(TA.BGM_SOC,0xF1AE,SESSION.DEFAULT,'62f1ae')
        match = re.search(r'(?<=\b\w{8})\w{16}', f1ae_info)
        match1 = re.search(r'\d{10}', match.group(0))
        app_soft_version = f"{match1.group(0)} {chr(int(match.group(0)[-4:-2], 16))}{chr(int(match.group(0)[-2:], 16))}"
        return app_soft_version

    def get_bgm_pbl_soft_version(self):
        f1ae_info = self.read_did_and_check(TA.BGM_SOC, 0xF1AE, SESSION.DEFAULT, '62f1ae')
        match = re.search(r'62f1ae\w{16}$', f1ae_info)
        match1 = re.search(r'\d{10}', match.group(0))
        pbl_soft_version = f"{match1.group(0)} {chr(int(match.group(0)[-4:-2], 16))}{chr(int(match.group(0)[-2:], 16))}"
        return pbl_soft_version
    
    def get_bgm_hard_version(self):
        f1aa_info = self.read_did_and_check(TA.BGM_SOC, 0xF1AA, SESSION.DEFAULT, '62f1aa')
        match = re.search(r'62f1aa\w{16}$', f1aa_info)
        match1 = re.search(r'\d{10}', match.group(0))
        hard_version = f"{match1.group(0)} {chr(int(match.group(0)[-4:-2], 16))}{chr(int(match.group(0)[-2:], 16))}"
        return hard_version
    
    def get_tcam_hard_version(self):
        f1aa_info = self.read_did_and_check(TA.TCAM, 0xF1AA, SESSION.DEFAULT, '62f1aa')
        match = re.search(r'62f1aa\w{16}$', f1aa_info)
        match1 = re.search(r'\d{10}', match.group(0))
        hard_version = f"{match1.group(0)} {chr(int(match.group(0)[-4:-2], 16))}{chr(int(match.group(0)[-2:], 16))}"
        return hard_version

    def get_tcam_soft_version(self):
        f1ae_info = self.read_did_and_check(TA.TCAM, 0xF1AE, SESSION.DEFAULT, '62f1ae')
        match = re.findall(r"62f1ae01(\w{16})", f1ae_info)[0]
        tcam_soft_version = match[:10] + chr(int(match[-6:-4], 16)) + chr(int(match[-4:-2], 16)) + chr(int(match[-2:], 16))
        return tcam_soft_version

    def read_bgm_mpu_version(self):
        """
        读取 ecu 软件号
         返回 bgm mpu 和 boot 版本号
        """
        # ret_value, version = self.sd_tester.read_version_or_check(check_data)
        # return ret_value, version
        try:
            self.sd_tester.update_serverdoipid(0x1001)
            self.sd_tester.information_check_f1ae()
            # sleep(0.5)
            recv_data_list = self.sd_tester.return_udsdata_and_check_and_print_response_result(" 发送 f1ae 获取版本号")
            data_list = recv_data_list[3:]
            # 转化为16进制字符串
            data_hex = bytes(data_list).hex()
            # 判断是bgm 还是tcam
            # bgm   02 6160110110 41 41 43  296011005520 4158
            fr = chr(int(data_hex[0:2], 16))
            mid = data_hex[2:12]
            ver_str = data_hex[12:18]
            ver = ''.join([chr(int(ver_str[i:i + 2], 16)) for i in range(0, len(ver_str), 2)])
            mcu_ver = (mid + ver).upper()
            # boot 的 版本号
            boot_str = data_hex[18:]
            boot_head = boot_str[:10]
            boot_foot = boot_str[10:]
            bot = ''.join([chr(int(boot_foot[i:i + 2], 16)) for i in range(0, len(boot_foot), 2)])
            boot_ver = (boot_head + bot).upper()
            logger.info(f'获取的 bgm 版本为: {mcu_ver} 和 boot 版本为: {boot_ver}')
            return boot_ver, mcu_ver
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
            logger.error(f"读取 bgm mpu 版本号失败{str(e)}")
            return None, None

    
    def read_bms_did_value(self,did:[str,int],defaul_value:str,default_mode:bool = False):
        did_str = dealwithDID(did)
        did_int = int(did_str, 16)
        check_resp_read = "62" + did_str + defaul_value
        if default_mode == True:
            prompt_info = f"---------->获取BMS相关DID:{did_str}的默认值"
            with allure.step(prompt_info):
                logger.info(prompt_info)
                self.read_did_and_check(TA.BGM_MCU,did_int,SESSION.DEFAULT,str.lower(check_resp_read))
        else:
            prompt_info = f"---------->获取BMS相关DID:{did_str}的值"
            with allure.step(prompt_info):
                logger.info(prompt_info)
                self.read_did_and_check(TA.BGM_MCU,did_int,SESSION.EMPTY,str.lower(check_resp_read))

    
    def write_bms_did_value(self,did:[str,int],write_data:str,check_resp:Union[str,None] = None,out_range_value:Union[list,str,None] = None,wait_time:Union[float,int] = 0):
        did_str = dealwithDID(did)
        did_int = int(did_str, 16)
        self.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        prompt_info = f"---------->设置BMS相关DID:{did_str}的默认值"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            check_resp_pos = check_resp
            if out_range_value is not None:
                if isinstance(out_range_value,list):
                    for value in out_range_value:
                        self.write_did(TA.BGM_MCU,did_int,write_data=value,check_resp="7f2e31")
                else:
                    self.write_did(TA.BGM_MCU,did_int,write_data=out_range_value,check_resp="7f2e31")
            self.write_did(TA.BGM_MCU,did_int,write_data=write_data,check_resp=check_resp_pos)

        if wait_time != 0:
            logger.info(f"设置信号之后等待{wait_time}")
            sleep(wait_time)

    def reboot_bgm_by_diag_hardreset(self):
        self.reset_0x1181()
        self.stop_sd_tester()
        sleep(10)
        self.start_sd_tester()
    
    def recover_bms_did_to_default_value(self,did:[str,int],defaul_value:str):
        did_str = dealwithDID(did)
        did_int = int(did_str, 16)
        check_resp_write = "6e" + did_str
        check_resp_read = "62" + did_str + defaul_value

        self.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        self.write_did(TA.BGM_MCU,did_int,write_data=defaul_value,check_resp=check_resp_write)
        sleep(2)
        self.read_did(TA.BGM_MCU,did_int,check_resp=check_resp_read)
    
    def write_did(self,ta:TA,did:[str,int],write_data:str,check_resp:Union[str,None] = None):
        did_str = dealwithDID(did)
        did_int = int(did_str, 16)
        data = "2E" + did_str + write_data
        if check_resp is not None:
            self.send_data_and_check(ta,data,str.lower(check_resp))
        else:
            self.send_data_and_check(ta,did_int,"")

    def read_did(self,ta:TA,did:[str,int],check_resp:Union[str,None] = None,return_result:Union[bool,None] = False):
        did_str = dealwithDID(did)
        did_int = int(did_str, 16)
        data = "22" + did_str
        if check_resp is not None:
            payload = self.send_data_and_check(ta,data,str.lower(check_resp))
        else:
            payload = self.send_data_and_check(ta,did_int,"")
        
        if return_result == True:
            return payload 
        
    
    def dtc_read_and_check(self, dtc:DTCFault, dtc_sts:DTCSts, fault_sts:bool = True):
        prompt_info = f"---------->Check DTC:{dtc.value} 的 {dtc_sts.name}状态是否为{fault_sts}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            dtc_bytes = transferDTCtoBytes(dtc.value)
            diag_req = [0x19, 0x04] + dtc_bytes + [0x20]
            diag_resp = self.sd_tester.send_request_and_recv_response(diag_req)[1]
            sts = diag_resp[5]

            logger.info(f"--------->通过1904获取DTC:{dtc.value}的当前状态为{bin(sts)}")

            if sts & dtc_sts.value == dtc_sts.value and fault_sts == True:
                assert True
            elif sts & dtc_sts.value != dtc_sts.value and fault_sts == False:
                assert True
            else:
                assert False
    
    def stop_tester_present(self):
        self.sd_tester.stop_tester_present()

    def check_mcu_whether_in_boot(self):
        return_result=self.read_did_and_check(TA.BGM_MCU,0xf186,SESSION.EMPTY,'62f186')
        if return_result[6:] in ['01','03']:
            logger.info("BGM MCU 不在boot下")
            return False
        else:
            logger.info("BGM MCU 在boot下")
            return True
        
    def reset_bgm(self):
        logger.info("重启BGM, 等待30s")
        self.send_data_and_check(TA.BGM_MCU,'1181')
        time.sleep(30)   

    def reset_tcam(self):
        self.sd_tester.tester_present()
        self.send_data_and_check(TA.TCAM,'1001','5001')
        time.sleep(1)
        self.send_data_and_check(TA.TCAM,'1003','5003')
        time.sleep(1)
        result_data=self.send_data_and_check(TA.TCAM,'1103','5103')
        logger.info("重启TCAM, 等待180s")
        time.sleep(180)
        self.sd_tester.stop_tester_present()
        return result_data
    
    def read_ccp(self):
        '''
        读取ccp ，返回值去掉服务最后的校验位
        @return: 字符串，列表
        '''
        ccp_string, ccp_list = self.sd_tester.read_ccp()
        return ccp_string, ccp_list

    def write_single_ccp(self, ccp_index: int, value: int):
        """
        序号从 1开始 不是0
       写入单个ccp数据，写入第几个字节
       :param ccp_index: ccp序号，如#10, index从1开始
       :param value: 写入值
       :return:
        """
        return self.sd_tester.write_single_ccp(ccp_index, value)

    def write_multi_ccp(self, ccp_dict: dict):
        """
        序号从 1开始 不是0
        写入多个ccp数据，如果读取的和写入的值相同，则不进行写入
        :param ccp_dict: 写入的ccp，如{10：2, 20: 3}
        :return:
        """
        return self.sd_tester.write_multi_ccp(ccp_dict)

    def check_ccp_value(self, ccp_dict: dict):
        '''
        校验 ccp 是否和读取的一样
        @param ccp_dict:
        @return: 返回 Flase 则存在不匹配的
        '''
        ccp_string, ccp_list = self.sd_tester.read_ccp()
        error_flag = True
        for key, value in ccp_dict.items():
            if ccp_list[key - 1] != value:
                logger.error(f"第{key}字节值不一致，读取的值为{ccp_list[key - 1]}，期望值为{value}")
                error_flag = False
        return error_flag



    def security_access_level(self, level: int = UnLock.L3):
        '''
        27 解锁
         L0 = 0
        L1 = 1
        L3 = 3
        L5 = 5
        L7 = 7
        L11 = 11
        @param level:
        @return:
        '''
        if level not in [1, 3, 5, 7, 11]:
            logger.error(f"不存在当前解锁模式{level}")
            assert 0, f"不存在当前解锁模式{level}"
        if level == UnLock.L1:
            self.sd_tester.security_access_level_l1()
        elif level == UnLock.L3:
            self.sd_tester.security_access_level_l2()
        elif level == UnLock.L5:
            self.sd_tester.security_access_level_l3()
        elif level == UnLock.L7:
            self.sd_tester.security_access_level_l4()
            # elif level==UnLock.L9:
            #     self.sd_tester.security_access_level_l5()
        elif level == UnLock.L11:
            self.sd_tester.security_access_level_l6()
        else:
            pass
        assert self.sd_tester.assert_security_access()

    def security_access(self, session: int, level: int, doipid=0x1001):
        '''
        进入指定会话并解锁
        @param session:
        @param level:
        @param doipid:
        @return:
        '''
        if not (1 <= session <= 3):
            logger.error(f"不存在当前模式{session}")
            assert 0, f"不存在当前模式{session}"
        # SESSION.EXTENDED, UnLock.L3
        self.sd_tester.update_serverdoipid(doipid)
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response(msg=[0x22, 0xf1, 0x86],
                                                                          recv=[0x62, 0xf1, 0x86])
        curr_session = ret_msg[3]
        # 如果进入 boot 下
        if session == SESSION.PROGRAMMING:
            # 当前模式是boot
            if curr_session == session:
                self.sd_tester.send_data([0x27,  int(str(level),16)])
                result = self.return_udsdata_and_check_and_print_response_result()
                curr_le = result[2:]
                if curr_le != [0x00, 0x00, 0x00]:
                    # 三级 27 解锁
                    self.security_access_level(level)
            else:
                # 当前模式不是boot
                self.sd_tester.stop_tester_present()
                self.sd_tester.enter_program_session_functional_addressing()
                time.sleep(12)
                self.sd_tester.tester_present()
                # 检查会话
                self.sd_tester.send_request_and_recv_response(msg=[0x22, 0xf1, 0x86], recv=[0x62, 0xf1, 0x86, 0x02])
                # 解锁
                self.security_access_level(level)
        else:
            # 不是进入boot
            # 如果当前是boot 则需要退出boot
            if curr_session == SESSION.PROGRAMMING:
                self.sd_tester.stop_tester_present()
                self.sd_tester.send_request_and_recv_response(msg=[0x10, 0x01], recv=[0x50, 0x01])
                time.sleep(20)
                self.sd_tester.tester_present()
                self.sd_tester.send_request_and_recv_response(msg=[0x22, 0xf1, 0x86], recv=[0x62, 0xf1, 0x86, 0x01])
                # 进入 指定会话
                self.sd_tester.send_request_and_recv_response(msg=[0x10, session], recv=[0x50, session])
                self.security_access_level(level)
            else:
                # 不是boot
                if curr_session != session:
                    self.sd_tester.send_request_and_recv_response(msg=[0x10, session], recv=[0x50, session])
                    self.security_access_level(level)
                else:
                    self.sd_tester.send_data([0x27,  int(str(level),16)])
                    result = self.return_udsdata_and_check_and_print_response_result()
                    curr_le = result[2:]
                    if curr_le != [0x00, 0x00, 0x00]:
                        # 三级 27 解锁
                        self.security_access_level(level)

    def bgm_soc_send_data_and_check(self, send_data=[], expect_recv=[], do_assert=True):
        '''

        @param do_assert:
        @return:
        '''
        self.sd_tester.update_serverdoipid(0x1001)
        # 在app 下
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response(msg=[0x22, 0xf1, 0x86],
                                                                          recv=[0x62, 0xf1, 0x86])
        if ret_msg[3] == SESSION.PROGRAMMING:
            assert 0, "当前模式不在app 下在boot 下"
        self.security_access(SESSION.EXTENDED, UnLock.L5)
        # 进入 eol 模式
        # send_data = [0x22, 0xDA, 0x01]
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response(msg=send_data, recv=expect_recv,
                                                                          do_assert=False)
        if not ret_code:
            # 进入 eol 模式失败
            if do_assert:
                assert 0, f'发送 {bytes(send_data).hex()} 期望收到  {bytes(expect_recv).hex()} 失败！ '
            return ret_msg
        if ret_msg[:len(expect_recv)] != expect_recv:
            if do_assert:
                assert 0, f'发送 {bytes(send_data).hex()} 期望收到  {bytes(expect_recv).hex()} 失败！ '
        return ret_msg

    def bgm_soc_enter_ecu_eol_mode(self, do_assert=True):
        '''
        SOC enter ECU EOL mode
        @param do_assert:
        @return: 返回 接搜
        '''
        send_data = [0x31, 0x01, 0xDC, 0x00, 0x01]
        expect_recv = [0x71, 0x01, 0xDC, 0x00, 0x10]
        return self.bgm_soc_send_data_and_check(send_data, expect_recv, do_assert)

    def bgm_soc_quit_ecu_eol_mode(self, do_assert=True):
        '''
        SOC enter ECU EOL mode
        @param do_assert:
        @return:
        '''
        send_data = [0x31, 0x01, 0xDC, 0x00, 0x02]
        expect_recv = [0x71, 0x01, 0xDC, 0x00, 0x10]
        return self.bgm_soc_send_data_and_check(send_data, expect_recv, do_assert)

    def bgm_soc_ddr(self, do_assert=True):
        '''
        如果收到 Routine Status = completed 说明测试通过
        @param do_assert:
        @return:
        '''
        send_data = [0x31, 0x01, 0xDC, 0x01]
        expect_recv = [0x71, 0x01, 0xDC, 0x01, 0x10]
        return self.bgm_soc_send_data_and_check(send_data, expect_recv, do_assert)

    def bgm_soc_emmc(self, do_assert=True):
        '''
        如果收到 Routine Status = completed 说明测试通过
        @param do_assert:
        @return:
        '''
        send_data = [0x31, 0x01, 0xDC, 0x02]
        expect_recv = [0x71, 0x01, 0xDC, 0x02, 0x10]
        return self.bgm_soc_send_data_and_check(send_data, expect_recv, do_assert)

    def bgm_soc_emmc_checksum_verify(self, do_assert=True):
        '''
        如果收到 Routine Status = completed 说明测试通过

        @param do_assert:
        @return:
        '''
        send_data = [0x31, 0x01, 0xDC, 0x03]
        expect_recv = [0x71, 0x01, 0xDC, 0x03, 0x10]
        return self.bgm_soc_send_data_and_check(send_data, expect_recv, do_assert)


    def bgm_soc_gpio(self, do_assert=True):
        '''
        MCU 收到控制请求后，控制 GPIO 状态
        通过 MPU 侧的 DID 获取 GPIO 状态
        上位机比较控制的状态跟读取的状态是否一致，一致就认为测试通过

        @param do_assert:
        @return:
        '''
        send_data = [0x22, 0xDA, 0x02]
        # expect_recv=[0x62, 0xDA, 0x02, 0x09]
        expect_recv = [0x62, 0xDA, 0x02]
        return self.bgm_soc_send_data_and_check(send_data, expect_recv, do_assert)

    def bgm_soc_check_secure_boot_status(self, do_assert=True):
        '''
        如果收到 OK, 说明测试通过
        @param do_assert:
        @return:
        '''
        send_data = [0x22, 0xDA, 0x00]
        expect_recv = [0x62, 0xDA, 0x00, 0x00]
        return self.bgm_soc_send_data_and_check(send_data, expect_recv, do_assert)


    def write_ccp_and_check(self, ccp_info: [list, dict, str], restore=True, do_assert=True, **kwargs):
        '''
        写入ccp 并校验写入是否成功，最后恢复原来的ccp
        @param ccp_info:
         为list：列表为整数，不需要 2E F1 06 和最后的校验后
         为dict：写入的ccp，如{10：2, 20: 3}
                序号从 1开始 不是0
                写入多个ccp数据，如果读取的和写入的值相同，则不进行写入
         为 str ：16进制字符串，不需要 2E F1 06 和最后的校验后
        @param restore: 默认为True 会恢复原来的ccp 值
        @param do_assert:
        @param kwargs:
        @return: 返回 False 则是失败，True 则是成功
        '''
        self.sd_tester.update_serverdoipid(0x1002)
        # 读取ccp  方便后面进行恢复
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x06],
                                                                                 recv=[0x62, 0xF1, 0x06])
        ccp_original_value = recv_data_list[3:1556 + 3]

        write_cpp_flag = True
        # 写入ccp
        if isinstance(ccp_info, dict):
            self.sd_tester.write_multi_ccp(ccp_info)
            # time.sleep(1)
            # 校验写入 对不对
            ret = self.check_ccp_value(ccp_info)
            if not ret:
                write_cpp_flag = False
        else:
            logger.info("开始写入ccp")
            self.write_ccp_value(ccp_info)
            # time.sleep(1)
            # 校验写入的 对不对
            ccp_string, ccp_list = self.sd_tester.read_ccp()
            if isinstance(ccp_info, list):
                if ccp_list != ccp_info:
                    logger.error(" 列表格式 ccp 未写入成功")
                    write_cpp_flag = False
            else:
                ccp_info = ccp_info.replace(' ', "")
                if ccp_string.lower() != ccp_info.lower():
                    logger.error(" 字符串格式 ccp 未写入成功")
                    logger.error(f"读取的ccp长度{len(ccp_string)}为{ccp_string.lower()}")
                    logger.error(f"写入的ccp长度{len(ccp_info)} 值为{ccp_info.lower()}")
                    write_cpp_flag = False

        if restore:
            logger.info("开始恢复原来的ccp")
            self.write_ccp_value(ccp_original_value)
            err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x06],
                                                                                     recv=[0x62, 0xF1, 0x06])
            recv_cpp = recv_data_list[3:1556 + 3]
            if ccp_original_value != recv_cpp:
                logger.error("恢复ccp 失败")
            else:
                logger.info("恢复ccp 成功！")

        if do_assert:
            assert write_cpp_flag
        return write_cpp_flag

    def write_ccp_value(self, ccp_data: [str, list], **kwargs):
        '''
        写入ccp  可以带cheksum  也可以不带，不带会自己生成
        @param ccp_data:
            为list：列表为整数，不需要 2E F1 06 和最后的校验后
            为 str ：16进制字符串，不需要 2E F1 06 和最后的校验后
        @param ccp_len:
        @return:
        '''
        ccp_len = 1556  # 纯粹 ccp 内容
        self.update_serverdoipid(0x1002)
        if isinstance(ccp_data, str):
            ccp_data = ccp_data.replace(' ', "")
            ccp_data_list = [int(ccp_data[i:i + 2], 16) for i in range(0, len(ccp_data), 2)]
        elif isinstance(ccp_data, (list, tuple)):
            ccp_data_list = list(ccp_data)
        else:
            assert 0, "ccp 数据格式不对，本应为列表或者字符串"
        logger.info(f'写入的的ccp={bytes(ccp_data_list).hex()}')
        if ccp_data_list[0:3] == [0x2E, 0XF1, 0X06]:
            ccp_data_list = ccp_data_list[3:]

        if len(ccp_data_list) == ccp_len:
            crc = hex(calc_crc_f106(ccp_data_list))[2:].zfill(4)
            crc_list = DataTypeHanding.hexstr_to_inlist(crc)
        elif len(ccp_data_list) == ccp_len + 2:
            crc_list = ccp_data_list[-2:]
        else:
            assert 0, f"ccp 长度不对目前长度为{len(ccp_data_list)}"

        self.sd_tester.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])
        self.security_access_level(UnLock.L5)
        send_data = [0x2e, 0xF1, 0X06] + ccp_data_list + crc_list
        self.sd_tester.send_request_and_recv_response(send_data, recv=[0x6e, 0xF1, 0X06])
    
    def quit_usage_mode(self, do_assert: bool = True):
        self.sd_tester.update_serverdoipid(0x1002)
        return self.sd_tester.quit_usage_mode(do_assert=do_assert)
    
    def send_usagemode_statistics_times_request_and_return_check_value(self, usagemode_size: UsagemodeSize, usagemode_size2: UsagemodeSize = 0, is_flag: bool = False):
        promt_info = f"---------------->发送读指定usagemode统计次数并返回指定的统计次数"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.sd_tester.send_data([0x22, 0x43, 0x0E])
            logger.info("向1002发送  0x22, 0x43, 0x0E")
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result()[3:]
            if is_flag:
                count1, count2 = self.return_usagmode_count(result, usagemode_size, usagemode_size2, is_flag)
                logger.info(f'result为{result}，count1为{count1}，count2为{count2}')
                return count1, count2
            else:
                count1 = self.return_usagmode_count(result, usagemode_size)
                logger.info(f'result为{result}，count1为{count1}')
                return count1

    def return_usagmode_count(self,response: list, usagemode_size: UsagemodeSize, usagemode_size2: UsagemodeSize = 0, is_flag: bool = False):
        count1 = 0
        count1 = 0
        if is_flag:
            count1 = response[usagemode_size.value - 3] + response[usagemode_size.value - 2]*256
            count2 = response[usagemode_size2.value - 3] + response[usagemode_size2.value - 2]*256
            return count1, count2
        else:
            count1 = response[usagemode_size.value - 3] + response[usagemode_size.value - 2]*256
            return count1

    def return_usagmode_time(self,response: list, usagemode_value: UsagemodeValue):
        time1 = response[usagemode_value.value - 3] + response[usagemode_value.value - 2]*256 + response[usagemode_value.value - 1]*65536
        return time1

    def compare_a_and_b(self, count_a: int, count_b: int, num: int, count_c: int =0, count_d: int =0, num_2:int =0, is_flag: bool = False):
        if count_b -count_a == num:
            logger.info(f'历史值{count_a}与当前值{count_b}符合预期的增张{num}')
        else:
            assert 0, "计数和预期的值不一致"
        if is_flag:
            if count_d -count_c == num_2:
                logger.info(f'历史值{count_c}与当前值{count_d}符合预期的增张{num_2}')
            else:
                assert 0, "计数和预期的值不一致"

    def send_usagemode_statistics_time_request_and_return_check_value(self, usagemode_value: UsagemodeValue):
        promt_info = f"---------------->发送读指定usagemode统计时间并返回指定的统计时间"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.sd_tester.send_data([0x22, 0x43, 0x0F])
            logger.info("向1002发送  0x22, 0x43, 0x0F")
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result()[3:]
            time1 = self.return_usagmode_time(result, usagemode_value)
            logger.info(f'result为{result}，count1为{time1}')
            return time1
    def get_vehicle_model(self, **kwargs):
        '''
        获取车型 配置
        @param kwargs:
        @return:
        '''
        data_config = {
            0x01: "Mars",
            0x02: "Venus",
        }
        data_config2 = {
            0x00: "400v",
            0x02: "800v",
        }

        ccp_string, ccp_list = self.read_ccp()
        # 根据 判断车型  （CCP#950==0x01代表Mars  CCP#950==0x02代表 Venus)
        vehicle_model = ccp_list[950-1]  # Mars  还是 Venus
        # （CCP#962==0x02代表MCA 800v  CCP#962==0x00代表MCA 400v)
        vehicle_mca = ccp_list[962 - 1]  #
        logger.info(f"当前车型为{data_config.get(vehicle_model)} {data_config2.get(vehicle_mca)}")
        return vehicle_model, vehicle_mca

    def set_ccp(self,ccp_type="mars",ccp_vlaue=None):
        if ccp_type == "mars":
            #mars1
            ccp="A3 01 80 06 FD 03 02 01 A3 02 09 03 04 02 01 02 85 8B 06 01 00 04 05 02 03 00 00 02 04 8F 80 0C 01 01 03 01 02 01 82 02 01 02 16 01 07 01 01 01 00 04 01 02 02 85 89 02 02 01 02 09 02 7B 74 03 01 01 01 01 01 01 01 03 01 02 02 02 02 01 02 01 02 01 01 01 01 01 02 02 01 03 01 02 01 80 02 03 02 80 01 80 00 01 00 81 80 11 01 03 04 01 01 01 01 02 01 03 02 81 02 02 01 01 01 01 01 04 01 01 01 01 01 01 01 02 03 01 01 03 02 02 01 83 02 01 01 02 01 01 29 02 01 04 02 03 80 02 81 03 81 04 01 14 01 0A 80 01 01 01 02 01 02 02 03 82 05 02 05 01 02 02 01 01 80 04 01 02 01 01 01 02 02 03 01 01 01 03 02 02 03 04 02 04 02 01 01 01 03 02 0A 02 01 01 01 02 01 01 01 80 81 0A 01 02 04 01 07 07 0A 0A 07 07 0A 0A 00 00 04 00 01 02 02 02 01 01 01 01 80 03 03 01 02 00 00 00 02 02 02 01 02 02 04 02 01 01 02 00 00 00 01 03 00 01 03 00 01 81 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 01 01 00 00 00 00 00 00 00 01 00 01 01 00 00 02 01 00 00 80 00 00 00 00 84 03 01 03 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 02 01 80 01 02 01 01 01 01 01 02 01 03 02 01 80 01 80 02 02 02 01 01 01 02 05 03 80 01 06 01 03 01 10 01 00 03 03 01 00 00 00 00 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 01 03 01 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 01 01 00 00 00 00 02 04 03 02 01 01 01 02 02 02 04 82 01 02 01 01 02 03 02 03 01 01 02 02 01 01 01 01 01 02 02 02 04 01 02 01 01 01 01 01 03 02 00 00 02 80 02 02 02 01 01 02 01 02 02 01 02 03 01 03 02 02 01 01 01 01 01 01 01 01 00 01 04 01 02 01 02 05 02 02 02 04 08 08 08 08 03 02 01 04 02 01 02 02 01 01 01 02 01 01 01 03 01 01 01 00 00 00 00 00 00 01 02 03 01 02 01 10 03 01 01 01 02 02 02 01 01 03 01 04 02 04 01 01 01 01 01 02 03 03 05 05 02 00 01 01 02 01 01 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 02 01 02 02 01 01 02 01 01 01 01 01 00 01 04 00 00 00 02 01 00 02 01 01 04 04 00 00 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 02 05 08 08 02 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 01 02 01 02 02 02 02 01 02 02 02 01 01 01 02 01 01 02 02 01 01 02 01 02 02 01 02 01 01 01 01 02 01 01 01 01 02 01 01 01 01 01 02 01 01 01 00 01 01 01 01 01 02 02 02 01 01 01 01 02 01 01 01 01 01 01 02 02 01 02 02 01 01 02 01 01 01 00 01 01 01 01 01 01 01 02 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 02 01 01 01 01 02 02 00 00 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 00 01 01 01 01 01 01 02 02 02 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 02 02 02 02 02 02 01 02 02 02 01 02 02 02 01 01 02 02 01 01 02 02 02 02 01 01 00 02 02 02 02 02 01 02 02 02 01 02 00 01"
            self.write_ccp_value(ccp)
        elif ccp_type == "vnus":
            #vnus
            ccp="A3 01 81 06 FD 03 01 01 A2 02 09 03 04 02 01 02 85 8B 06 01 00 04 05 02 03 00 00 01 04 8F 80 0C 01 01 01 01 02 01 82 02 01 02 16 01 07 01 01 01 00 03 01 02 02 80 89 02 03 01 01 03 02 73 72 03 01 01 01 01 01 01 01 03 01 02 02 02 02 0A 01 01 02 01 02 01 01 01 02 02 01 03 01 02 01 80 02 03 02 80 01 80 00 00 00 81 80 11 01 03 04 01 01 01 01 02 01 03 02 80 01 02 01 01 01 01 01 04 01 01 01 01 01 01 01 02 03 01 01 03 02 02 01 83 02 01 01 02 01 01 29 02 01 04 02 03 80 02 82 03 03 04 01 14 03 0A 80 01 04 01 02 01 02 02 03 82 05 02 05 01 01 02 01 01 80 04 01 02 01 01 01 02 05 02 01 01 00 03 02 02 03 04 02 02 02 01 01 01 02 00 01 01 01 01 01 01 01 01 01 80 03 0A 01 01 04 06 07 07 0A 0A 07 07 0A 0A 00 00 04 00 00 02 01 01 01 01 01 02 80 03 03 01 02 00 00 00 02 02 02 01 02 02 04 00 01 01 02 00 00 00 01 03 00 00 01 00 00 81 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 00 00 00 00 00 00 00 00 00 00 01 00 01 01 00 00 02 00 00 00 80 00 00 00 00 84 03 01 01 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 02 01 80 01 02 01 01 01 01 01 02 01 03 02 01 80 01 80 02 02 01 01 01 01 01 05 03 80 02 06 01 03 01 10 00 00 02 03 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 01 03 01 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 03 02 01 00 00 00 00 00 85 04 01 02 02 02 01 02 02 02 04 85 01 02 01 01 02 80 04 03 01 01 02 02 01 03 01 01 01 02 02 02 04 01 02 01 01 01 01 01 03 00 00 00 01 80 02 02 01 01 02 02 01 02 02 02 01 02 01 03 02 02 01 01 01 01 01 01 01 01 00 01 03 01 02 01 01 05 02 03 03 04 01 01 01 01 03 01 01 04 02 01 02 01 01 01 01 02 01 01 01 01 01 01 01 00 00 00 00 00 00 01 02 03 01 02 01 10 03 01 01 01 02 01 02 01 01 03 01 04 01 04 01 01 01 01 01 02 01 03 01 05 02 00 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 01 01 01 01 01 02 01 01 01 01 02 06 00 00 01 01 04 01 01 00 00 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 03 02 02 08 01 00 00 01 02 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 01 02 02 01 01 02 02 02 02 02 02 02 02 01 02 02 01 02 01 02 02 02 02 01 02 02 02 02 01 02 02 02 02 02 02 01 02 02 01 02 02 01 02 01 01 01 01 02 01 01 01 01 02 01 01 01 00 01 02 01 01 01 00 01 01 01 01 01 02 02 02 01 01 01 02 02 01 01 01 01 01 01 02 02 01 02 02 01 01 01 01 01 01 00 01 01 01 01 01 01 01 02 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 02 02 01 01 01 01 02 02 00 00 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 00 01 01 01 01 01 01 02 02 02 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 02 02 02 01 02 02 02 01 02 02 01 01 01 02 02 01 01 02 02 02 02 02 01 00 02 02 02 02 02 01 02 02 02 01 02 00 01"
            self.write_ccp_value(ccp)

        if ccp_vlaue != None:
            self.sd_tester.write_ccp(ccp)

    
    def read_and_check_did_range_value(self,did:int,check_value_range:list):
        data_str = hex(did)[2:].replace(" ", "")
        did_data = [int(data_str[i : i + 2], 16) for i in range(0, len(data_str), 2)]
        send_data = [0x22] + did_data

        self.send_data(send_data)
        result = self.return_udsdata_and_check_and_print_response_result(f"向1002发送{send_data}")
        logger.info(f"获取DID的返回结果是{result}")
        if result[0] != 0x62:
            logger.info("获取的是否定响应")
            assert False
        else:
            diag_result = result[3:]
        
        lenth = len(diag_result)
        if lenth == 1:
            result  = diag_result
        elif lenth == 2:
            result  = diag_result[0]*(0xff+1) + diag_result[1]
        elif lenth == 3:
            result  = diag_result[0]*(0xffff+1) + diag_result[1]*(0xff+1) + diag_result[2]
        else:
            logger.info("响应长度超过3个Byte暂时没有考虑")
        
        if result >= check_value_range[0] and result <= check_value_range[1]:
            assert True
            logger.info("获取的值在期望范围之内")
            return result
        else:
            logger.info("获取的值不在期望范围之内")
            assert False
    
    def send_carmode_subtype_request_and_check_result_value(self, carmode_subtype:Carmode_subtype, do_assert:bool=True):
        promt_info = f"---------------->发送读carmode子模式的did并校验结果"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.sd_tester.diagnostic_session_check()
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
                "Send f186 to get result"
            )[3:]
            curr_status = result[-1]
            if curr_status != 0x03:
                # 进入扩展会话
                self.sd_tester.enter_extended_session()
                result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
                    "Send 1003 to get result"
                )
                if do_assert and result[0] != 0x50:
                    assert 0, f'enter_extended_session 失败'
                self.sd_tester.security_access_level_l2()
            else:
                # 判断是否需要解锁
                self.sd_tester.client_sim.send_data([0x27, 0x03])
                result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
                    "Send 0x27, 0x03 to get result"
                )
                curr_le = result[2:]
                if curr_le != [0x00, 0x00, 0x00]:
                    # 五级 27 解锁
                    self.sd_tester.security_access_level_l2()
            self.sd_tester.send_data([0x22, 0x43, 0xc4])
            logger.info("向1002发送  0x22, 0x43, 0xc4")
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result()[3:] 
            logger.info(f'读出来的值为{result[0]}')
            if result[0] == carmode_subtype.value:
                logger.info(f'读出来的值{result[0]}与期望的{carmode_subtype.value}一直')
            else:
                assert 0, "读出来的值与预期不一致"

    def compare_list(self, list_a: list, list_b: list, is_equal:bool = True):
        if (list_a[0] == None) or (list_b[0] == None):
            assert 0, "有一组值为空"
        if is_equal:
            if list_a == list_b:
                logger.info(f'存储的值与预期值一致')
            else:
                assert 0, "存储的值与预期值不一致"
        else:
            if list_a == list_b:
                assert 0, "存储的值与预期值一致"
            else:
                logger.info(f'存储的值与预期值不一致')

    def generate_dd01_list(self, read_list:list):
        max_list = [0x41, 0x89, 0x37]
        min_list = [0x0, 0x0, 0xff]
        min_list_2 = [0x0, 0x0, 0x0a]
        if read_list <= min_list:
            if read_list <= min_list_2:
                write_list = min_list
                check_list = write_list
            else:
                write_list = read_list
                write_list[2] = read_list[2] - 1
                check_list = write_list
        else:
        # 生成随机里程
            write_list = [random.randint(0, 255) for _ in range(3)]
            check_list1 = max(write_list, read_list)
            check_list = min(max_list, check_list1)
        return write_list, check_list
    
    def read_f155(self):
        sleep(1)#等待写入完成
        return re.search(r'\d{2}$', self.read_did_and_check(TA.BGM_SOC,0xF155,SESSION.DEFAULT,'62f155')).group()
    
    def write_bncm_key(self,ta=TA.BGM_MCU,session=SESSION.EXTENDED,unlock_level=UnLock.L5,bncm_key=None):
        bncm_status=self.read_did_and_check(TA.BGM_MCU,0xd904,SESSION.DEFAULT,'62d904') #62d90400 未写入 or 62d90401 已写入
        if bncm_status == '62d90401':
            logger.info("值已经被写入先擦除BNCM值 再写入BNCM值")
            with allure.step(f"擦除BNCM值"):
                self.write_did_and_check(ta,0xd905,session,unlock_level,bncm_key,'6ed905',check_method=Check_Method.response,recover=False)
            with allure.step(f"读取D904状态确认是否已经被擦除 00是已经被擦除 01未被擦除"):
                self.read_did_and_check(ta,0xd904,SESSION.EMPTY,'62d90400')
            with allure.step(f"写入BNCM值"):
                self.write_did_and_check(ta,0xd903,session,unlock_level,bncm_key,'6ed903',check_method=Check_Method.response,recover=False)
            with allure.step(f"读取D904状态确认是否已经被写入 00是未写入 01是写入"):
                self.read_did_and_check(ta,0xd904,SESSION.EMPTY,'62d90401')
            with allure.step(f"重启后再读取D904状态确认是否已经被写入"):
                self.reset_0x1181()
                self.read_did_and_check(ta,0xd904,session,'62d90401')
        elif bncm_status == '62d90400':
            logger.info("值未被写入 直接写入BNCM值")
            with allure.step(f"写入BNCM值"):
                self.write_did_and_check(TA.BGM_MCU,0xd903,session,unlock_level,'00112233445566778899aabbccddeeff','6ed903',check_method=Check_Method.response,recover=False)
            with allure.step(f"读取D904状态确认是否已经被写入 00是未写入 01是写入"):
                self.read_did_and_check(TA.BGM_MCU,0xd904,SESSION.EMPTY,'62d90401')
            with allure.step(f"重启后再读取D904状态确认是否已经被写入"):
                self.reset_0x1181()
                self.read_did_and_check(TA.BGM_MCU,0xd904,SESSION.DEFAULT,'62d90401')
            with allure.step(f"擦除BNCM值"):
                self.write_did_and_check(ta,0xd905,session,unlock_level,'00112233445566778899aabbccddeeff','6ed905',check_method=Check_Method.response,recover=False)
            with allure.step(f"读取D904状态确认是否已经被擦除 00是已经被擦除 01未被擦除"):
                self.read_did_and_check(ta,0xd904,SESSION.EMPTY,'62d90400')

    def get_bgm_soft_version(self):
        F1AE_info = self.read_did_and_check(TA.BGM_SOC, 0xF1AE, SESSION.DEFAULT, '62f1ae')
        logger.info(F1AE_info)
        app_version, pbl_version = re.findall(r"62f1ae02(\w{16})(\w{16})", F1AE_info)[0]
        app_version = app_version[:-6] + chr(int(app_version[-6:-4], 16)) + chr(int(app_version[-4:-2], 16)) + chr(int(app_version[-2:], 16))
        pbl_version = pbl_version[:-6] + chr(int(pbl_version[-6:-4], 16)) + chr(int(pbl_version[-4:-2], 16)) + chr(int(pbl_version[-2:], 16))
        return f"{app_version},{pbl_version}"
    
    def check_program_precondition(self,reverse_test_type = ""):
        logger.info("刷写step1:检查程序预置条件")
        with allure.step(f"刷写step1:检查程序预置条件"):
            if reverse_test_type == "上次刷写未进行复位":
                logger.info("上次刷写未进行复位")
                self.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 11':'7F3131','10 01':'7F3131'})
            else:
                self.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 11':'710102061001','10 01':'710102061001'})

    def enter_program_mode(self):
        logger.info("刷写step2:功能寻址请求进入program_session")
        with allure.step(f"刷写step2:功能寻址请求进入program_session"):
            self.sd_tester.update_serverdoipid(0x1FFF)
            self.send_data([0x10,0x82])
    
    def confirm_program_mode(self,doipid):
        logger.info("刷写step3:物理寻址请求进入program_session")
        with allure.step(f"刷写step3:物理寻址请求进入program_session"):
            self.sd_tester.update_serverdoipid(doipid)
            self.result = self.sd_tester.send_request_and_recv_response([0x10, 0x02])

    def diagnostic_session_check(self,doipid):
        logger.info("刷写step4:诊断会话校验")
        with allure.step(f"刷写step4:诊断会话校验"):
            self.sd_tester.update_serverdoipid(doipid)
            self.result = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x86], recv=[0x62, 0xF1, 0x86, 0x02])

    def infotainment_check(self,doipid):
        self.sd_tester.update_serverdoipid(doipid)
        logger.info("刷写step5.1:序列号Infotainment Check_ED 20")
        with allure.step(f"刷写step5.1:序列号Infotainment Check"):
            self.send_request_and_recv_response([0x22, 0xED, 0x20])
        logger.info("刷写step5.2:硬件号Infotainment Check_F1 AA")
        with allure.step(f"刷写step5.2:硬件号Infotainment Check"):
            self.send_request_and_recv_response([0x22, 0xF1, 0xAA])
        logger.info("刷写step5.3:总成号Infotainment Check_F1 AB")
        with allure.step(f"刷写step5.3:总成号Infotainment Check"):
            self.send_request_and_recv_response([0x22, 0xF1, 0xAB])
        logger.info("刷写step5.4:序列号Infotainment Check_F1 8C")
        with allure.step(f"刷写step5.4:序列号Infotainment Check"):
            self.send_request_and_recv_response([0x22, 0xF1, 0x8C])
        logger.info("刷写step5.5:Public Key Infotainment Check_D0 1C")
        with allure.step(f"刷写step5.5:Public Key Infotainment Check"):
            self.send_request_and_recv_response([0x22, 0xD0, 0x1C],recv=False)
    
    def unlocK_for_download(self,doipid,ecu):
        self.sd_tester.update_serverdoipid(doipid,ecu)
        logger.info("刷写step6:安全会话解锁")
        with allure.step(f"刷写step6:安全会话解锁"):
            self.security_access_level(level=1)

    def erase_memory(self,doipid,file_path):
        self.sd_tester.update_serverdoipid(doipid)
        logger.info("刷写step7:擦除内存")
        with allure.step(f"刷写step7:擦除内存"):
            self.file_size = os.path.getsize(file_path)
            logger.info("file_size is {}".format(self.file_size))
            self.first_address = 0
            self.memory_address = list(self.first_address.to_bytes(4, byteorder='big'))
            self.memory_size = list(self.file_size.to_bytes(4, byteorder='big'))
            # old
            # self.routine_control([0x01], [0xFF, 0x00], zz = [0x44] + self.memory_address + self.memory_size)
            # jidu
            self.result = self.send_request_and_recv_response([0x31,0x01] + [0xFF, 0x00] + self.memory_address + self.memory_size,recv=[0x71, 0x01, 0xFF, 0x00, 0x10])

    def request_download(self,doipid,file_path,compression_encryption_method=[0x00],reverse_test_type = "",**kwargs):
        self.sd_tester.update_serverdoipid(doipid)
        logger.info("刷写step8:请求下载")
        with allure.step(f"刷写step8:请求下载"):
            self.file_size = os.path.getsize(file_path)
            logger.info("file_size is {}".format(self.file_size))
            compression_encryption_method = compression_encryption_method
            self.first_address = kwargs.get('first_address',0)
            # self.first_address = 0x1FFF
            if self.file_size < 4 * 1024 * 1024 * 1024:
                length_format = [0x44]
                self.memory_address = list(self.first_address.to_bytes(4, byteorder='big'))
                self.memory_size = list(self.file_size.to_bytes(4, byteorder='big'))
            else:
                length_format = [0x88]
                self.memory_address = list(self.first_address.to_bytes(8, byteorder='big'))
                self.memory_size = list(self.file_size.to_bytes(8, byteorder='big'))
            # print('compression_encryption_method=',compression_encryption_method)
            # print('length_format=',length_format)
            # print('self.memory_address',self.memory_address)
            # print('self.memory_size',self.memory_size)
            if reverse_test_type == "skip_erase_memory":
                logger.info("跳过erase_memory")
                self.result = self.send_request_and_recv_response([0x34] + compression_encryption_method + length_format + self.memory_address + self.memory_size,recv=[0x7F, 0x34, 0x24])
                return
            elif reverse_test_type == "skip_request_download":
                self.sd_tester.client_sim.uds_client.max_bl = 1024
                logger.info("跳过request_download")
            else:
                self.result = self.send_request_and_recv_response([0x34] + compression_encryption_method + length_format + self.memory_address + self.memory_size,recv=True)
    
    def transfer_data(self,doipid,file_path,usr_block_length=1000000000,reverse_test_type = ""):
        self.sd_tester.update_serverdoipid(doipid)
        logger.info("刷写step9:数据传输")
        with allure.step(f"刷写step9:数据传输"):
            # Rely on  request_download
            if self.file_size:
                logger.info("client_sim.uds_client.max_bl = {}".format(self.sd_tester.client_sim.uds_client.max_bl))
                block_length = self.sd_tester.client_sim.uds_client.max_bl - 2
                with open(file_path, "rb") as f:
                    if (usr_block_length - 2) < block_length:
                        block_length = usr_block_length
                    # head_address = 0
                    self.end_address = 0
                    block_sequence_counter = 0
                    loop = 0
                    while self.end_address < self.file_size:
                        if block_sequence_counter == 255:
                            loop += 1
                            block_sequence_counter = 0
                        elif block_sequence_counter < 255:
                            block_sequence_counter += 1
                        else:
                            block_sequence_counter = 0

                        if  reverse_test_type == "跳过一段数据传输":
                            block_data = f.read(block_length)
                            self.end_address += block_length
                            block_sequence_counter -= 1
                            reverse_test_type = ""
                            continue

                        block_data = f.read(block_length)

                        #self.send_data([0x36] + [block_sequence_counter] + list(block_data))
                        if reverse_test_type == "skip_request_download":
                            logger.info("跳过request_download")
                            self.send_request_and_recv_response([0x36] + [block_sequence_counter] + list(block_data),recv=[])
                            break
                        elif reverse_test_type == "skip_transfer_data":
                            logger.info("跳过transfer_data")
                            break
                        elif reverse_test_type == "只传输一个数据块":
                            logger.info("只传输一个数据块")
                            self.send_request_and_recv_response([0x36] + [block_sequence_counter] + list(block_data),recv=[0x76,0x01])
                            break
                        elif reverse_test_type == "重复传一帧数据":
                            logger.info("重复传一帧数据")
                            self.send_request_and_recv_response([0x36] + [block_sequence_counter] + list(block_data),recv=[0x76,0x01])
                            step_log = "transfer_data ---- loop: {}   block_sequence_counter:{}".format(loop,
                                                                                                        block_sequence_counter)
                            self.send_request_and_recv_response([0x36] + [block_sequence_counter] + list(block_data),recv=[0x76,0x01])
                            step_log = "transfer_data ---- loop: {}   block_sequence_counter:{}".format(loop,
                                                                                                        block_sequence_counter)
                            reverse_test_type = ""
                        elif reverse_test_type == "传包过程36的blockindex序号错误":
                            logger.info("传包过程36的blockindex序号错误")
                            if block_sequence_counter == 1:
                                self.send_request_and_recv_response([0x36] + [block_sequence_counter] + list(block_data),recv=[0x76,0x01])
                                step_log = "transfer_data ---- loop: {}   block_sequence_counter:{}".format(loop,
                                                                                                            block_sequence_counter)
                            if block_sequence_counter == 2:
                                logger.info("跳过发送block_sequence_counter=2的包")
                                continue
                            elif block_sequence_counter == 3:
                                self.send_request_and_recv_response([0x36] + [block_sequence_counter] + list(block_data),recv=[0x7F,0x36,0x73])
                                break
                        elif reverse_test_type == "重复传一段数据":
                            logger.info("重复传一段数据")
                            if block_sequence_counter == 1:
                                self.send_request_and_recv_response([0x36] + [block_sequence_counter] + list(block_data),recv=[0x76,0x01])
                                block_data_temp = block_data
                            elif block_sequence_counter == 2:
                                self.send_request_and_recv_response([0x36] + [block_sequence_counter] + list(block_data),recv=[0x76,0x02])
                            elif block_sequence_counter == 3:
                                self.send_request_and_recv_response([0x36] + [block_sequence_counter] + list(block_data),recv=[0x76,0x03])   
                            elif block_sequence_counter == 4:
                                self.send_request_and_recv_response([0x36] + [0x01] + list(block_data_temp),recv=[0x7F,0x36,0x73])
                                break
                        elif reverse_test_type == "跳过一段数据传输":
                            logger.info("跳过一段数据传输")
                            if block_sequence_counter == 1:
                                self.send_request_and_recv_response([0x36] + [block_sequence_counter] + list(block_data),recv=[0x76,0x01])
                                self.end_address += block_length
                                reverse_test_type = ""
                        elif reverse_test_type == "错误的包":
                            logger.info("错误的包")
                            self.send_request_and_recv_response([0x36] + [block_sequence_counter] + list(block_data)[::-1])
                            self.end_address += block_length
                            #reverse_test_type = ""
                        elif reverse_test_type == "传输块大于最大允许的数据块长度":
                            logger.info("传输块大于最大允许的数据块长度")
                            block_data_temp = [0]*(block_length+1)
                            self.send_request_and_recv_response([0x36] + [block_sequence_counter] + block_data_temp,recv=[0x7F,0x36,0x31])
                            break
                        elif reverse_test_type == "传包过程中异常掉电":
                            logger.info("传包过程中异常掉电")
                            self.send_request_and_recv_response([0x36] + [block_sequence_counter] + list(block_data),recv=False, do_assert=False)
                            self.end_address += block_length
                            time.sleep(1)
                        else:
                            self.sd_tester.client_sim.send_data([0x36] + [block_sequence_counter] + list(block_data))
                            step_log = "transfer_data ---- loop: {}   block_sequence_counter:{}".format(loop,
                                                                                                        block_sequence_counter)
                            response_result = self.sd_tester.check_and_print_response_result(step_log)
                            if response_result == True:
                                self.end_address += block_length
                            elif response_result == False:
                                logger.info("Receive NRC")
                                break
                            elif response_result == None:
                                logger.info("Time out!!!  Message is not  received ")
                                break
            else:
                with open(file_path, "rb") as f:
                    block_length = os.path.getsize(file_path)
                    block_data = f.read(block_length)
                    #self.send_data([0x36] + [0x01] + list(block_data))
                    self.sd_tester.client_sim.send_data([0x36] + [0x01] + list(block_data))
                logger.error("file_size is {}".format(self.file_size))

    def request_transfer_exit(self,doipid,reverse_test_type = ""):
        self.sd_tester.update_serverdoipid(doipid)
        logger.info("刷写step10:请求退出数据传输")
        with allure.step(f"刷写step10:请求退出数据传输"):
            if reverse_test_type == "skip_transfer_data":
                logger.info("跳过transfer_data")
                self.result = self.send_request_and_recv_response([0x37],recv=[0x7F,0x37,0x72])
                return
            elif reverse_test_type == "跳过一段数据传输":
                logger.info("跳过一段数据传输")
                self.result = self.send_request_and_recv_response([0x37],recv=[0x7F,0x37,0x72])
                return
            else:
                self.result = self.send_request_and_recv_response([0x37],recv=[0x77])

    def transfer_keyinfo(self,doipid,key_info,reverse_test_type = ""):
        self.sd_tester.update_serverdoipid(doipid)
        logger.info("刷写step11:传输keyinfo")
        with allure.step(f"刷写step11:传输keyinfo"): 
            key_info = key_info.encode("utf-8")
            key_info = list(key_info)
            if reverse_test_type == "skip_request_transfer_exit":
                logger.info("跳过request_transfer_exit")
                self.result = self.send_request_and_recv_response([0x31,0x01] + [0x02, 0x08] + key_info, recv=[0x7F,0x31,0x10])
                return
            elif reverse_test_type == "keyinfo的长度错误":
                logger.info("keyinfo的长度错误")
                keyinfo_lengtherror = key_info[:-10]#切片
                if doipid == 0x1001:
                    self.result = self.send_request_and_recv_response([0x31,0x01] + [0x02, 0x08] + keyinfo_lengtherror, recv=[0x7F, 0x31, 0x13])
                    return
                elif doipid == 0x1011:
                    self.result = self.send_request_and_recv_response([0x31,0x01] + [0x02, 0x08] + keyinfo_lengtherror, recv=[0x71, 0x01, 0x02, 0x08, 0x10, 0x00])
                    return
            elif reverse_test_type == "keyinfo的内容错误":
                logger.info("keyinfo的内容错误")
                keyinfo_contenterror = key_info[::-1]#将列表元素倒序排列
                self.result = self.send_request_and_recv_response([0x31,0x01] + [0x02, 0x08] + keyinfo_contenterror, recv=[0x71, 0x01, 0x02, 0x08, 0x10, 0x00])
                return
            else:
                self.result = self.send_request_and_recv_response([0x31,0x01] + [0x02, 0x08] + key_info, recv=[0x71, 0x01, 0x02, 0x08, 0x10, 0x00])


    def verify_software_integrity(self,doipid,reverse_test_type = "",verify_time=0):
        self.sd_tester.update_serverdoipid(doipid)
        logger.info("刷写step12:软件一致性校验")
        with allure.step(f"刷写step12:软件一致性校验"): 
            if reverse_test_type == "keyinfo的内容错误":
                logger.info("keyinfo的内容错误")
                if doipid == 0x1001:
                    self.result = self.send_request_and_recv_response([0x31,0x01] + [0x02, 0x05], recv=[0x71, 0x01, 0x02, 0x05, 0x10, 0x00, 0x00, 0x00, 0x22])
                    return
                elif doipid == 0x1011:
                    self.result = self.send_request_and_recv_response([0x31,0x01] + [0x02, 0x05], recv=[0x71, 0x01, 0x02, 0x05, 0x10, 0x00, 0x00, 0x00, 0x01])
                    return
            elif reverse_test_type == "错误的包":
                logger.info("错误的包")
                if doipid == 0x1001:
                    self.result = self.send_request_and_recv_response([0x31,0x01] + [0x02, 0x05], recv=[0x71, 0x01, 0x02, 0x05, 0x10, 0x00, 0x00, 0x00, 0x22])
                    return
                elif doipid == 0x1011:
                    self.result = self.send_request_and_recv_response([0x31,0x01] + [0x02, 0x05], recv=[0x71, 0x01, 0x02, 0x05, 0x10, 0x00, 0x00, 0x00, 0x01])
                    return
            elif reverse_test_type == "安装过程中异常掉电":
                logger.info("安装过程中异常掉电")
                self.result = self.send_request_and_recv_response([0x31,0x01] + [0x02, 0x05], recv=False, do_assert=False)
                time.sleep(verify_time)
            else:
                self.result = self.send_request_and_recv_response([0x31,0x01] + [0x02, 0x05], recv=[0x71, 0x01, 0x02, 0x05, 0x10, 0x00, 0x00, 0x00, 0x00])
            
    def reset(self):
        self.sd_tester.update_serverdoipid(0x1FFF)
        logger.info("刷写step13:刷写完成后复位")
        with allure.step(f"刷写step13:刷写完成后复位"): 
              self.send_data([0x11,0x81])

    def read_version_or_check(self,doipip,check_data=None):
        """
        读取 ecu 软件号，并根据参数判断是否需要校验，
        @param check_data: 默认为 None 不校验，则返回（True，版本号），否则返回（校验结果，版本号）
        """
        # 读取版本号
        self.sd_tester.information_check_f1ae()
        # sleep(0.5)
        recv_data_list = self.return_udsdata_and_check_and_print_response_result()
        data_list = recv_data_list[3:]
        # 转化为16进制字符串
        data_hex = bytes(data_list).hex()
        # 判断是bgm 还是tcam
        if doipip == 0x1001:
            # bgm   02 6160110110 41 41 43  296011005520 4158
            fr = chr(int(data_hex[0:2], 16))
            mid = data_hex[2:12]
            ver_str = data_hex[12:18]
            ver = ''.join([chr(int(ver_str[i:i + 2], 16)) for i in range(0, len(ver_str), 2)])
            mcu_ver = (mid + ver).upper()
            # boot 的 版本号
            boot_str = data_hex[18:]
            boot_head = boot_str[:10]
            boot_foot = boot_str[10:]
            bot = ''.join([chr(int(boot_foot[i:i + 2], 16)) for i in range(0, len(boot_foot), 2)])
            boot_ver = (boot_head + bot).upper()
            logger.info(f'获取的 bgm 版本为: {mcu_ver} 和 boot 版本为: {boot_ver}')
        # elif self.client_sim.server_doip_id == 0x1011:
        elif doipip == 0x1011:
            # tcam
            # 第一个字节  1ASCII+5BCD+3ASCII
            fr = chr(int(data_hex[0:2], 16))
            mid = data_hex[2:12]
            ver_str = data_hex[12:]
            ver = ''.join([chr(int(ver_str[i:i + 2], 16)) for i in range(0, len(ver_str), 2)])
            mcu_ver = (mid + ver).upper()
            boot_ver = 'None'
            logger.info(f'获取的tcam版本为{mcu_ver} ')
        else:
            logger.info("获取非app版本号")
        # 如果不校验，则直接返回 true 和 版软件号
        if check_data is None:
            return True, mcu_ver
        elif isinstance(check_data, str):
            temp = check_data.upper().replace(' ', '')
            mcu_ver = mcu_ver.replace(' ', '')
            boot_ver = boot_ver.replace(' ', '')
            if temp.startswith("6"):
                ret_value = mcu_ver == temp
            else:
                ret_value = boot_ver == temp

        elif isinstance(check_data, (list, tuple)):
            temp = list(check_data)
            ret_value = mcu_ver == temp
        else:
            logger.error("check_data 参数的格式不对")
            ret_value = False

        return ret_value, mcu_ver

    def check_version(self,doipid,check_data=None):
        '''
        获取升级完后的版本，根据 check_data 来判断是否校验
        '''
        self.update_serverdoipid(doipid)
        if doipid == 0x1001:
            logger.info(f"BGM重启中等待20s")
            sleep(20)
        else:
            logger.info(f"TCAM重启中等待{180-self.tcam_redundancy_time}s")
            sleep(180-self.tcam_redundancy_time)

        try:
            ret, version = self.read_version_or_check(doipid,check_data=check_data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
            logger.error(f"读取版本号失败:{str(e)}")
            ret, version = 0, ''
        self.update_serverdoipid(doipid)
        sleep(1)
        return ret, version
    
    def flashimage_download(self,file_url,offline=False):
        logger.info("开始下载升级文件")
        with allure.step("下载升级文件"):
            # bin keyinfo 文件下载
            if file_url.startswith('https:'): #url是以https开头的，则下载文件
                file_path = self.sd_tester.download_and_check_bin_file(file_url, offline)
                if file_path is None:
                    try:
                        logger.info("==================== bin 文件下载完成 ==========================")
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
                        logger.info("==================== bin 文件下载异常 ==========================")
                        logger.error(e)
                    assert 0, "bin 文件下载异常"
            else:
                url_bin, url_keyinfo = self.sd_tester.get_path_url(ver=keyinfo, name=file_url)#根据写的APP名字获取对应的bin 和keyinfo 路径
                url_keyinfo_path = self.sd_tester.download_and_check_bin_file(url_keyinfo, offline)
                if url_keyinfo_path is None:
                    try:
                        logger.info("==================== keyinfo 文件下载完成 ==========================")
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
                        logger.info("==================== keyinfo 文件下载异常 ==========================")
                        logger.error(e)
                    assert 0, "keyinfo 文件下载异常"
                else:
                    with open(url_keyinfo_path, "r") as f:
                        lines = f.readlines()
                        lines_list = [i.strip().replace("\n", '') for i in lines if i.strip()]
                        keyinfo = lines_list[-1].split(":")[-1]
                        logger.info(f"获取的keyinfo=》{keyinfo}")
                if check_data == file_url:
                    check_data = self.sd_tester.get_version_by_url(url_bin)
                file_path = self.sd_tester.download_and_check_bin_file(url_bin, offline)
                if file_path is None:
                    try:
                        logger.info("==================== bin 文件下载完成 ==========================")
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
                        logger.info("==================== bin 文件下载异常 ==========================")
                        logger.error(e)
                    assert 0, "bin 文件下载异常"

            return file_path

    def flash_single_standard_ecu(
            self,
            ecu,
            doipip, 
            file_path,
            key_info,
            target_step=14,
            init_step=0,
            skip_step=[0],
            check_data=None,
            compression_encryption_method=0x00,
            offline_flashing=False,           
    ):
        '''
        标准的升级流程，默认会执行 0 到 14 步
        @param keyinfo:  如 "HacdLlcI1suuaQgb5NYeXSVob7bCxVO8mEN6poxblq76bim0VunQUHvpvkdJzGysy4jUso7AR7L07jEd3cadbyiWPeyoVqdSTVuln3xZyUZxcFvd0ewc2/u1GZKrRwWPF4deM0l+b18lL2zcbmdnO2KX+OqIf4loBaOhQ8OGiOV+DoIYsjXUC/zghbO+Fpz9rkxMH1T7+m33mZo0EwY7uYnmc5CPmIQg2wC/fmnFS91mdqn7pjcwsTKqjKR2eDkTApanNZmwD6HlYlYQDfQEIzBS8sZ/e2e27WRHXLNCynF3lgVzdWmvZZx9yHLLfMx+bBsU4MUTyfcIfselexCLZg=="
        @param file_url: 升级的bin 文件路径 如 "https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/6110110055BD.bin"
        @param target_step: 结束步骤 （最大为 14）
        @param init_step: 开始步骤  （最小为 0）
        @param skip_step: 要跳过的步骤， 为列表格式
        @param check_data: 版本 字符串类型  如 6160110110AAC 或者6110110055 BD
        @return:
        '''
        self.flash_result = True
        step = init_step
        sub_step = 1
        self.transfer_data_total_int_time = 0
        self.pregramming_dependencies_total_int_time = 0
        self.flash_total_int_time = 0
        self.flash_start = time.time()
         # Start Flash... Active ECU
        logger.info("====== Start Flash... Active ECU ======")
        while self.flash_result and (step != target_step):
            step += 1
            if step in skip_step:
                logger.info("Skip the step {}".format(step))
            else:
                if step == 1:
                    # Step 1  Check Program Pre-condition
                    self.check_program_precondition()
                    sleep(1.5)
                elif step == 2:
                    # Step 2  Enter Program Mode
                    self.enter_program_mode()
                elif step == 3:
                    # Step 3  Confirm Program Mode
                    if offline_flashing:
                        sleep(5)# 离线刷写新需求： 1082之后由立即发送1002变更为等待5s之后再发送1002
                    self.confirm_program_mode(doipip)
                elif step == 4:
                    # Step 4  Diagnostic Session Check
                    if offline_flashing:# 离线刷写台新需求：进入boot后，22F186返回1后由工具立刻返回错误，变更为工具等待1s重试发1002进boot
                        self.send_data([[0x22, 0xF1, 0x86]])
                        result_data = self.return_udsdata_and_check_and_print_response_result()
                        if result_data == [0x62, 0xF1, 0x86, 0x01]:
                            sleep(1)
                            self.confirm_program_mode(doipip)
                        elif result_data == [0x62, 0xF1, 0x86, 0x02]:
                            self.flash_result=True
                        else:
                            self.flash_result=False

                    self.diagnostic_session_check(doipip)
                elif step == 5:
                    # Step 5  Information Check
                    self.infotainment_check(doipip)
                    time.sleep(2)
                elif step == 6:
                    # Step 6  Unlock For Download
                    
                    self.unlocK_for_download(doipip,ecu)
                elif step == 7:
                    # Step 7  Erase Memory
                    self.erase_memory(doipip,file_path)
                elif step == 8:
                    # Step 8  Request Download
                    self.request_download(doipip,file_path,compression_encryption_method=[compression_encryption_method])
                    # self.sd_tester.request_download(file_path,compression_encryption_method=[compression_encryption_method])
                    # self.flash_result = self.sd_tester.check_and_print_response_result(
                    #     "Step 8  Request Download"
                    # )
                elif step == 9:
                    # Step 9  Transfer Data
                    self.transfer_data_start = time.time()
                    self.transfer_data(doipip,file_path)
                    #self.sd_tester.transfer_data(file_path)
                    #传包时间统计
                    self.transfer_data_end = time.time()
                    self.transfer_data_total_time = (self.transfer_data_end - self.transfer_data_start)
                    self.transfer_data_total_int_time = int(self.transfer_data_total_time)
                    self.transfer_data_total_time_minute = (self.transfer_data_total_int_time // 60)
                    self.transfer_data_total_time_second = (self.transfer_data_total_int_time % 60)
                    logger.info("self.transfer_data_total_time is {} minutes  {} seconds".format(
                            self.transfer_data_total_time_minute,
                            self.transfer_data_total_time_second,))
                elif step == 10:
                    # Step 10  Request Transfer Exit
                    self.request_transfer_exit(doipip)
                elif step == 11:
                    # Step 11  Transfer Key Info
                    self.transfer_keyinfo(doipip,key_info)
                elif step == 12:
                    # Step 12  Verify Software Integrity
                    self.pregramming_dependencies_start = time.time()
                    self.verify_software_integrity(doipip)
                    #预编程依赖时间统计
                    self.pregramming_dependencies_end = time.time()
                    self.pregramming_dependencies_total_time = (
                            self.pregramming_dependencies_end
                            - self.pregramming_dependencies_start
                    )
                    self.pregramming_dependencies_total_int_time = int(
                        self.pregramming_dependencies_total_time
                    )
                    self.pregramming_dependencies_total_time_minute = (
                            self.pregramming_dependencies_total_int_time // 60
                    )
                    self.pregramming_dependencies_total_time_second = (
                            self.pregramming_dependencies_total_int_time % 60
                    )
                    logger.info(
                        "self.pregramming_dependencies_total_time is {} minutes  {} seconds".format(
                            self.pregramming_dependencies_total_time_minute,
                            self.pregramming_dependencies_total_time_second,
                        )
                    )
                elif step == 13:
                    #重启之前停止抓包
                    BGM_SSH().stop_bgm_tcpdump()
                    logger.info('stop sniff packet eth0')

                    # Step 13  Reset
                    self.reset()
                    vehicle_announcement_before = time.time()
                    with allure.step("获取1181退出boot后第一条车辆公告发出时间"):
                        vehicle_announcement_after = self.wait_vehicle_announcement()
                    with allure.step("判断间隔时间是否在20s内"):
                        global interval_1181
                        interval_1181 = vehicle_announcement_after - vehicle_announcement_before
                        logger.info(f"间隔时间为{interval_1181}s")
                        with allure.step("判断功能寻址下获取1181退出boot后第一条车辆公告发出时间间隔时间是否在20s内"):
                            assert interval_1181 < 20 , '功能寻址下获取1181退出boot后第一条车辆公告发出时间大于20s'
                    rs_start_time = time.time()
                    # if self.sd_tester.server_doip_id == 0x1011:
                    #     self.flash_result = self.sd_tester.check_and_print_response_result(
                    #         "Step 13  ECU Reset")
                    rs_end_time = time.time()
                    self.tcam_redundancy_time = rs_end_time - rs_start_time
                    # if self.flash_result is False:
                    #     raise AssertionError(f"诊断回复负响应。")
                    
                    #刷写总时间统计
                    self.flash_end = time.time()-interval_1181
                    self.flash_total_time = self.flash_end - self.flash_start
                    self.flash_total_int_time = int(self.flash_total_time)
                    self.flash_total_time_minute = self.flash_total_int_time // 60
                    self.flash_total_time_second = self.flash_total_int_time % 60
                    logger.info(
                        "flash_total_time is {} minutes  {} seconds".format(
                            self.flash_total_time_minute, self.flash_total_time_second
                        )
                    )
                    
                elif step == 14:
                    # Step 14  校验 升级后的版本
                    logger.info(f"check_data = {check_data}")
                    self.flash_result, version = self.check_version(doipip,check_data)
                    if check_data is None:
                        logger.info(f" =================Doip Flash Done  Current Version  {version} =================")
                    sleep(1)
                    logger.info(" ===========================   Doip Flash Complete   ===========================")


        self.flash_time_statistics = [
            self.transfer_data_total_int_time,
            self.pregramming_dependencies_total_int_time,
            self.flash_total_int_time,
        ]

        return self.flash_result    

    def upgrade_ecu(self,ecu,doipip,keyinfo,file_url,standard=True, check_data=None, skip_step=[0], offline=False, save_packet=True,sniff_packet=False,save_path='.'):
        '''
        软件升级，默认是一个完整的升级流程
        :param keyinfo: 如 "HacdLlcI1suuaQgb5NYeXSVob7bCxVO8mEN6poxblq76bim0VunQUHvpvkdJzGysy4jUso7AR7L07jEd3cadbyiWPeyoVqdSTVuln3xZyUZxcFvd0ewc2/u1GZKrRwWPF4deM0l+b18lL2zcbmdnO2KX+OqIf4loBaOhQ8OGiOV+DoIYsjXUC/zghbO+Fpz9rkxMH1T7+m33mZo0EwY7uYnmc5CPmIQg2wC/fmnFS91mdqn7pjcwsTKqjKR2eDkTApanNZmwD6HlYlYQDfQEIzBS8sZ/e2e27WRHXLNCynF3lgVzdWmvZZx9yHLLfMx+bBsU4MUTyfcIfselexCLZg=="
        :param file_url: 升级的bin 文件路径 如 "https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/6110110055BD.bin"
        :param standard: 是否为标准升级流程（默认是 标准流程),为false 表示按special 方式升级
        :param check_data: 版本 字符串类型  如 6160110110AAC 或者6110110055 BD
        :param skip_step: 要跳过的步骤， 为列表格式
        :param offline: 是否离线刷写，默认在线刷写，离线刷写 需要吧 对应的bin 文件放在执行目录下,tcam 则放在sat/xat_cases/legacy/tcam ;bgm则放在sat/xat_cases/legacy/bgm
        :param save_packet: 是否要保存OBD抓包数据
        :param sniff_packet: 是否要保存tcpdump抓包数据
        :param save_path: 保存tcpdump抓包数据的路径
        '''
        self.sd_tester.update_serverdoipid(doipip,ecu)
        #抓包工具推送及初始化
        self.sniff_packet = sniff_packet
        if self.sniff_packet:
            BGM_SSH().init_bgm_tcpdump(connect_type="obd")#推送tcpdump抓包工具，并初始化抓包工具
        if save_packet:
            self.sff = SniffPacket(iface='169.254.1.200')
            # 设置抓包保存名字，可以不设置，有默认值，保存的文件都会带有时间
            self.sff.set_save_name('诊断升级')
            # 开启抓包
            self.sff.start_sniff()
        
        try:
            #获取刷写软件版本号
            # 如果check_data不传参数，则根据 url 路径获取 版本号
            if check_data is None:
                check_data = self.sd_tester.get_version_by_url(file_url)#获取刷写软件的版本号

            name = "standard flash" if standard else "special flash"
            logger.info(f"当前的升级流程为 {name}")

            self.flash_time_total = {}

            # bin keyinfo 文件下载
            if file_url.startswith('https:'): #url是以https开头的，则下载文件
                # 下载文件，要放在开启3e80 后面，防止下载时间久，会超时拆链接
                file_path = self.sd_tester.download_and_check_bin_file(file_url, offline)
                if file_path is None:
                    try:
                        logger.info("==================== bin 文件下载完成 ==========================")
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
                        logger.info("==================== bin 文件下载异常 ==========================")
                        logger.error(e)
                    assert 0, "bin 文件下载异常"
            else:
                url_bin, url_keyinfo = self.sd_tester.get_path_url(ver=keyinfo, name=file_url)#根据写的APP名字获取对应的bin 和keyinfo 路径
                # 下载文件，要放在开启3e80 后面，防止下载时间久，会超时拆链接 下载 keyinfo 文件
                url_keyinfo_path = self.sd_tester.download_and_check_bin_file(url_keyinfo, offline)
                if url_keyinfo_path is None:
                    try:
                        logger.info("==================== keyinfo 文件下载完成 ==========================")
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
                        logger.info("==================== keyinfo 文件下载异常 ==========================")
                        logger.error(e)
                    assert 0, "keyinfo 文件下载异常"
                else:
                    with open(url_keyinfo_path, "r") as f:
                        lines = f.readlines()
                        lines_list = [i.strip().replace("\n", '') for i in lines if i.strip()]
                        keyinfo = lines_list[-1].split(":")[-1]
                        logger.info(f"获取的keyinfo=》{keyinfo}")
                if check_data == file_url:
                    check_data = self.sd_tester.get_version_by_url(url_bin)
                file_path = self.sd_tester.download_and_check_bin_file(url_bin, offline)
                if file_path is None:
                    try:
                        logger.info("==================== bin 文件下载完成 ==========================")
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
                        logger.info("==================== bin 文件下载异常 ==========================")
                        logger.error(e)
                    assert 0, "bin 文件下载异常"

            #获取刷写软件版本号
            self.send_data([0x22, 0xF1, 0x86])# 读取会话状态 [0x22, 0xF1, 0x86]
            result = self.return_udsdata_and_check_and_print_response_result()
            # [0x62, 0xF1, 0x86,0x01/0x02]
            diagnostic_session = result[-1]
            sleep(0.5)
            # 判断在boot中还是app中
            if diagnostic_session == 1:
                # app 升级
                self.read_version_or_check(doipip)#[0x22, 0xF1, 0xAE] 读取BGM/TCAM APP版本号
            else:
                self.sd_tester.update_serverdoipid(0x1002)#BGM boot版本号
                sleep(2)
                self.sd_tester.read_boot_version_or_check()

            self.sd_tester.update_serverdoipid(doipip)
            sleep(1)

            #执行刷写流程第1-2步骤
            try:
                if standard:
                    result = self.flash_single_standard_ecu(
                        ecu,
                        doipip,
                        file_path,
                        keyinfo,
                        target_step=2,
                        init_step=0,
                        check_data=check_data,
                        skip_step=skip_step, 
                    )
                else:
                    result = self.flash_single_standard_ecu(
                        ecu,
                        doipip,
                        file_path,
                        keyinfo,
                        target_step=2,
                        init_step=0,
                        check_data=check_data,
                        skip_step=skip_step,
                    )
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
                logger.info("==================== flash_single_standard_ecu Error ==========================")
                logger.error(e)
                result = 0

            sleep(10)

            # 执行刷写流程第3-14步骤
            if result:
                #开启tcpdump抓包
                if self.sniff_packet:
                    tcpdump_file_path,tcpdump_save_name = BGM_SSH().start_bgm_tcpdump(iface='eth0',name='eth0_',path='/data',connect_type="obd")
                    logger.info('starting to sniff eth0 packet')
                #执行刷写流程第3-14步骤
                try:
                    if standard:
                        result = self.flash_single_standard_ecu(
                            ecu,
                            doipip,
                            file_path,
                            keyinfo,
                            target_step=14,
                            init_step=2,
                            check_data=check_data,
                            skip_step=skip_step,
                        )
                    else:
                        result = self.flash_single_standard_ecu(
                            ecu,
                            doipip,
                            file_path,
                            keyinfo,
                            target_step=14,
                            init_step=2,
                            check_data=check_data,
                            skip_step=skip_step,
                        )
                except Exception as e:
                    #刷写失败停止抓包
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
                    if self.sniff_packet:
                        BGM_SSH().stop_bgm_tcpdump()
                        logger.info('stop sniff packet eth0')
                        
                    logger.error(e)
                    result = 0
            #刷写流程步骤1-2，3-14步骤如果存在失败，保存BGM日志
            if not result:
                sleep(20) 
                logger.info("==========  Flash Failed , Restart  =======")
                try:
                    if doipip == 0x1001:
                        self.sd_tester.reset_ecu_functional_addressing()
                        sleep(20)
                        logger.info('BGM刷写失败 重启BGM并等待20s')
                    else:
                        logger.info('TCAM刷写失败 重启TCAM并等待180s')
                        self.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
                        self.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])
                        self.send_request_and_recv_response([0x11, 0x03], recv=[0x51, 0x03])
                        sleep(180)
                    result = 0
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
                    logger.error(str(e))
                    logger.warning("====  Flash Failed , Restart  Failed =========")
                    result = 0

            #记录对应刷写次数的flash时间
            global flash_count
            flash_count += 1
            flash_count_name = "flash_count_{}".format(flash_count)
            self.flash_time_total[flash_count_name] = self.flash_time_statistics
            logger.info(
                "{} Flash Time statistics[transfer_data_total_int_time,pregramming_dependencies_total_int_time,"
                "flash_total_int_time] is {}".format(
                    flash_count_name, self.flash_time_statistics
                )
            )

        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/sdtest.py")
            logger.error(f'升级失败{str(e)}')
            sleep(10)
            result = 0

        #  停止抓抓包
        if save_packet:
            self.sff.stop_sniff()

        if self.sniff_packet:
            #把tcpdump抓包数据下下载到本地 下载完成后删除
            BGM_SSH().scp_bgm_file_to_local(bgm_file_pah=tcpdump_file_path,local_path=save_path,del_flag=True, connect_type="obd")
            logger.info(f'download sniff packet /{tcpdump_save_name} to {save_path} ...')

        assert result, " Flash >>>>>>>>>>>>>>>>  Failed"

    def generate_tire_P_and_T(self,pressure: float, temperature: int):
        tire_P = math.ceil(pressure / 1.373)
        tire_T = temperature + 50
        check_tire_p = tire_P * 1.373
        check_tire_t = tire_T - 50
        return tire_P, tire_T, check_tire_p, check_tire_t
