import os
import re

from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.perstable.case_helper.constant import WORK_PATH, BGM_LOG_PATH
from xat_cases.legacy.perstable.case_helper.constant import testParameter


def handle_bgm_logs(self, bgm_log_path, mcu=True):
    try:
        for root, dirs, files in os.walk(bgm_log_path):
            for file in files:
                if file.startswith('jetlog_messages') and file.endswith('.zst'):
                    print('current_file:', file)
                    file_path = os.path.join(root, file)
                    replace_file = os.path.join(root, 'ana_bgm', file.replace("zst", "txt"))
                    self.decompress_zst_file(file_path, replace_file)
                    if os.path.exists(replace_file):
                        self.read_log(replace_file)
                        if mcu:
                            self.analysis_bgm_mcu_log()
                            self.write_to_csv(os.path.join(bgm_log_path, "bgm_mcu_list.csv"), self.mcu_cpu_list)

                        self.analysis_bgm_log()
                        self.write_to_csv(os.path.join(bgm_log_path, "bgm_thread_list.csv"), self.bgm_thread_list)
                        self.write_to_csv(os.path.join(bgm_log_path, "bgm_cpu_list.csv"), self.bgm_cpu_list)
                        self.write_to_csv(os.path.join(bgm_log_path, "bgm_mem_list.csv"), self.bgm_mem_list)

    except Exception as e:
        self.logger.error('处理bgm日志error:{}'.format(e))


def handle_tcam_logs(self, tcam_log_path):
    for root, dirs, files in os.walk(tcam_log_path):
        for file in files:
            if file.startswith('jetlog_messages') and file.endswith('.zst'):
                print('current_file:', file)
                file_path = os.path.join(root, file)
                replace_file = os.path.join(root, 'ana_tcam', file.replace("zst", "txt"))
                self.decompress_zst_file(file_path, replace_file)
                if os.path.exists(replace_file):
                    self.read_log(replace_file)
                    self.analysis_tcam_log()
                    self.write_to_csv(os.path.join(tcam_log_path, "tcam_cpu_list.csv"), self.tcam_cpu_list)
                    self.write_to_csv(os.path.join(tcam_log_path, "tcam_mem_list.csv"), self.tcam_mem_list)
                    self.write_to_csv(os.path.join(tcam_log_path, "tcam_thread_list.csv"),
                                      self.tcam_thread_list)


def calc_uptime_seconds(uptime: str):
    """
    calc the linux system running time, unit is seconds
    parameter: uptime is provided by running command 'uptime -p', example: up 1 year, 11 weeks, 4 days, 9 hours, 43 minutes
    return: seconds of system running time
    """
    time_dict = {
        "year": 365 * 24 * 60 * 60,
        "week": 7 * 24 * 60 * 60,
        "day": 24 * 60 * 60,
        "hour": 60 * 60,
        "minute": 60
    }
    summary_seconds = 0
    uptime = uptime.replace("up", '').strip().split(',')
    for t in uptime:
        time_value, time_type = t.split()
        time_type = time_type[:-1] if time_type[-1] == 's' else time_type
        summary_seconds += float(time_value) * time_dict.get(time_type, 0)

    return summary_seconds


def print_run_time(test_duration):
    hours = test_duration // 3600
    minutes = (test_duration % 3600) // 60
    seconds = test_duration % 60
    logger.info(f"程序运行了{hours}小时{minutes}分{seconds}秒")


def scp_bgm_file_to_local(bgm_ssh: BGM_SSH, src_path: str, dest_path: str):
    cmd = f"ls {src_path}/jetlog_message*.zst -lht"
    out = bgm_ssh.type_commands(cmd).split("\n")
    valid_jetlog_files = [file for file in out if (file.startswith('-rw') and file.endswith("zst") and '11M' in file)]

    for file in valid_jetlog_files:
        file_info = str(file).split()
        file_size, file_name = file_info[4], file_info[-1]
        existed_files, _ = subprocess_run(cmd=f"ls {dest_path}")
        if file.split("/")[-1] in str(existed_files).split():
            continue
        logger.info(f"开始拉取{file_name}...")
        bgm_ssh.type_commands(f"chmod 777 {file_name}")
        bgm_ssh.scp_bgm_file_to_local(bgm_file_pah=file_name, local_path=dest_path, del_flag=False, connect_type='obd')


def scp_local_file_to_bgm(bgm_ssh: BGM_SSH, local_path: str, bgm_path='/log/'):
    bgm_ssh.scp_local_file_to_bgm(local_path=local_path, bgm_path=bgm_path)


def is_bgm_reboot():
    bgm_log_files = [os.path.join(BGM_LOG_PATH, file) for file in os.listdir(BGM_LOG_PATH) if file.startswith("jetlog_messages") and file.endswith("txt")]
    patterns = [r".*?E MCUL:.*?McuDetModuleId 58368.*", r".*?I MCUL:.*?McuModuleId 229.*"]

    for file in bgm_log_files:
        for line in read_large_file_generator(file):
            for pattern in patterns:
                if re.search(pattern, line):
                    print(f"BGM系统有重启过。具体请参{file}里面的{line}")
                    return True, file, line
    else:
        return False, '', ''


def read_log_file(file):
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as fr:
            lines = fr.read()
    except Exception as e:
        lines = ''
        print("Error {} happened in line {}".format(e, e.__traceback__.tb_lineno))
    return lines


def read_large_file_generator(file_path):
    with open(file_path, 'rb') as f:
        for line in f:
            try:
                yield line.decode('utf-8').strip()
            except UnicodeDecodeError:
                logger.info(f"UnicodeDecodeError happened in {file_path} \n\tline: {line}")
                yield ''


def subprocess_run(cmd, cmd_input=None, timeout=60):
    """
    执行 cmd 命令
    """
    import subprocess
    try:
        if cmd_input is not None:
            # 创建子进程并执行命令
            cmd_process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           shell=True)
            input_context = '{}\n'.format(cmd_input).encode('utf-8')
            cmd_process.stdin.write(input_context)
            stdout, stderr = cmd_process.communicate(timeout=timeout)
        else:
            cmd_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = cmd_process.communicate(timeout=timeout)
    except Exception as e:
        logger.error(f'执行命令超时，超时信息：{e}')
        return None, None
    else:
        return stdout.decode('utf-8'), stderr.decode()


def exec_shell(command):
    import subprocess
    try:
        # 执行命令
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 等待命令执行完成
        process.wait()
        # 获取命令的输出和错误信息
        output = process.stdout.read()
        error = process.stderr.read()
        # 将输出和错误信息解码为字符串
        output = output.decode(encoding="utf-8")
        error = error.decode(encoding="utf-8")
    except Exception as e:
        output = ""
        error = str(e)
    # 返回命令的输出和错误信息
    result = {"output": output, "error": error}
    logger.info(result)
    return result


def get_pcap_file(ids=False):
    if os.path.exists("/root/test_data/pcap"):
        file_list = os.listdir("/root/test_data/pcap")
        test_cases = [os.path.join(WORK_PATH, file) for file in file_list if file.endswith("pcap")]
    else:
        test_cases = []

    if ids:
        logger.info("=============================================")
        logger.info(f"pcap数据包下用例个数：{len(test_cases)}")
        logger.info("=============================================")
        return list(range(1, len(test_cases) + 1))
    else:
        return test_cases


if __name__ == "__main__":
    get_pcap_file()
