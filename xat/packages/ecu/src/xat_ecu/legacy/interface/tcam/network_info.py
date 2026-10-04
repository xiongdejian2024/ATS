import os
import sys
import time

root_path = os.path.dirname(os.path.realpath(__file__))
current_path = root_path
from xat_ecu.legacy.common.logger import logger, Logger
from xat_ecu.legacy.driver.ssh_client import SSHClient


def show_net_operator(ssh_client):
    """
       显示运营商 返回值 0:移动，1:联通
    """
    mobile_strs = ["46000", "46002", "46004", "46007", "46008", "46013"]
    result, detail = at_cmd_run(ssh_client, 1, "CHINA MOBILE")
    if not result:
        result, detail = at_cmd_run(ssh_client, 2, mobile_strs)
    return (0, "移动") if result else (1, "联通")


def get_networkCard(ssh_client):
    """
    获取网卡 返回值 网卡列表(联通1个，移动4个)
    """
    check_cmd = f"ifconfig | grep rmnet_data"
    ssh_client.connect()
    connect_status = ssh_client.is_connected()
    if connect_status:
        stdin, stdout = ssh_client.type_commands(check_cmd)
        net_list = stdin.split("\n")
        return True, net_list
    else:
        logger.info("SSH connect fail! ")
        return False, []


def setFun(ssh_client, num):
    """
    设置功能模式 参数 0:最小功能模式 ;1:全功能模式
    """
    mobile_strs = ["OK"]
    result = None
    mode = "全功能模式" if num else "最小功能模式"
    if num == 0:
        result, detail = at_cmd_run(ssh_client, 3, mobile_strs)
        time.sleep(0.5)
        logger.info("最小功能模式设置结果：{}".format(result))
    elif num == 1:
        result = at_cmd_run(ssh_client, 4, mobile_strs)
        time.sleep(0.5)
        logger.info("全功能模式设置结果：{}".format(result))
    else:
        logger.info("Invalid num:{}".format(num))
    return result, mode


def get_netStatus(ssh_client):
    """
    网络状态 返回值 0：网络OK，-1:网络不OK
    """
    _, net_list = get_networkCard(ssh_client)
    net_list = [x.split(" ")[0] for x in net_list]
    result_list = []
    ssh_client.connect()
    connect_status = ssh_client.is_connected()
    if connect_status:
        for net in net_list:
            try:
                stdin, stdout = ssh_client.type_commands("ping -I {} www.baidu.com -c 4".format(net),
                                                         timeout=30, wait_time=20)
                logger.info("############ping -I {} www.baidu.com -c 4##############".format(net))
                logger.info(stdin)
                if stdin:
                    res = filter(lambda x: x.count('icmp_seq') == 1, stdin.split('\n'))
                    result_list.append(True if len(list(res)) == 4 else False)
                else:
                    result_list.append(False)
            except Exception:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/tcam/network_info.py")
                result_list.append(False)
    else:
        logger.info("ssh connect to server fail!")
    success_list = list(filter(lambda x: x is True, result_list))
    if len(net_list) >= 4 and len(success_list) >= 3:
        logger.info("Mobile")
        return 0, "网络OK"
    elif len(net_list) == 1 and len(success_list) == 1:
        logger.info("union")
        return 0, "网络OK"
    else:
        return -1, "网络不OK"


def get_regStatus(ssh_client):
    """
    网络注册状态 返回值 1：注册OK
    注：返回 0，1 是正常的，如果看到0，0 的话如果能上网也OK，可能显示问题
    """
    mobile_strs = ["OK"]
    result, detail = at_cmd_run(ssh_client, 6, mobile_strs)
    time.sleep(0.5)
    logger.info("get_regStatus 返回结果：{}".format(detail))
    if detail.count("0,0") > 0 or detail.count("0,1") > 0:
        return 1, "注册OK"
    else:
        return 0, "注册失败"


def get_netFormat(ssh_client):
    """
    网络制式 返回值 7: 4G ， >=11:5G ，2:机卡分离
    """
    mobile_strs = ["+COPS"]
    result, detail = at_cmd_run(ssh_client, 1, mobile_strs)
    time.sleep(0.5)
    for s in detail.split("\n"):
        if s.count("+COPS") > 0:
            num = int(s.split(",")[3])
            if num == 7:
                detail = "4G"
            elif num >= 11:
                detail = "5G"
            else:
                detail = "机卡分离"
            break
    else:
        detail = "error"
    return result, detail


def get_signalStrength(ssh_client):
    """
    信号强度: +csq: 26,99 ：数字26大于20，返回“Strong”，否则返回“Weak”
    """
    mobile_strs = ["+csq"]
    num = None
    result, detail = at_cmd_run(ssh_client, 5, mobile_strs)
    time.sleep(0.5)
    for s in detail.split("\n"):
        if s.count("+csq") > 0:
            num = int(s.split(" ")[1].split(",")[0])
            if num > 20:
                detail = "Strong"
            else:
                detail = "Weak"
            break
    else:
        detail = "error"
    return num, detail


def at_cmd_run(ssh_client, cmd_id, search_strs):
    """
    AT指令执行
    cmd_id：命令id，对应的network.sh 中的ID
    search_strs：搜索的字符串列表
    """
    check_cmd1 = f"sh /mnt/sdcard/network.sh {cmd_id} > /mnt/sdcard/temp.txt"
    check_cmd2 = f"cat /mnt/sdcard/temp.txt"
    ssh_client.connect()
    connect_status = ssh_client.is_connected()
    if connect_status:
        upload_at_shell(ssh_client)
        for i in range(10):
            logger.info(f"Execute num: {i+1}")
            ssh_client.type_commands(check_cmd1)
            time.sleep(2)
            stdin, stdout = ssh_client.type_commands(check_cmd2)
            for search_str in search_strs:
                if stdin.count(search_str) > 0:
                    logger.info("有效输出：{}".format(stdin))
                    after_at_cmd_run(ssh_client)
                    return True, stdin
        logger.info("未找到查询字符串：{}".format(search_strs))
        after_at_cmd_run(ssh_client)
        return False, "Not Found"
    else:
        logger.info("SSH connect fail! ")
        return False, "SSH connect fail! "


def rm_temp_file(ssh_client):
    """
    删除AT命令执行时，生成的临时文件、shell脚本
    """
    temp_cmd = "rm -rf /mnt/sdcard/temp.txt"
    shell_cmd = "rm -rf /mnt/sdcard/network.sh"
    ssh_client.connect()
    connect_status = ssh_client.is_connected()
    if connect_status:
        ssh_client.type_commands(temp_cmd)
        time.sleep(0.5)
        ssh_client.type_commands(shell_cmd)
        time.sleep(0.5)


def kill_at_process(ssh_client):
    """
    kill AT 后台进程
    """
    find_process_cmd = "ps -ef | grep smd8 | grep -v grep"
    ssh_client.connect()
    connect_status = ssh_client.is_connected()
    if connect_status:
        stdin, stdout = ssh_client.type_commands(find_process_cmd)
        stdin = stdin.split('\n')
        pid_list = []
        for s in stdin:
            if s:
                s = ' '.join(s.split())
                s = s.split(' ')
                pid_list.append(s[0])
        if len(pid_list):
            kill_pid_str = ' '.join(str(x) for x in pid_list)
            kill_cmd = f"kill -9 {kill_pid_str}"
            ssh_client.type_commands(kill_cmd)
            time.sleep(1)


def after_at_cmd_run(ssh_client):
    """
    AT命令执行完，后处理
    """
    kill_at_process(ssh_client)
    rm_temp_file(ssh_client)


def upload_at_shell(ssh_client):
    """
    上传AT命令对应的shell脚本
    """
    local_file = os.path.join(current_path, " ecu_simulator/interface/tcam/network.sh")
    put_result = ssh_client.put_file(local_file, "/mnt/sdcard/network.sh")
    if put_result:
        time.sleep(0.5)
        ssh_client.type_commands("chmod u+x /mnt/sdcard/network.sh")
        time.sleep(0.5)


if __name__ == '__main__':
    logger = Logger().get_logger("test")
    client = SSHClient('172.16.5.31', 22, 'root', 'oelinux123')
    logger.info("111111:{}".format(show_net_operator(client)))
    logger.info("222222:{}".format(get_networkCard(client)))
    logger.info("444444:{}".format(get_netStatus(client)))
    logger.info("555555:{}".format(get_regStatus(client)))
    logger.info("666666:{}".format(get_netFormat(client)))
    logger.info("777777:{}".format(get_signalStrength(client)))
    logger.info("333333:{}".format(setFun(client, 1)))
