import os
import sys
import json

current_path = os.path.dirname(os.path.realpath(__file__))
from xat_ecu.legacy.common.logger import *
from download_service_from_youzi import WebDriverTool

soazipconf_path = '/root/soazip/soazipconf.json'
artifactory_base_path = 'https://repo.jidudev.com/artifactory/SOASDK/SoaAutoTestPackages'
ARTIFACTORY_USERNAME = "sunquan_onwner"
ARTIFACTORY_PASSWORD = __import__("os").environ.get('XAT_CREDENTIAL_ECU__TOOLS_SETUP_ENV_GENERATE_SOA_PARTNER_PY_ARTIFACTORY_PASSWORD', "")
soazip_name = 'soa.zip'
ignore_ip = '172.18.128.5'


def get_soa_name():
    # get soa path
    if os.path.exists("/root/soagit/task.json"):
        with open("../../task.json", "r") as f:
            task = json.load(f)

            JIDLCompiler = task.get("JIDLCompiler")
            print("JIDLCompiler: {}".format(JIDLCompiler))

            X86_value = task.get("X86")
            print("X86: {}".format(X86_value))
            if "apus" in X86_value:
                global bootes_flag
                bootes_flag = False

            idl = task.get("idl")
            print("idl: {}".format(idl))
            soa_name = "SOA_" + JIDLCompiler + X86_value + idl
            soa_name = soa_name.replace(".", "_")
        return soa_name, JIDLCompiler, X86_value, idl


def change_partner_status(soa_name, status="Installing"):
    if not os.path.exists(soazipconf_path):
        with open(soazipconf_path, "w") as f:
            json.dump({}, f)
    with open(soazipconf_path) as f:
        soazipconf = json.load(f)
    with open(soazipconf_path, 'w') as f:
        if status is None:
            try:
                del soazipconf[soa_name]
            except:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/setup_env/generate_soa_partner.py")
                pass
        else:
            soazipconf[soa_name] = status
        json.dump(soazipconf, f, indent=4)


def check_partner_status(soa_name):
    if not os.path.exists(soazipconf_path):
        with open(soazipconf_path, "w") as f:
            json.dump({}, f)
    with open(soazipconf_path, "r") as f:
        soazipconf = json.load(f)
        if soazipconf.get(soa_name) is None:
            return True
        elif soazipconf.get(soa_name) == 'Installing':
            print(f'{soa_name}正在生成中，无需再执行')
            return False
        elif soazipconf.get(soa_name) == 'Finish':
            print(f'{soa_name}已生成中，无需再执行')
            return False


def upload_soazip_to_artifactory(soa_name, soazip_name):
    print("upload to artifactory")
    cmd = f'curl -u {ARTIFACTORY_USERNAME}:{ARTIFACTORY_PASSWORD} -X PUT "{artifactory_base_path}/{soa_name}/{soazip_name}" -T /root/soazip/{soa_name}/{soazip_name}'
    res = os.system(cmd)
    if res == 0:
        print(f"====>>>>  upload fished, artifactory path is {artifactory_base_path}/{soa_name}/{soazip_name}")
        change_partner_status(soa_name, 'Finish')
    else:
        print(f"upload {artifactory_base_path}/{soa_name}/{soazip_name} failed")
        change_partner_status(soa_name, None)
        raise Exception(f"upload {artifactory_base_path}/{soa_name}/{soazip_name} failed")


if __name__ == '__main__':
    soa_name, JIDLCompiler, X86_value, idl = get_soa_name()
    if not check_partner_status(soa_name):
        exit(0)
    change_partner_status(soa_name)
    res = os.system(f'tools/setup_env/update_soagit_bootes.sh {JIDLCompiler} {X86_value} {idl}')
    if res != 0:
        print('更新代码失败')
        change_partner_status(soa_name, None)
        exit(1)
    # 下载已发布的partner包
    web_client = WebDriverTool()
    web_client.login()
    web_client.download_all_service(JIDLCompiler, idl, "soa_partner/BootesRelease/out")
    res = os.system(f'tools/setup_env/makezipmv_soa_bootes.sh /root/soazip/{soa_name}/')
    if res != 0:
        print('打包失败')
        change_partner_status(soa_name, None)
        exit(1)
    upload_soazip_to_artifactory(soa_name, soazip_name)
