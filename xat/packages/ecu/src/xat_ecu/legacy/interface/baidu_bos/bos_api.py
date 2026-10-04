#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :bos_api.py
@Time         :2024/11/26 17:22
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
import base64

from baidubce.services.bos import storage_class
from baidubce.services.bos.bos_client import BosClient
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration

from xat_ecu.legacy.common.constant import BosConstant


class BosApi:
    def __init__(
            self,
            bos_host='bj.bcebos.com',
            ak=base64.b64decode(BosConstant.AK).decode(),
            sk=base64.b64decode(BosConstant.SK).decode(),
            bucket_name='jidu-bj-test-sil-test-soa-autotest-log'
    ):
        self.bos_host = bos_host
        self.ak = ak
        self.sk = sk
        self.bucket_name = bucket_name
        self.config = BceClientConfiguration(credentials=BceCredentials(self.ak, self.sk), endpoint=bos_host)
        self.bos_client = BosClient(self.config)

    def put_and_get_url(self, target_path, file_path, expiration_in_seconds=-1, save_type=storage_class.STANDARD_IA):
        """
        将文件上传到指定路径，并生成该文件的预签名URL。
        Args:
            target_path (str): 目标存储路径，即文件在对象存储中的位置。
            file_path (str): 本地文件路径，即要上传的文件的本地路径。
            expiration_in_seconds (int, optional): 预签名URL的有效期，以秒为单位。默认为-1，表示URL长期有效。
            save_type (str, optional): 存储类型。默认为storage_class.STANDARD_IA，表示低频存储。
        Returns:
            str: 生成的预签名URL。
        """
        if not target_path.startswith('/'):
            target_path = f"/{target_path}"
        file_name = file_path.split('/')[-1]
        target_path = f"{target_path}/{file_name}"
        self.bos_client.put_object_from_file(self.bucket_name, target_path, file_path, storage_class=save_type)
        return self.bos_client.generate_pre_signed_url(bucket_name=self.bucket_name, key=target_path,
                                                       expiration_in_seconds=expiration_in_seconds)


if __name__ == '__main__':
    bos_api = BosApi()
    # url = bos_api.put_and_get_url('/test/console (56).log', r'C:\Users\dejian.xiong\Downloads\console (56).log')
    ret = bos_api.bos_client.list_objects(bucket_name="jidu-bj-test-sil-test-soa-autotest-log", prefix='/test/')
    print(ret)
