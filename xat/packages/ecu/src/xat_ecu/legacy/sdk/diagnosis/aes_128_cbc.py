# -*- coding: utf-8 -*-
"""
@File        : aes_128_cbc.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-06-28 18:57
@Description : 
"""

import sys
import os
# from ..common.logger import *

from Crypto.Cipher import AES
from Crypto.Hash import CMAC
from Crypto.Util.Padding import pad
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from typing import Union
import base64


class AesCmac128(object):
    """"AES-128(CMAC mode)"""

    def __init__(self, key):
        self.key = key
        self.cipher = CMAC.new(key, ciphermod=AES)

    def encrypt(self, text: str):
        """
        通过key对明文计算CMAC
        :param text: 待计算CMAC的字符串
        :return: 返回16字节CMAC
        """
        self.cipher = CMAC.new(self.key, ciphermod=AES)
        return self.cipher.update(bytes.fromhex(text)).hexdigest().upper()  # hexdigest表示加密字符串转化成16进制


class Aes128:
    """"AES-128，适配多种mode，默认CBC"""

    def __init__(self, key, iv=None, mode=AES.MODE_CBC):
        self.key = DataTypeHanding.to_bytes(key)
        self.iv = DataTypeHanding.to_bytes(iv)
        self.mode = mode

    def update_key_utf8(self, key: str = "${XAT_CREDENTIAL_SCAN_B7043B1F2B2E544D49FF}"):
        # key = "${XAT_CREDENTIAL_SCAN_B7043B1F2B2E544D49FF}"
        self.key = bytes(key, "utf-8")

    def update_key_hexstr(self, key: str = "${XAT_CREDENTIAL_SCAN_4D834173E3BB240A94B8}"):
        # key = "${XAT_CREDENTIAL_SCAN_4D834173E3BB240A94B8}"
        self.key = bytes.fromhex(key)

    def update_iv_utf8(self, iv: str = "0000000000000000"):
        # iv = "0000000000000000"
        self.iv = bytes(iv, "utf-8")

    def encrypt_pad_with_pkcs7(self, plaintext: str) -> bytes:
        """
        加密报文(使用pksc7填充)
        :param plaintext: 十六进制字符串的明文
        :return: 十六进制字符串的密文
        """
        encryptor = AES.new(self.key, self.mode, self.iv)
        plain_bytes = pad(DataTypeHanding.to_bytes(plaintext), AES.block_size)
        return encryptor.encrypt(plain_bytes)

    def encrypt(self, plain: Union[bytes, str]) -> bytes:
        """
        加密报文
        :param plain: 明文, 可以是bytes也可以是str
        :return: 十六进制字符串的密文
        """
        encryptor = AES.new(self.key, self.mode, self.iv)
        plain_bytes = DataTypeHanding.to_bytes(plain)
        length = encryptor.block_size
        count = len(plain_bytes)
        if count // length >= 1 and count % length == 0:
            cipher_bytes = encryptor.encrypt(plain_bytes)
        else:
            raise ValueError("The length of the plaintext is wrong")
        return cipher_bytes

    def decrypt(self, cipher: Union[bytes, str]) -> bytes:
        """
        将密文解密为明文
        :param cipher: 密文, 字符串或bytes
        :return: 十六进制字符串的明文
        """
        encryptor = AES.new(self.key, self.mode, self.iv)
        cipher_bytes = DataTypeHanding.to_bytes(cipher)
        plain_bytes = encryptor.decrypt(cipher_bytes)
        return plain_bytes


def bcc_check(inlist: list) -> int:
    """
    BCC异或校验
    :param inlist: 输入参数，[0x11, 0x12, 0x13]
    :return: int
    """
    res = 0
    for x in inlist:
        res ^= x
    return res


if __name__=="__main__":
    # NT1 key , NT1 iv
    text = "01D74CFD2A3C5A3D5A248361B7878F421629C9097474107B54EE34FDE9F619EACEE4E9F921C337FA67BADB1FC26B" \
           "E0D8142B61081FF08473DFB871C9300A34FE"
    text_bytes = bytes.fromhex(text)
    # text_bytes = bytes(text, "utf-8")
    print(text_bytes)

    cryptor = Aes128(key=__import__("os").environ['XAT_CREDENTIAL_SCAN_83E56124FEB1621E9413'], iv="00000000000000000000000000000000")

    ciphertext = cryptor.encrypt(text_bytes)
    ciphertext_hexstr = ciphertext.hex()
    print(ciphertext_hexstr)

    ciphertext_verification = "1A96CE5E947D2BD4756B7943DD3D9F6CF3AF0AF3711E44F1F255774A21497F0608D9F26EE8A7C905A8C7BDA" \
                 "4B031E5590CE648EDC9FB8996D4F2D14CE0811A09"

    print(ciphertext_hexstr.upper() == ciphertext_verification)
    print(cryptor.decrypt(bytes.fromhex("09e9a1e11fa2098ce6a5d4d0a2faa5828e90aafb5986039a59d6479e8ad421aedb2846b9a3a289e716eff50d341673b9")))

    BNCM_KEY = bytes([0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F])
    BNCM_IV = bytes([0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F])
    print(bcc_check([0x01, 0xA0, 0x7C, 0xFF, 0x02]))
    print(bcc_check([0x01, 0x80, 0x09, 0xA3, 0x00, 0x05, 0x00, 0x00, 0x84, 0x00, 0x00, 0x04]))





