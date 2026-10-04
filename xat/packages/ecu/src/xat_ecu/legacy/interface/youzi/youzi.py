import base64
import os

from xat_ecu import reporting as allure
from jal_cloud_communication import Client
from xat_ecu.legacy.common.constant import YouZiConstant
from xat_ecu.legacy.common.logger import logger


class YouZiClient(Client):
    def __init__(self,
                 host='http://youzi.jidudev.com',
                 username=base64.b64decode(YouZiConstant.USERNAME).decode(),
                 password=base64.b64decode(YouZiConstant.PASSWORD).decode()):
        self.host = host
        self.username = username
        self.password = password
        self.nc = None
        try:
            self.login_youzi()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/youzi/youzi.py")
            logger.error("登入失败: {}".format(e))

    def login_youzi(self):
        self.nc = Client(host=self.host)
        self.nc.login(user=self.username, password=self.password)

    def upload_files_to_youzhi(self, local_file_path, remote_dir_path):
        """
        将本地文件上传到指定的远程目录，并生成一个无需密码的分享链接。

        Args:
            local_file_path (str): 要上传的本地文件路径。
            remote_dir_path (str, optional): 远程目录路径。

        Returns:
            str: 生成的无密码分享链接。
        """
        remote_dir_path = remote_dir_path + os.path.basename(local_file_path)
        self.nc.put_file(remote_file_path=remote_dir_path, local_file_path=local_file_path)
        link = self.nc.simply_share_no_passwd(remote_path=remote_dir_path)
        return link
if __name__ == '__main__':
    a = YouZiClient()
    b = a.upload_files_to_youzhi('/root/lei_test/sat/ecu-simulator/xat_ecu/legacy/interface/youzi/11.text',
                                 '/SOA/JFS_route_map/')
    print(b)
