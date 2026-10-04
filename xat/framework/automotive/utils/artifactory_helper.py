#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :artifactory_helper.py
@time         :6/3/24 21:27
@author       :dejian.xiong@jiduauto.com
@description  :
"""
from artifactory import ArtifactoryPath

ARTIFACTORY_USERNAME = "public_soa_bgm_tcam"
ARTIFACTORY_PASSWORD = __import__("os").environ.get('XAT_CREDENTIAL_PYTEST___UTILS_ARTIFACTORY_HELPER_PY_ARTIFACTORY_PASSWORD', "")

ARTIFACTORY_QUAN_USERNAME = "sunquan_onwner"
ARTIFACTORY_QUAN_PASSWORD = __import__("os").environ.get('XAT_CREDENTIAL_PYTEST___UTILS_ARTIFACTORY_HELPER_PY_ARTIFACTORY_QUAN_PASSWORD', "")


class ArtifactoryHelper:

    @staticmethod
    def get_keyinfo(url):
        """
        从给定的URL中读取内容，并提取'keyInfo:'后的内容（不包括冒号和末尾的换行符）。

        参数:
        url (str): Artifactory中的文件URL

        返回:
        str: 提取的'keyInfo:'后的内容
        """
        ap = ArtifactoryPath(url, auth=(ARTIFACTORY_USERNAME, ARTIFACTORY_PASSWORD))
        with ap.open() as f:
            result = f.read().decode()
        if "keyInfo:" in result:
            keyinfo = result.split('keyInfo:')[-1][:-1]
            return keyinfo
    
    @staticmethod
    def get_bin_keyinfo(url):
        """
        从指定URL获取二进制文件的key信息。
        
        Args:
            url (str): 二进制文件的URL。
        
        Returns:
            str: 返回key信息。
        
        """
        ap = ArtifactoryPath(url, auth=(ARTIFACTORY_USERNAME, ARTIFACTORY_PASSWORD))
        return ap.properties.get("keyInfo")[0]
    @staticmethod
    def get_boot_url(url):
        """
        在给定的URL下搜索以'29'开头且以'.bin'结尾的文件，并返回其URL。

        参数:
        url (str): Artifactory中的目录URL

        返回:
        str: 找到的文件的URL
        """
        ap = ArtifactoryPath(url, auth=(ARTIFACTORY_USERNAME, ARTIFACTORY_PASSWORD))
        for p in ap:
            if p.name.startswith('29') and p.name.endswith(".bin"):
                return str(p)

    @staticmethod
    def get_url_list(url):
        ap = ArtifactoryPath(url, auth=(ARTIFACTORY_USERNAME, ARTIFACTORY_PASSWORD))
        return [p.name for p in ap]

    @staticmethod
    def download(url, filename, username=ARTIFACTORY_USERNAME, password=ARTIFACTORY_PASSWORD):
        """
        从给定的URL下载文件内容，并将其保存到指定的本地文件名中。

        参数:
        url (str): Artifactory中的文件URL
        filename (str): 本地保存的文件名

        返回:
        str: 下载的文件内容
        """
        ap = ArtifactoryPath(url, auth=(username, password))
        with ap.open() as f:
            result = f.read().decode()
        with open(filename, 'w') as f:
            f.write(result)
        return result

    @staticmethod
    def upload(url, filename, username=ARTIFACTORY_USERNAME, password=ARTIFACTORY_PASSWORD):
        """
        将本地文件上传到给定的URL路径下。

        参数:
        url (str): Artifactory中的目标目录URL
        filename (str): 要上传的本地文件名

        返回:
        None
        """
        ap = ArtifactoryPath(url, auth=(username, password))
        ap.deploy_file(filename)

    @classmethod
    def upload_UA_info(cls):
        cls.upload(
            'https://repo.jidudev.com/artifactory/SOASDK/SoaAutoTestPackages/',
            "UA_download_info.json",
            ARTIFACTORY_QUAN_USERNAME,
            ARTIFACTORY_QUAN_PASSWORD
        )

    @classmethod
    def download_UA_info(cls):
        cls.download(
            'https://repo.jidudev.com/artifactory/SOASDK/SoaAutoTestPackages/UA_download_info.json',
            "UA_download_info.json",
            ARTIFACTORY_QUAN_USERNAME,
            ARTIFACTORY_QUAN_PASSWORD
        )


if __name__ == '__main__':
    ArtifactoryHelper.upload_UA_info()
