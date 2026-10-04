
import os
from signal import signal
import signal
import subprocess

from xat_ecu.legacy.sdk.soa_partner.partner_helper import check_soa_partner, deploy_soa_partner
from xat_ecu.legacy.common.logger import logger


class StartPartnerBase:
    """
    Soa partner 启动类，启动的过程中会检查本地部署的版本，如果非匹配版本，则部署匹配版本
    """
    def __init__(self, name, operator_port=16789, deploy_path="/root/soa_partner", soa_version_name=None):
        """
        operator_port：启动soa partner时使用的默认端口
        project_path：
        """
        self.process = None
        self.operator_port = operator_port
        self.pid = None
        self.name = name
        self.soa_version_name = soa_version_name
        self.deploy_path = deploy_path + "/BootesRelease"
        self.deploy_result = False
        try:
            if not os.path.exists(deploy_path):
                os.makedirs(deploy_path)
            is_deploy_soa_partner = check_soa_partner(deploy_path, self.soa_version_name)  # 启动时检查是否需要升级
            if is_deploy_soa_partner:
                deploy_soa_partner(deploy_path, self.soa_version_name)  # 升级soa partner
            self.deploy_result = True
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/soa_partner/PartnerStart.py")
            logger.info("soa partner 启动检查失败")
            raise e

    def run_operator(self, domain='acu'):
        idl_path = self.deploy_path
        apus_path = os.path.join(self.deploy_path, 'X86')
        soa_partner_path = os.path.join(self.deploy_path, 'Tools', 'bin', 'soa_partner')
        start_cmd = f'{soa_partner_path} -r {idl_path} -s {apus_path} run -d {domain} -p {self.operator_port}'

        logger.info(start_cmd)
        self.process = subprocess.Popen(start_cmd, shell=True, close_fds=True, preexec_fn=os.setsid)
        self.pid = self.process.pid

    def stop_operator(self):
        try:
            self.process.terminate()
            self.process.wait()
            os.killpg(self.pid, signal.SIGINT)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/soa_partner/PartnerStart.py")
            logger.warning("Stop SOA operator Error : {}".format(e))
