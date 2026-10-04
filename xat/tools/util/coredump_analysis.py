
password_key = __import__("os").environ.get('XAT_CREDENTIAL____UTIL_COREDUMP_ANALYSIS_PY_PASSWORD_KEY', "")

import json
import os
from datetime import datetime

import pexpect
import requests


def upload_log_to_platform(log_path: str, log_name: str, id: int):
    log_full_path = os.path.join(log_path, log_name)

    url = rf'http://10.80.51.28:8887/agentCoreDump/updateAnalysisResult?agentCoreDumpId={id}'
    files = {'file': open(fr'{log_full_path}', 'r')}
    times = 1
    retry = 3
    while times <= retry:
        try:
            res = requests.post(
                url=url,
                files=files,
            ).json()
            status = res['status']
            print(f"{res}")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/util/coredump_analysis.py")
            print(f'upload log failed, {str(e)}')
            times += 1
        else:
            if status == 1:
                print('upload log success')
                return
            else:
                print('upload log failed')
                times += 1
    else:
        print(f'retry {retry} times, upload log failed')


def get_to_analysis_list():
    url = rf'http://10.80.51.28:8887/agentCoreDump/list'
    # data = {'analysis_result': "123", "agentIp": "172.18.128.7", "name": "32960"}
    data = {'analysisResult': "123", 'ecuType': "BGM"}
    print("查询的参数为: data {}".format(data))
    resp = requests.post(url=url, data=data)
    print(resp.text)
    return json.loads(resp.text)


def get_new_file(file_path):
    file_lists = os.listdir(file_path)
    file_lists.sort(
        key=lambda fn: os.path.getmtime(file_path + "/" + fn) if not os.path.isdir(file_path + "/" + fn) else 0)
    # 最新的文件
    filename_latest = file_lists[-1]
    print(filename_latest)
    return filename_latest


if __name__ == '__main__':
    result = get_to_analysis_list()
    ip_password = {"172.23.21.9": "jidu666", "172.18.128.138": '123', "172.18.128.144": 'Zzp1994'}
    ssh_newkey = 'Are you sure you want to continue connecting'
    for aa in result["data"]:
        if aa["analysisResult"]:
            continue
        print("======================")
        print(aa["agentIp"])
        print(aa["version"][-5:])
        version = aa["version"][-5:]
        agentCoreDumpId = aa["id"]
        file_name = aa["name"].split("/")[-1]
        print(aa["name"].split("/")[-1])
        if aa["md5"]:
            file_info = aa["filePath"].replace("http://10.80.51.28:8887/upload", "/root/master/static/upload")
            print("云端coredump: "+file_info)
            res = os.system(f"cp {file_info} /data/")
            if res == 0:
                print("server端 复制文件成功")
            else:
                print("server端 复制文件失败")
        else:
            command = f'scp root@{aa["agentIp"]}:/root/monitor/agent/tmp/{aa["name"].split("/")[-1]} /data/'
            # if not os.path.isdir("/data/tmp/"):
            #     os.mkdir("/data/tmp/")
            if not os.path.isfile(f'/data/{aa["name"].split("/")[-1]}'):  # 文件不存在
                try:

                    execute = pexpect.spawn(command, timeout=600)
                    ret = execute.expect([ssh_newkey, password_key])
                    if ret == 0:
                        execute.sendline('yes')
                        execute.expect(password_key)
                    execute.sendline(ip_password.get(aa["agentIp"], "jidu123"))
                    execute.expect(pexpect.EOF)
                    print("agent 拷贝文件成功")
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/util/coredump_analysis.py")
                    print("agent 拷贝文件失败")
                    continue
        print(f'./bgm_parse_coredump.sh -c {file_name} -v {version}')
        res = os.system(f'./bgm_parse_coredump.sh -c {file_name} -v {version}')
        if res != 0:
            print('分析文件失败')
            continue
        else:
            print("分析文件成功")
            upload_log_to_platform("/data", get_new_file("/data"), agentCoreDumpId)
            os.system(f"rm -rf /data/{file_name}")
        print("======================")



