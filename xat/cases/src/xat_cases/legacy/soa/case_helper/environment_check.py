import os
import subprocess
import sys
import time

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
from xat_ecu.legacy.common.logger import logger


def can_status_check(can_name):
    """
    检查上位机的CAN网卡是否是启动状态，如果未启动，则即时启动
    """
    check_cmd = f"ifconfig | grep {can_name}"
    pi = subprocess.Popen(check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    stdout = pi.stdout.read().replace('\n', '')
    if stdout:
        logger.info("查询到{}网卡信息：{}".format(can_name, stdout))
    else:
        logger.info("未查询到{}网卡信息".format(can_name))
    if stdout.count(can_name) > 0:
        return True
    else:
        start_cmd = f"ip link set {can_name} up type can bitrate 500000 restart-ms 300"
        pi = subprocess.Popen(start_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        stdout = pi.stdout.read()
        if not stdout:
            logger.info("{} up success".format(can_name))
            return True
        else:
            logger.info("error message: {}".format(stdout), end='')
            return False


def vlan5_status_check():
    """
    检查上位机的vlan5是否就绪
    """
    check_cmd = f"ping 172.16.5.1 -c 4"
    pi = subprocess.Popen(check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    stdout = pi.stdout.read()
    res = filter(lambda x: x.count('icmp_seq') == 1, stdout.split('\n'))
    res_list = list(res)
    if len(res_list) == 4:
        logger.info("上位机ping 172.16.5.1：success")
        return True
    else:
        logger.info("上位机ping 172.16.5.1：fail")
        return False


def partner_process_check():
    """
    检查上位机上是否有其它未关闭的soa_partner进程在运行，如果有，则杀死进程
    """
    check_cmd = f"ps -ef | grep soa_partner | grep -v grep"
    pi = subprocess.Popen(check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    stdout = pi.stdout.read()
    if stdout:
        logger.info("命令执行结果：\n{}".format(stdout))
        stdout = stdout.split('\n')
        pid_list = []
        for s in stdout:
            if s:
                s = ' '.join(s.split())  # 合并连续的空格
                s = s.split(' ')
                pid_list.append(s[1])
        if len(pid_list):
            kill_pid_str = ''
            for pid in pid_list:
                kill_pid_str += pid
                kill_pid_str += ' '
            check_cmd = f"kill -9 {kill_pid_str}"
            pi = subprocess.Popen(check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  encoding='utf-8')
            time.sleep(1)
            stdout = pi.stdout.read()
            if stdout:
                logger.info("error: {}".format(stdout))
                logger.info("process kill fail")
                time.sleep(1)
                return False
            else:
                logger.info("process kill success")
                time.sleep(1)
                return True
    else:
        # logger.info("没有残留的soa partner 进程")
        return True


def s2s_before_check():
    """
        s2s自动化测试前进行环境检查
    """
    result_list = []
    logger.info("开始进行环境检查....")
    result_list.append(can_status_check('can0'))
    result_list.append(can_status_check('can1'))
    result_list.append(can_status_check('can2'))
    result_list.append(can_status_check('can3'))
    result_list.append(can_status_check('can4'))
    result_list.append(can_status_check('can5'))
    result_list.append(partner_process_check())
    result_list.append(vlan5_status_check())

    return all(result_list)


if __name__ == '__main__':
    can_status_check('can0')
    vlan5_status_check()
    partner_process_check()

