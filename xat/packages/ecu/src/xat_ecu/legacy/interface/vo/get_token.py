#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: get_token.py
@Time: 2024/5/29 14:03
@Author: lei.hong
@Software: vscode
@Description: 获取token
@Examples: 
"""
import rsa
import base64
import time
from hashlib import md5
import json
import requests
from xat_ecu.legacy.common.logger import logger
def get_passport_b_token(client_id: str, client_secret: str, user_name: str, password: str
    ):
        """获取平台token
        Args:
            client_id (str): Client ID
            client_secret (str): Client Secret
            user_name (str): 用户名
            password (str): 密码

        Returns:
            str: token
        """
        endpoint = "https://passport.jiduprod.com/api/passportb"
        r = get_token(
            user_name=user_name,
            password=password,
            client_id=client_id,
            env_name='staging',
            endpoint=endpoint,
            client_secret=client_secret,
        ).json()
        if not "token" in r["data"]:
            logger.info(r)
            return None
        return r["data"]["token"]

def get_token(env_name, user_name, password, client_id, endpoint, client_secret
    ):
        """获取 token 方法"""
        path = "/openapi/v1/login/password"
        json_data = {
            "username": user_name,
            "password": rsa_encrypt(text=password, env_name=env_name),
        }
        now = time.time()
        timestamp = str(int(round(now * 1000)))
        body_md5 = md5(json.dumps(json_data).encode("utf-8")).hexdigest()
        signdata = f"timestamp={timestamp}&url={path}&identity={client_id}&body={body_md5}&secret={client_secret}"
        signature = md5(signdata.encode("utf-8")).hexdigest()
        headers = {
            "Connection": "keep-alive",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            "sec-ch-ua-mobile": "?0",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Timestamp": timestamp,
            "x-jidu-clientid": client_id,
            "x-jidu-clientid-signature": signature,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
        }
        url = f"{endpoint}{path}"
        response = requests.post(
            url=url, headers=headers, json=json_data, timeout=5
        )
        http_debug(url=url, data=json_data, headers=headers, ret=response.text)
        return response

def rsa_encrypt(text, env_name):
    """RSA 加密"""
    test_publickey = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzhq8/sb7wB6xbt4DiDoR
    S+cJ+IIuJQJWsKd7nMlZKOpLxi/bggqdSoK3Joc9ai1NQNKgkfQEvM5X8ZiDRvn2
    YgO7CrpTS5rstLPkrzuoLA52NLy2kI6arnxL9OT/qM2qOsoDegfFacZnUEnVa80O
    M7KBXIaoXJfLF+0M5bm27rWAhms+uXcOOEnkvI/Zs2fEPEJ6uLLyC/G0vDNq5yyT
    dI2tQ3C7XUA5eUiZwdLiXuoV9DLdozWJPCJc6EewwlV2swZ09xNnnlikAez6lVFu
    Q5BhdtCbr0h6fTHlEebFKB0NpGxpTiU1DjAPQsykjGU9PaOiCFuFhqEOFFCpSZbV
    lwIDAQAB
    -----END PUBLIC KEY-----
    """
    dev_publickey = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAn5JDwpIdGMY0BY/eLqDw
U1W3JOoGR0t2cyW63b4PjTL+0dDfir784+TqQ4+IgdCq3iKwgpmGbYUNCTo+aOAg
KUoLBJYKCI09RJ9GyfqXWNMb5wwtlmMn0ad/FLR0yfkMb8ChwaWaRE+dlPacaJgK
DveM2ze/t5FJU35lrf7IFwjH1iA61aOmLVorzxxevoiKZmYaFP8u6pZdMDQIEzBc
Ymi9gYFzeNWCcbDZLoigOG0JCn1IJIf6PPkfLzadEYFRC7jHrnyGVPwPPkNoNqCR
ZzcZHKRwqismQYichIPsuE0R+31dnoduLG91Ekolo86B5XSqEffwQWRo8mbLq0nI
cwIDAQAB
-----END PUBLIC KEY-----
    """
    staging_publickey = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmlzjOSeLpzsPbceW0rlL
zrSx7dpUOdbhSAoBqQTOOkq2BYK2iujy3XjD3COgWxxcLA6QC3Gq6TypW7c/umjP
fOAmLaHKxrlX1jSuguZXkuN2tb7kIhZC/5QOQY4+CDbKpf8rZCRTCeADZ2/cHa60
PI3YwJHETDzhkI+C3dq1mxYe4HMTAXIbqwhhKuA2HquwAehAr5eQ2z3BiucdfxbM
bOIj0kRW06/cdDJKokmWQnxXXtw+9WG+wycDnqeQh6cVFjG66OkjDegRDhy8sbZG
Tqpww/ycFOT5CumDG1DkHwDIKnF9t5MO3xu2OGNPwxQqLalEIiJzo62kQglGSqJ6
TQIDAQAB
-----END PUBLIC KEY-----"""

    publickey = {
        "test": test_publickey,
        "dev": dev_publickey,
        "staging": staging_publickey,
    }[env_name]
    rsapk = rsa.PublicKey.load_pkcs1_openssl_pem(publickey.encode())
    return base64.b64encode(rsa.encrypt(text.encode(), rsapk)).decode()

def http_debug(url=None, data=None, headers=None, ret=None):
    """used for debugging a http request"""

    debug_info = ""
    if url:
        debug_info = f"{debug_info}\nurl: {url}"
    if data:
        debug_info = f"{debug_info}\ndata: {data}"
    if headers:
        debug_info = f"{debug_info}\nheaders: {headers}"
    if ret:
        debug_info = f"{debug_info}\nret: {ret}"
    logger.debug(debug_info)

# a = get_passport_b_token(
#     client_id="349a9e1ac04c44ad", client_secret="904cae9755114eea8c19589e8ce7a215", user_name="lei.hong", password="@Hqy199367"
# )