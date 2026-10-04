# -*- coding: utf-8 -*-
"""
@File        : rsa_encrypt.py
@Author      : jiabin.zhu@jiduatuo.com
@Time        : 2023-02-01 14:44
@Description :
"""

import sys
import os

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import base64

bgm_tsp_rsa_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtJ1O/b2u1hHDuxNwkPoDKr8jYNuYIjsrxlGCNfa7tuFprDiY7/J4CZj2XHQZLppZZNk5kf6Af1Wkan/prO4wEpXivtsLAzPXuX/Y2bnKiCvMPnNXSCcXeWVzO1Rt0osMX3nlIujEwX5/3wrS5CbkJOvfX+lxgaqU7ZMnRbbXyNQiAX4QV7Me9U//+xxILtGXvdetojdS3Bfgn9YUZZvVe7gx2MX9FAoorLsia70k92egzS9i6sl3YWqzz0Izubg29WiQIyfb/lf92h7Y2ggfD5ZRhp1BLPfV9Ye5A1Ra1iGJ7Rdn5fs0oN2IHb9YtmNX+yThhvVXnzxInMuqLDyFsQIDAQAB'


class RsaEncrypt:
    def __init__(self, public_key=bgm_tsp_rsa_public_key, private_key=''):
        self.public_key = self.get_key(public_key)
        self.private_key = self.get_key(private_key)

    @staticmethod
    def get_key(key_str):
        return RSA.importKey(key_str)

    def encrypt_data(self, data: str):
        cipher = PKCS1_cipher.new(self.public_key)  # 生成一个加密的类
        encrypt_text = base64.b64encode(cipher.encrypt(data.encode()))  # 对数据进行加密
        return encrypt_text.decode()  # 对文本进行解码码

    def decrypt_data(self, encrypt_data):
        cipher = PKCS1_cipher.new(self.private_key)  # 生成一个解密的类
        back_text = cipher.decrypt(base64.b64decode(encrypt_data), 0)  # 进行解密
        return back_text.decode()  # 对文本内容进行解码


if __name__ == '__main__':
    rsa = RsaEncrypt(private_key=bgm_tsp_rsa_public_key)
    print(rsa.decrypt_data('EES5iLltdGnthnbZbD2BANKCUMY2rrZlnhit3O599K+lyZj6XCUj1vaG5luK9P45qhWegHiy4C5TAKl1630frHPGyZR0hwNAhY0Zy0oMuXuJ0T5/LIL+C/I+7NM6n1n4yAedlPV2LFwchK16+zIlpTh/qzJ3BcAyKcAcXl4cN74esK/vDxczKQhknXXXW/srRfhJSLtPsuj1vQcyiWHjxfWE6SPmPcAtUUkL17hHH3Z543uhoksWdSu5jfqd9daJ8SwE4JgQmCs3TpHnBh8pR44tm0NeM2TpADstorwomW9e1OWmpPoO/q/ffYTwbLJr9xR1EzJ+GGzZ3SprY/+BFJmF4QMIsEH52MWn97QbKc1h0MDeMI0vQ6OmE0LLm5KUejuc1wms+Qwx88VxdiApjBFiKqyce+KaxIDn6KoQ5RFZsb9X3mS1v4DVHhvP7lVInbW4pukWkrlCuOBBmrnIy36/1Kjz/Oad5p6DQFTsWjou/LzR8UjNIAdXWmY/voyuaHhAGOFyNhvlgzZMoix7bjYyXORPaTjQcwOo6OIDtxvEPI3nq5suaemVx54P9cLFkRcamkGukFf9odjL0vO8EC+VJy3MKR1WqLjp8fXdpE7TE5ELPKn2rNtBtNTmJq7kIZvh24GkhZ6tGAQeioyjCVKLVKL2HsQoiPsGzNLsuKQ='))
