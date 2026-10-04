import os
import sys
from os.path import join
from subprocess import CalledProcessError, check_output
import argparse

ecu_simulator_path = os.path.join(
    os.path.realpath(__file__).split("ecu_simulator")[0], 'ecu_simulator'
)
from xat_ecu.legacy.common.logger import logger


class PypiManagerLinux:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.root_path = self.exec("cd ~ && pwd").strip()
        self.pip_conf_path = None
        self.pypirc_path = None

    def init_upload_env(self):
        self.make_dir_pip()
        self.touch_pip_conf()
        self.update_pip_conf()
        self.show_pip_conf_content()
        self.update_pypirc()
        self.show_pypirc_content()

    def exec(self, cmd):
        ret = check_output(cmd, shell=True).decode()
        logger.debug(f"{cmd}: {ret}")
        return ret

    def make_dir_pip(self):
        ret = self.exec("ls -al ~")
        if ".pip" in ret:
            logger.info("local pip dir exists")
            return
        self.exec(f"cd {self.root_path} && mkdir .pip")

    def touch_pip_conf(self):
        dir_path = self.exec("cd ~/.pip && touch pip.conf && pwd").strip()
        self.pip_conf_path = join(dir_path, "pip.conf")

    def update_pip_conf(self):
        if not self.pip_conf_path:
            logger.error("empty pip.conf path")
            return
        with open(self.pip_conf_path, "w") as f:
            f.writelines(
                [
                    "[global]\n",
                    f"index-url = https://{self.username}:{self.password}@repo.jidudev.com/artifactory/api/pypi/pypi/simple\n",
                ]
            )

    def show_pip_conf_content(self):
        if not self.pip_conf_path:
            logger.error("empty pip.conf path")
            return
        with open(self.pip_conf_path, "r") as f:
            content = f.read()
            logger.info(f"file {self.pip_conf_path} content:\n{content}")

    def update_pypirc(self):
        if not self.root_path:
            logger.error("empty root path")
            return
        self.pypirc_path = join(self.root_path, ".pypirc")
        with open(self.pypirc_path, "w") as f:
            f.writelines(
                [
                    "[distutils]\n",
                    "index-servers = local\n",
                    "[local]\n",
                    "repository: https://repo.jidudev.com/artifactory/api/pypi/Pypi-local\n",
                    f"username: {self.username}\n",
                    f"password: {self.password}\n",
                ]
            )

    def show_pypirc_content(self):
        if not self.pypirc_path:
            logger.error("empty pypirc path")
            return
        with open(self.pypirc_path, "r") as f:
            content = f.read()
            logger.info(f"file {self.pypirc_path} content:\n{content}")

    def build_and_upload(self):
        self.exec("python3 setup.py sdist")
        try:
            self.exec("python3 setup.py sdist upload -r local")
            logger.info("upload success")
        except CalledProcessError:
            logger.error("upload failed")


if __name__ == "__main__":
    __import__("os").environ['XAT_CREDENTIAL_SCAN_3CBDC2A1896E3B7A5731']

    # 参数解析
    parser = argparse.ArgumentParser(description="在 linux 环境下将项目打包上传到公司内部 pypi 源")
    parser.add_argument(
        "--username",
        "-u",
        type=str,
        help="请前往 https://repo.jidudev.com/ 查看 username",
        required=True,
    )
    parser.add_argument(
        "--password",
        "-p",
        type=str,
        help="请前往 https://repo.jidudev.com/ 查看 password",
        required=True,
    )
    args = vars(parser.parse_args())
    username = args["username"]
    password = args["password"]

    # 自动部署及打包上传到公司内部 pypi 源
    m = PypiManagerLinux(username=username, password=password)
    m.init_upload_env()
    m.build_and_upload()
