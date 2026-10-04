# -*- coding: utf-8 -*-
import sys
import os
from hashlib import md5, sha1, sha256
project_root = __import__("xat_ecu.resources", fromlist=["LEGACY_ROOT"]).LEGACY_ROOT.as_posix()
from xat_ecu.legacy.common.logger import logger

class Hash:
    """
    获取下载文件的md5, sha1, sha256值
    """
    def __init__(self, strFilePath):

        self.strFilePath = strFilePath  # 文件绝对路径
        self.hashMD5 = ""  # MD5值
        self.hashSHA1 = ""  # SHA1值
        self.hashSHA256 = ""  # SHA256值

    def getMd5(self):  # 计算md5
        mdfive = md5()
        with open(self.strFilePath, 'rb') as f:
            mdfive.update(f.read())
        self.hashMD5 = mdfive.hexdigest().upper()
        return self.hashMD5

    def getSha1(self):  # 计算sha1
        sha1Obj = sha1()
        with open(self.strFilePath, 'rb') as f:
            sha1Obj.update(f.read())
        self.hashSHA1 = sha1Obj.hexdigest()
        return self.hashSHA1

    def getSha256(self):  # 计算sha256
        sha256Obj = sha256()  # Get the hash algorithm.
        with open(self.strFilePath, 'rb') as f:
            sha256Obj.update(f.read())  # Hash the data.
        self.hashSHA256 = sha256Obj.hexdigest()  # Get he hash value.
        return self.hashSHA256

def check(url, file):
    """
    校验远程文件与本地文件的sha256值
    """
    cmd = __import__("os").environ['XAT_CREDENTIAL_SCAN_965D63D31923F87092B7']
    stdout = os.popen(cmd).read()
    logger.info(f"JFrog上的bin文件的sha256值是{stdout}")
    data = Hash(strFilePath=file).getSha256()
    logger.info(f"下载的bin文件的sha256值是{data}")
    if stdout == data:
        logger.info("sha256值一致, 下载的bin包无误")
        return True
    else:
        logger.info("sha256值不一致, 请重新下载bin包")
        return False


if __name__ == '__main__':
    file = "./daily_build/6160110050AL.bin"
    url="https://repo.jidudev.com/artifactory/BGMSoftware/daily_build/6160110050AL.bin"
    data = check(url, file)
    print(data)
