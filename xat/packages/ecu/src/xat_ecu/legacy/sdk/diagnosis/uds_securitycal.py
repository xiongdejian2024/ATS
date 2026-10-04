# -*- coding: utf-8 -*-

from xat_ecu.legacy.sdk.ecu_sim_const import ECUSimConst
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.diagnosis.aes_128_cbc import Aes128


class SecurityAlgorithm:
    """
    Security Algorithm
    """
    def __init__(self, ecu, sec_con :dict={}):
        self.seed = None
        self.constant = None
        self.result = None
        self.temp = None
        self.temp_1 = None
        self.temp_2 = None
        self.temp_3 = None
        self.security_constant_dict = ECUSimConst.ECU_SECURITY
        if sec_con:
            self.security_constant_dict.update(sec_con)
        security_constants = self.security_constant_dict.get(ecu)
        #logger.info("security_constants of {} is {}".format(ecu, security_constants))

        if isinstance(security_constants, list):
            if len(security_constants) < 8:
                for i in range(8 - len(security_constants)):
                    security_constants.append(None)
                    
            self.constant_lev1 = security_constants[0]
            self.constant_lev2 = security_constants[1]
            self.constant_lev3 = security_constants[2]
            self.constant_lev4 = security_constants[3]
            self.constant_lev5 = security_constants[4]
            self.constant_lev6 = security_constants[5]
            self.constant_lev7 = security_constants[6]
            self.constant_lev8 = security_constants[7]
            
            if self.constant_lev1 == None:
                self.constant_lev1 = 0xFFFFFFFFFF
            elif self.constant_lev2 == None:
                self.constant_lev2 = 0xFFFFFFFFFF
            elif self.constant_lev3 == None:
                self.constant_lev3 = 0xFFFFFFFFFF
            elif self.constant_lev4 == None:
                self.constant_lev4 = "00112233445566778899aabbccddeeff"
            elif self.constant_lev5 == None:
                self.constant_lev5 = 0xFFFFFFFFFF
            elif self.constant_lev6 == None:
                self.constant_lev6 = 0xFFFFFFFFFF
            elif self.constant_lev7 == None:
                self.constant_lev7 = 0xFFFFFFFFFF
            elif self.constant_lev8 == None:
                self.constant_lev8 = 0xFFFFFFFFFF
        else:
            logger.error("security_constants of {} is error".format(ecu))

        if self.constant_lev4 == None :
            self.constant_lev4 = "8a46c5b548c0a3318bacc17bc3a8edea"
        
        self.cryptor_aes128 = Aes128(key=self.constant_lev4, iv="00000000000000000000000000000000")

    def update_security_constant(self, ecu):
        security_constants = self.security_constant_dict.get(ecu)
        if len(security_constants) < 8 :
                for i in range(8 - len(security_constants) ):
                    security_constants.append(None)
        self.constant_lev1 = security_constants[0]
        self.constant_lev2 = security_constants[1]
        self.constant_lev3 = security_constants[2]
        self.constant_lev4 = security_constants[3]
        self.constant_lev5 = security_constants[4]
        self.constant_lev6 = security_constants[5]
        self.constant_lev7 = security_constants[6]
        self.constant_lev8 = security_constants[7]
        
        if self.constant_lev1 == None:
            self.constant_lev1 = 0xFFFFFFFFFF
        elif self.constant_lev2 == None:
            self.constant_lev2 = 0xFFFFFFFFFF
        elif self.constant_lev3 == None:
            self.constant_lev3 = 0xFFFFFFFFFF
        elif self.constant_lev4 == None:
            self.constant_lev4 = "00112233445566778899aabbccddeeff"
        elif self.constant_lev5 == None:
            self.constant_lev5 = 0xFFFFFFFFFF
        elif self.constant_lev6 == None:
            self.constant_lev6 = 0xFFFFFFFFFF
        elif self.constant_lev7 == None:
            self.constant_lev7 = 0xFFFFFFFFFF
        elif self.constant_lev8 == None:
            self.constant_lev8 = 0xFFFFFFFFFF
                                 
        self.cryptor_aes128.key = self.constant_lev4

    def get_calculated_key(self, level, value):  # calculate key from seed
        """
        从seed计算得到key
        @param level: 解锁等级
        @param value: seed值
        @return:
        """
        if isinstance(value, list):
            value = bytes(value)
        if level in [1,2,3,5,6,7,8]:
            seed = int.from_bytes(value, byteorder='little',signed=False)
            if level == 1:
                result = self.cal_seed(seed=seed, constant=self.constant_lev1)
            elif level == 2:
                result = self.cal_seed(seed=seed, constant=self.constant_lev2)
            elif level == 3:
                result = self.cal_seed(seed=seed, constant=self.constant_lev3)
            elif level == 5:
                result = self.cal_seed(seed=seed, constant=self.constant_lev5)
            elif level == 6:
                result = self.cal_seed(seed=seed, constant=self.constant_lev6)
            elif level == 7:
                result = self.cal_seed(seed=seed, constant=self.constant_lev7)
            elif level == 8:
                result = self.cal_seed(seed=seed, constant=self.constant_lev8)
            result = result.to_bytes(3, 'little')
            return result
        elif level == 4:
            self.cryptor_aes128.update_key_hexstr(self.constant_lev4)
            result = self.cryptor_aes128.encrypt(value)
            return result

    def cal_seed(self, seed, constant):
        seed &= 0x00FFFFFF
        result = 0x00C541A9
        constant = int.from_bytes(constant.to_bytes(5, 'little'), byteorder='big')
        constant <<= 24
        constant |= seed

        for i in range(0, 64):
            temp = constant & 0x00000001
            temp = result ^ temp
            result >>= 1
            temp <<= 23
            temp &= 0x00800000
            result |= temp  # B24
            temp >>= 3
            result = ((temp ^ result) & 0x00100000) | (result & (~0x00100000))  # B21
            temp >>= 5
            result = ((temp ^ result) & 0x00008000) | (result & (~0x00008000))  # B16
            temp >>= 3
            result = ((temp ^ result) & 0x00001000) | (result & (~0x00001000))  # B13
            temp >>= 7
            result = ((temp ^ result) & 0x00000020) | (result & (~0x00000020))  # B6
            temp >>= 2
            result = ((temp ^ result) & 0x00000008) | (result & (~0x00000008))  # B4
            constant >>= 1

        temp_1 = result | 0x00
        temp_2 = (result >> 8) | 0x00
        temp_3 = (result >> 16) | 0x00
        result >>= 4  # Response Byte1
        result &= 0xFF0000FF
        temp_2 = (temp_3 >> 4) | (temp_2 & 0xF0)
        result |= ((0x0000 | temp_2) << 8)  # Response Byte2
        result |= (((0x000000 | ((temp_1 << 4) | (temp_3 & 0x0F)))) << 16)  # Response Byte3
        result &= 0x00FFFFFF  # Discard Byte4
        return result